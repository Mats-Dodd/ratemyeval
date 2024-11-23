import json
import os
from dotenv import load_dotenv
import uuid
import logging
from fastapi import FastAPI, Form, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from typing import Optional

load_dotenv()

# Configure logging
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

@app.post("/upload-dataset", status_code=201)
async def upload_dataset(name: Optional[str] = Form(None), file: UploadFile = File(...)):
    logger.info("Uploading dataset")

    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Uploaded file must be a JSON file")
    
    content = await file.read()
    dataset = json.loads(content)

    dataset_entry = {
        "name": name if name else file.filename,
        "dataset": dataset
    }

    # Insert data into datasets table
    response = supabase.table("datasets").insert(dataset_entry).execute()

    logger.info(f"Dataset {name} uploaded successfully")
    return {
        "message": "Dataset uploaded successfully",
        "data": response.data[0]
    }
    """
    {
        "message": "Dataset uploaded successfully",
        "data": {
            "id": "85d16a6d-d927-4e44-a876-e9742125b763",
            "name": "sample_dataset.json",
            "dataset": [
                {
                    "input": "John moved to the kitchen. Mary is in the garden. Where is John?",
                    "target": "kitchen"
                },
                /* rest of the tasks */
            ]
        }
    }
    """


@app.post("/benchmark", status_code=201)
async def benchmark():
    logger.info("Running benchmark test")

    # ===================
    #  Run the benchmark
    # ===================
    with open("run_data.json", "r") as file:
        benchmark_results = json.load(file)
    
    with open("run_data_samples.json", "r") as file:
        benchmark_data = json.load(file)

    # Insert data into benchmark_results table
    supabase.table("benchmark_results").insert(benchmark_results[0]).execute()
    logger.info("Inserted benchmark results into benchmark_results table")
    
    # Insert data into benchmark_data table
    for i, run in enumerate(benchmark_data):
        supabase.table("benchmark_data").insert(run).execute()
        logger.info(f"Inserted benchmark data for run {i+1} into benchmark_data table")
    
    return {
        "message": "Benchmark test completed",
        "run_id": benchmark_results[0]["run_id"]
    }
    """
    {
        "message": "Benchmark test completed",
        "run_id": "GFJUCeSDrcsJMzch5HZ5an"
    }
    """

@app.get("/benchmark/{run_id}", status_code=200)
async def read_benchmark(run_id: str):
    logger.info(f"Getting benchmark results for {run_id}")
    query_response = supabase.table("benchmark_results").select("*").eq("run_id", run_id).execute()

    return {
        "message": f"Benchmark results for {run_id}",
        "data": query_response.data[0]
        }
    """
    {
        "message": "Benchmark results for GFJUCeSDrcsJMzch5HZ5an",
        "data": {
            "id": "b193dab8-b794-4ed0-a3c8-0a1f581fde38",
            "run_id": "GFJUCeSDrcsJMzch5HZ5an",
            "model": "openai/gpt-4",
            "prompt": "{prompt}",
            "accuracy": 0.79,
            "stderr": 0.0409360181,
            "run_start": "2024-11-23T00:27:58-08:00",
            "run_end": "2024-11-23T00:40:23-08:00",
            "upper_bound": 0.8702345954,
            "lower_bound": 0.7097654046
        }
    }
    """

@app.get("/")
async def read_root():
    return {"message": "Welcome to easyeval"}
