from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class BenchmarkRequest(BaseModel):
    Model: str
    Benchmark: str

@app.post("/benchmark", status_code=201)
async def benchmark(Model: str, Benchmark: str):
    print(f"Benchmarking {Model} against {Benchmark}")
    return {"message": f"Benchmarked {Model} against {Benchmark}"}

@app.get("/benchmark/{test_id}", status_code=200)
async def read_benchmark(test_id: uuid.UUID):
    print(f"Getting benchmark results for {test_id}")
    return {"message": f"Benchmark results for {test_id}"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to easyeval"}
