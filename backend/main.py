import csv
import json
import os
from dotenv import load_dotenv
import uuid
import logging
from fastapi import FastAPI, Form, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
import pandas as pd
import numpy as np
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Supabase client initialization
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)


@app.get("/")
async def read_root():
    return {"message": "Welcome to easyeval"}


class OverallEval(BaseModel):
    dataset: str
    model1: str
    model2: str


engine = create_engine(os.getenv('DATABASE_URL'))

class benchmark_results(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    run_id: str
    dataset: str
    model: str
    prompt: str
    accuracy: float
    stderr: float
    run_start: str
    run_end: str
    input_tokens: int
    run_input_tokens: int
    run_output_tokens: int
    run_total_tokens: int
    upper_bound: float
    lower_bound: float


class benchmark_data(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    run_id: str
    sample_id: str
    epoch: int
    input: str
    target: str
    output: str
    score: str
    score_binary: int
    cumulative_score: int
    cumulative_score_percentage: float


SQLModel.metadata.create_all(engine)



@app.get("/overall-eval")
async def overall_eval(model1: str, model2: str):
    with Session(engine) as session:
        # Execute query and convert results to dictionaries
        results = session.exec(
            select(
                benchmark_results.model, 
                benchmark_results.accuracy, 
                benchmark_results.stderr
            ).where(benchmark_results.model.in_([model1, model2]))
        )
        # Convert results to a list of dictionaries
        return [
            {
                "model": row.model,
                "accuracy": round(row.accuracy, 2),
                "stderr": round(row.stderr, 2)
            }
            for row in results
        ]
    
@app.get("/dataset-eval")
async def dataset_eval(model1: str, model2: str):
    with Session(engine) as session:
        run_ids = session.exec(select(benchmark_results.run_id).where(benchmark_results.model.in_([model1, model2]))).all()
        results1 = session.exec(
            select(
                benchmark_data.sample_id,
                benchmark_data.input,
                benchmark_data.target,
                benchmark_data.output,
                benchmark_data.score
            ).where(benchmark_data.run_id == run_ids[0])
        )
        results2 = session.exec(
            select(
                benchmark_data.sample_id,
                benchmark_data.input,
                benchmark_data.target,
                benchmark_data.output,
                benchmark_data.score
            ).where(benchmark_data.run_id == run_ids[1])
        )

        # Convert results to pandas DataFrames
        df1 = pd.DataFrame([{
            "score": row.score,
            "sample_id": row.sample_id,
            "input": row.input,
            "target": row.target,
            "output": row.output
        } for row in results1])

        df2 = pd.DataFrame([{
            "score": row.score,
            "sample_id": row.sample_id,
            "input": row.input,
            "target": row.target,
            "output": row.output
        } for row in results2])

        merged_df = pd.merge(df1, df2, on="sample_id", suffixes=("_model1", "_model2"))

        return_df = merged_df[["sample_id", 
                               "input_model1",
                                 "target_model1",
                                 "output_model1",
                                 "output_model2",
                                 "score_model1",
                                 "score_model2"]].rename(columns={"input_model1": "input",
                                                                   "target_model1": "target",
                                                                   "output_model1": "output_model1",
                                                                   "output_model2": "output_model2",
                                                                   "score_model1": "score_model1",
                                                                   "score_model2": "score_model2"})

        return return_df.to_dict(orient="records")
    


@app.get("/compare-naive")
async def compare_naive(model1: str, model2: str):
    with Session(engine) as session:
        results = session.exec(select(benchmark_results.model,
                                      benchmark_results.accuracy,
                                      benchmark_results.stderr).where(benchmark_results.model.in_([model1, model2])))
        
        df = pd.DataFrame([{
            "model": row.model,
            "accuracy": row.accuracy,
            "stderr": row.stderr
        } for row in results])

        model1_mean_accuracy = df[df['model'] == model1]['accuracy'].iloc[0]
        model2_mean_accuracy = df[df['model'] == model2]['accuracy'].iloc[0]

        model1_stderr = df[df['model'] == model1]['stderr'].iloc[0]
        model2_stderr = df[df['model'] == model2]['stderr'].iloc[0]

        diff_mean_accuracy = model1_mean_accuracy - model2_mean_accuracy
        diff_stderr = np.sqrt(model1_stderr**2 + model2_stderr**2)

        upper_bound = diff_mean_accuracy + 1.96 * diff_stderr
        lower_bound = diff_mean_accuracy - 1.96 * diff_stderr

        z_score = diff_mean_accuracy / diff_stderr

        is_significant_at_90_confidence = z_score > 1.645 or z_score < -1.645
        is_significant_at_95_confidence = z_score > 1.96 or z_score < -1.96
        is_significant_at_99_confidence = z_score > 2.58 or z_score < -2.58
        is_significant_at_99_9_confidence = z_score > 3.29 or z_score < -3.29


        return {
            'diff_mean_accuracy': round(float(diff_mean_accuracy), 2),
            'diff_stderr': round(float(diff_stderr), 2),
            'upper_bound': round(float(upper_bound), 2), 
            'lower_bound': round(float(lower_bound), 2), 
            'z_score': round(float(z_score), 2), 
            'is_significant_at_90_confidence': bool(is_significant_at_90_confidence), 
            'is_significant_at_95_confidence': bool(is_significant_at_95_confidence), 
            'is_significant_at_99_confidence': bool(is_significant_at_99_confidence), 
            'is_significant_at_99_9_confidence': bool(is_significant_at_99_9_confidence)
        }
    

@app.get("/compare-smart")
async def compare_smart(model1: str, model2: str):

    n_samples = 100
    with Session(engine) as session:
        results = session.exec(select(benchmark_results.run_id,
            benchmark_results.model,
                                      benchmark_results.accuracy).where(benchmark_results.model.in_([model1, model2])))
        
        df = pd.DataFrame([{
            "run_id": row.run_id,
            "model": row.model,
            "accuracy": row.accuracy
        } for row in results])

        model1_mean_accuracy = df[df['model'] == model1]['accuracy'].iloc[0]
        model2_mean_accuracy = df[df['model'] == model2]['accuracy'].iloc[0]


        diff_mean_accuracy = model1_mean_accuracy - model2_mean_accuracy

        models = [model1, model2]
        run_ids = df['run_id'].tolist()

        df_samples = session.exec(select(benchmark_data.run_id,
                                         benchmark_data.sample_id,
                                         benchmark_data.score_binary).where(benchmark_data.run_id.in_(run_ids)))
        
        df_samples = pd.DataFrame([{
            "run_id": row.run_id,
            "sample_id": row.sample_id,
            "score_binary": row.score_binary
        } for row in df_samples])

        run1_df = df_samples[df_samples['run_id'] == run_ids[0]][['run_id', 'sample_id', 'score_binary']]
    run2_df = df_samples[df_samples['run_id'] == run_ids[1]][['run_id', 'sample_id', 'score_binary']]

    merged_df = run1_df.merge(run2_df, on='sample_id', suffixes=('_run1', '_run2'))

    merged_df['score_diff'] = merged_df['score_binary_run1'] - merged_df['score_binary_run2']

    merged_df['diff_mean_accuracy'] = diff_mean_accuracy

    merged_df['score_diff_agg_sqaured'] = (merged_df['score_diff'] - merged_df['diff_mean_accuracy'])**2

    sum_squared_diffs = merged_df['score_diff_agg_sqaured'].sum()

    multiplier = 1/(n_samples - 1)

    paired_se = ((sum_squared_diffs * multiplier) / n_samples)**0.5

    upper_bound = diff_mean_accuracy + 1.96 * paired_se
    lower_bound = diff_mean_accuracy - 1.96 * paired_se

    z_score = diff_mean_accuracy / paired_se

    is_significant_at_90_confidence = z_score > 1.645 or z_score < -1.645
    is_significant_at_95_confidence = z_score > 1.96 or z_score < -1.96
    is_significant_at_99_confidence = z_score > 2.58 or z_score < -2.58
    is_significant_at_99_9_confidence = z_score > 3.29 or z_score < -3.29

    return {'diff_mean_accuracy': float(round(diff_mean_accuracy, 2)),
            'diff_stderr': float(round(paired_se, 2)),
            'upper_bound': float(round(upper_bound, 2)), 
            'lower_bound': float(round(lower_bound, 2)), 
            'z_score': float(round(z_score, 2)), 
            'is_significant_at_90_confidence': bool(is_significant_at_90_confidence), 
            'is_significant_at_95_confidence': bool(is_significant_at_95_confidence), 
            'is_significant_at_99_confidence': bool(is_significant_at_99_confidence), 
            'is_significant_at_99_9_confidence': bool(is_significant_at_99_9_confidence)}        