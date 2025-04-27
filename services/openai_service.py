import openai
import os
from typing import Dict, Any

from services.base_service import ModelService

class OpenAIService(ModelService):
    """
    Service for OpenAI models
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the OpenAI model service
        
        Args:
            model_name: Name of the OpenAI model to use
        """
        self._name = f"OpenAI ({model_name})"
        self._model_name = model_name
        
        # Check if API key is available
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        
        openai.api_key = api_key
    
    @property
    def name(self) -> str:
        return self._name
    
    def get_answer(self, question: str) -> str:
        """
        Get an answer for the given question using OpenAI
        """
        try:
            response = openai.ChatCompletion.create(
                model=self._model_name,
                messages=[
                    {"role": "system", "content": "You are a legal expert assistant. Provide accurate, concise answers to questions about legal topics."},
                    {"role": "user", "content": question}
                ],
                temperature=0,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error getting answer from OpenAI: {str(e)}"
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the OpenAI model"""
        return {
            "model_type": "openai",
            "model_name": self._model_name,
        }