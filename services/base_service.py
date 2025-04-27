from abc import ABC, abstractmethod
from typing import Dict, Any
from utils.cache import get_cached_response

class ModelService(ABC):
    """
    Abstract base class for all model services
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Model service name"""
        pass
    
    @abstractmethod
    def get_answer(self, question: str) -> str:
        """
        Get an answer for the given question
        
        Args:
            question: The question to answer
            
        Returns:
            The model's answer as a string
        """
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get additional metadata about the model
        
        Returns:
            Dictionary of model metadata
        """
        return {}
    
    def get_response(self, question: str) -> str:
        """Get response from model with caching"""
        # Try to get from cache first
        cached_result = get_cached_response(self._name, question)
        if cached_result is not None:
            return cached_result
            
        # If not in cache, get from model and store in cache
        response = self._get_model_response(question)
        get_cached_response.cache_clear()  # Need to clear to update
        get_cached_response(self._name, question)  # Store in cache
        return response
    
    def _get_model_response(self, question: str) -> str:
        """Internal method to be implemented by subclasses"""
        raise NotImplementedError