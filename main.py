from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import asyncio
from parallel_benchmarker import benchmark_models_parallel

from models import (
    BenchmarkRequest,
    BenchmarkResponse,
    ModelEvaluation,
    ABTestConfig,
    ABTestResult
)
from benchmarker import benchmark_models
from services.huggingface_service import HuggingFaceService
from services.openai_service import OpenAIService
from services.ab_test_service import ABTestService
from utils.csv_logger import log_benchmark_to_csv
from services.llm_service import LegalLLMService 

app = FastAPI(
    title="Legal AI Model Benchmarker",
    description="An API to benchmark different question-answering models on legal queries",
    version="1.0.0",
)

import os
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

os.makedirs(templates_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/benchmark", response_model=BenchmarkResponse)
async def benchmark(request: BenchmarkRequest, save_to_csv: bool = False):
    """
    Benchmark multiple AI models on a legal question.
    """
    if not request.question or len(request.question.strip()) < 5:
        raise HTTPException(status_code=400, detail="Question must contain at least 5 characters")

    models = []

    try:
        llm_service = LegalLLMService()
        models.append(llm_service)
    except Exception as e:
        from services.simplified_service import SimplifiedModelService
        models.append(SimplifiedModelService())

    try:
        huggingface_service = HuggingFaceService()
        models.append(huggingface_service)
    except Exception as e:
        pass

    try:
        openai_service = OpenAIService()
        models.append(openai_service)
    except Exception as e:
        pass

    results = benchmark_models(request.question, models, request.expected_keywords)

    if save_to_csv:
        log_benchmark_to_csv(request.question, results, request.expected_keywords)
    
    return BenchmarkResponse(
        question=request.question,
        models=results,
        expected_keywords=request.expected_keywords
    )

@app.get("/")
async def root():
    """Root endpoint that provides basic API information"""
    return {"message": "Legal AI Benchmarking API is running. Visit /docs for documentation."}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Simple dashboard to visualize benchmark results"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

ab_test_service = ABTestService()

@app.post("/ab-test", response_model=ABTestResult)
async def run_ab_test(config: ABTestConfig, request: BenchmarkRequest):
    """
    Run an A/B test comparing different model configurations
    """
    if not request.question or len(request.question.strip()) < 5:
        raise HTTPException(status_code=400, detail="Question must contain at least 5 characters")
    
    return await ab_test_service.run_ab_test(
        config, 
        request.question, 
        request.expected_keywords or []
    )

@app.post("/batch-benchmark", response_model=List[BenchmarkResponse])
async def batch_benchmark(requests: List[BenchmarkRequest], save_to_csv: bool = False):
    """Process multiple benchmark requests in a single call"""
    results = []
    for request in requests:
        result = await benchmark(request, save_to_csv)
        results.append(result)
    return results

@app.get("/access-to-justice-demo", response_class=HTMLResponse)
async def access_to_justice_demo(request: Request):
    """Demo showing how AI models can help with common legal issues faced by underserved populations"""
    return templates.TemplateResponse("access_demo.html", {"request": request})