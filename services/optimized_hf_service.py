from transformers import pipeline
import torch
from typing import Dict, Any

from services.base_service import ModelService

class OptimizedHuggingFaceService(ModelService):
    """
    Service for optimized Hugging Face question-answering models using quantization
    """
    
    def __init__(self, model_name: str = "deepset/roberta-base-squad2"):
        """
        Initialize the optimized Hugging Face model service with quantization
        
        Args:
            model_name: Name of the Hugging Face model to use
        """
        self._name = f"OptimizedHF ({model_name.split('/')[-1]})"
        self._model_name = model_name
        
        # Initialize quantized model
        self._qa_pipeline = pipeline(
            "question-answering",
            model=model_name,
            tokenizer=model_name,
            device_map="auto",
            torch_dtype=torch.float16  # Use half-precision
        )
    
    @property
    def name(self) -> str:
        return self._name
    
    def get_answer(self, question: str) -> str:
        """
        Get an answer for the given question using optimized Hugging Face model
        """
        # For legal questions, we'll create a minimal context
        context = (
            f"This is a legal question about: {question} "
            "The Indian Penal Code (IPC) is the official criminal code of India. "
            "It covers all substantive aspects of criminal law. "
            "Section 420 in The Indian Penal Code deals with Cheating and dishonestly "
            "inducing delivery of property."
        )
        
        result = self._qa_pipeline(
            question=question,
            context=context
        )
        
        return result['answer']
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the Hugging Face model"""
        return {
            "model_type": "optimized_huggingface",
            "model_name": self._model_name,
            "quantization": "float16"
        }