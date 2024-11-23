import os
from dotenv import load_dotenv
import uuid
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client

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

@app.post("/benchmark", status_code=201)
async def benchmark(Model: str, Benchmark: str):
    logger.info(f"Benchmarking {Model} against {Benchmark}")
    test_id = uuid.uuid4()
    benchmark_data = {"Model": Model, "Benchmark": Benchmark, "test_id": test_id}
    # supabase.from_table("benchmarks").insert([benchmark_data]).execute()
    
    return {"message": f"Benchmarked {Model} against {Benchmark}"}

@app.get("/benchmark/{test_id}", status_code=200)
async def read_benchmark(test_id: uuid.UUID):
    logger.info(f"Getting benchmark results for {test_id}")
    # benchmark_data = supabase.from_table("benchmarks").select("*").eq("test_id", test_id).execute()

    return {
        "message": f"Benchmark results for {test_id}",
        # "data": benchmark_data
        }

@app.get("/")
async def read_root():
    return {"message": "Welcome to easyeval"}
