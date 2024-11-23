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

# Benchmark model
class BenchmarkRequest(BaseModel):
    model_name: str
    dataset_id: str

# Upload dataset
def csv_to_json(file_content: bytes) -> List[dict]:
    content_str = file_content.decode("utf-8")
    csv_reader = csv.DictReader(content_str.splitlines())
    
    # Convert rows to JSON format
    result = [{"input": row["input"], "target": row["target"]} for row in csv_reader]
    return result

@app.post("/upload-dataset", status_code=201)
async def upload_dataset(name: Optional[str] = Form(None), file: UploadFile = File(...)):
    logger.info("Uploading dataset")

    # Check if the uploaded file is valid
    if file.content_type not in ["application/json", "text/csv"]:
        raise HTTPException(status_code=400, detail="Uploaded file must be a JSON or CSV file")
    
    content = await file.read()

    # Determine file format and convert content accordingly
    if file.content_type == "application/json":
        dataset = json.loads(content)
    elif file.content_type == "text/csv":
        dataset = csv_to_json(content)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

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
async def benchmark(request: BenchmarkRequest):
    model_name = request.model_name
    dataset_id = request.dataset_id
    dataset_response = supabase.table("datasets").select("*").eq("id", dataset_id).execute()
    logger.info(f"Running benchmark test for model: {model_name}, dataset_id: {dataset_id}")
    print(dataset_response.data)

    # ===================
    #  Run the benchmark with model_name and dataset_id
    # ===================

    with open("benchmark_results.json", "r") as file:
        benchmark_results = json.load(file)
    
    with open("benchmark_data.json", "r") as file:
        benchmark_data = json.load(file)

    # Insert data into benchmark_results table
    for i, run in enumerate(benchmark_results):
        supabase.table("benchmark_results").insert(run).execute()
    
    # Insert data into benchmark_data table
    for i, run in enumerate(benchmark_data):
        supabase.table("benchmark_data").insert(run).execute()
    
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

# Get benchmark results
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
