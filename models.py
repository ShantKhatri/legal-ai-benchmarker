from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class BenchmarkRequest(BaseModel):
    """
    Request model for the benchmark endpoint
    """
    question: str = Field(..., description="The legal question to benchmark models on")
    expected_keywords: Optional[List[str]] = Field(
        default=None, 
        description="Optional list of keywords expected in a good answer"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "question": "What is IPC 420?",
                "expected_keywords": ["cheating", "fraud", "dishonesty", "section 420", "imprisonment"]
            }
        }

class ModelEvaluation(BaseModel):
    """
    Evaluation results for a single model
    """
    model_name: str = Field(..., description="Name of the AI model")
    answer: str = Field(..., description="The model's answer to the question")
    keyword_coverage: float = Field(..., description="Percentage of expected keywords found in the answer")
    keywords_found: List[str] = Field(..., description="List of expected keywords found in the answer")
    length_category: str = Field(..., description="Assessment of answer length: 'too_short', 'good', or 'too_long'")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    confidence_score: float = Field(default=0.0, description="Confidence score based on answer characteristics (0-100)")
    metadata: Dict[str, Any] = Field(default={}, description="Additional model-specific metadata")
    social_impact_metrics: Optional[Dict[str, float]] = None

class BenchmarkResponse(BaseModel):
    """
    Response model for the benchmark endpoint
    """
    question: str = Field(..., description="The question that was benchmarked")
    models: List[ModelEvaluation] = Field(..., description="List of model evaluations")
    expected_keywords: Optional[List[str]] = Field(
        default=None, 
        description="Keywords that were expected in the answer"
    )

class ABTestConfig(BaseModel):
    """Configuration for A/B testing different model settings"""
    test_name: str = Field(..., description="Name for this A/B test")
    model_variants: List[Dict[str, Any]] = Field(..., description="List of model configurations to test")
    evaluation_criteria: List[str] = Field(..., description="Metrics to evaluate (e.g., response_time, keyword_match)")
    
class ABTestResult(BaseModel):
    """Results from an A/B test"""
    test_name: str = Field(..., description="Name of the test")
    variant_results: Dict[str, Dict[str, Any]] = Field(..., description="Results for each variant")
    winning_variant: str = Field(..., description="Name of the variant that performed best")
    performance_difference: float = Field(..., description="Performance difference vs. runner-up (percentage)")