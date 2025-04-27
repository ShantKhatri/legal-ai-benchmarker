import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
import time

from models import ModelEvaluation
from services.base_service import ModelService
from utils.text_analysis import calculate_keyword_coverage, assess_length, calculate_confidence_score
from utils.social_impact import evaluate_social_impact

async def benchmark_models_parallel(
    question: str, 
    models: List[ModelService],
    expected_keywords: Optional[List[str]] = None
) -> List[ModelEvaluation]:
    """
    Benchmark multiple models in parallel on a given question.
    
    Args:
        question: The question to answer
        models: List of model services to benchmark
        expected_keywords: Optional list of keywords expected in good answers
        
    Returns:
        List of model evaluations
    """
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        tasks = [
            loop.run_in_executor(
                executor,
                lambda m=model: benchmark_single_model(question, m, expected_keywords)
            )
            for model in models
        ]
        results = await asyncio.gather(*tasks)
    return results

def benchmark_single_model(
    question: str, 
    model: ModelService,
    expected_keywords: Optional[List[str]] = None
) -> ModelEvaluation:
    """
    Benchmark a single model on a question
    
    Args:
        question: The question to answer
        model: Model service to benchmark
        expected_keywords: Optional list of keywords expected in good answers
        
    Returns:
        Model evaluation
    """
    normalized_keywords = [k.lower() for k in expected_keywords] if expected_keywords else []
    
    start_time = time.time()
    answer = model.get_answer(question)
    end_time = time.time()
    response_time_ms = int((end_time - start_time) * 1000)
    
    if normalized_keywords:
        keyword_coverage, keywords_found = calculate_keyword_coverage(answer, normalized_keywords)
    else:
        from utils.text_analysis import extract_keywords
        potential_keywords = extract_keywords(question)
        keyword_coverage, keywords_found = calculate_keyword_coverage(answer, potential_keywords)
    
    length_category = assess_length(answer)
    
    confidence_score = calculate_confidence_score(answer)
    
    result = ModelEvaluation(
        model_name=model.name,
        answer=answer,
        keyword_coverage=keyword_coverage,
        keywords_found=keywords_found,
        length_category=length_category,
        response_time_ms=response_time_ms,
        confidence_score=confidence_score,
        metadata=model.get_metadata()
    )
    
    result.social_impact_metrics = evaluate_social_impact(result)
    
    return result