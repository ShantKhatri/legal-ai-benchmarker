from typing import List, Dict, Any
from models import ABTestConfig, ABTestResult, BenchmarkRequest
from services.huggingface_service import HuggingFaceService
from services.openai_service import OpenAIService
from parallel_benchmarker import benchmark_single_model

class ABTestService:
    def __init__(self):
        pass
    
    async def run_ab_test(self, config: ABTestConfig, question: str, expected_keywords: List[str]) -> ABTestResult:
        """Run an A/B test comparing multiple model variants"""
        variant_results = {}
        
        # Test each variant
        for variant in config.model_variants:
            variant_name = variant.get("name", "Unnamed variant")
            model = self._create_model_from_config(variant)
            benchmark_result = benchmark_single_model(question, model, expected_keywords)
            
            # Collect metrics we care about
            metrics = {}
            for criterion in config.evaluation_criteria:
                if criterion == "response_time":
                    metrics["response_time"] = benchmark_result.response_time_ms
                elif criterion == "keyword_match":
                    metrics["keyword_match"] = benchmark_result.keyword_coverage
                elif criterion == "confidence":
                    metrics["confidence"] = benchmark_result.confidence_score
                    
            variant_results[variant_name] = {
                "benchmark_result": benchmark_result,
                "metrics": metrics
            }
        
        # Determine winner based on primary metric (first in evaluation_criteria)
        primary_metric = config.evaluation_criteria[0]
        winning_variant = max(
            variant_results.keys(),
            key=lambda k: variant_results[k]["metrics"].get(primary_metric, 0)
        )
        
        # Calculate performance difference
        variants = list(variant_results.keys())
        if len(variants) >= 2:
            winner_value = variant_results[winning_variant]["metrics"].get(primary_metric, 0)
            runner_up = max(
                [v for v in variants if v != winning_variant],
                key=lambda k: variant_results[k]["metrics"].get(primary_metric, 0)
            )
            runner_up_value = variant_results[runner_up]["metrics"].get(primary_metric, 0)
            
            if runner_up_value > 0:
                performance_difference = (winner_value - runner_up_value) / runner_up_value * 100
            else:
                performance_difference = 100.0
        else:
            performance_difference = 0.0
        
        return ABTestResult(
            test_name=config.test_name,
            variant_results=variant_results,
            winning_variant=winning_variant,
            performance_difference=performance_difference
        )
    
    def _create_model_from_config(self, config: Dict[str, Any]):
        """Create model instance based on configuration"""
        model_type = config.get("type", "")
        
        if model_type == "openai":
            return OpenAIService(
                model_name=config.get("model_name", "gpt-3.5-turbo")
            )
        elif model_type == "huggingface":
            return HuggingFaceService(
                model_name=config.get("model_name", "deepset/roberta-base-squad2")
            )
        
        raise ValueError(f"Unsupported model type: {model_type}")