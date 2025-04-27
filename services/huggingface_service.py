from transformers import pipeline
from typing import Dict, Any
import os

from services.base_service import ModelService

class HuggingFaceService(ModelService):
    """
    Service for Hugging Face question-answering models
    """
    
    def __init__(self, model_name: str = "deepset/roberta-base-squad2"):
        """
        Initialize the Hugging Face model service
        
        Args:
            model_name: Name of the Hugging Face model to use
        """
        self._name = f"HuggingFace ({model_name.split('/')[-1]})"
        self._model_name = model_name
        
        # Initialize the model
        self._qa_pipeline = pipeline(
            "question-answering",
            model=model_name,
            tokenizer=model_name
        )
    
    @property
    def name(self) -> str:
        return self._name
    
    def get_answer(self, question: str) -> str:
        """
        Get an answer for the given question using Hugging Face
        
        For QA models, we need context. Since we don't have specific context,
        we'll use the question itself as minimal context.
        """
        # For legal questions, we'll create a minimal context from the question
        # In a real-world scenario, you'd provide actual legal context
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
            "model_type": "huggingface",
            "model_name": self._model_name,
        }