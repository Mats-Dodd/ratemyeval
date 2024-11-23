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

SQLModel.metadata.create_all(engine)



@app.get("/overall-eval")
async def overall_eval(model1: str,
                        model2: str):
    with Session(engine) as session:
        results = session.exec(select(benchmark_results).where(benchmark_results.model.in_([model1, model2])))
        return results.all()