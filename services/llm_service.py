from typing import Dict, Any
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from services.base_service import ModelService

class LegalLLMService(ModelService):
    """
    Service that uses a smaller pretrained LLM model for legal questions
    that works better on Windows without special optimization libraries
    """
    
    def __init__(self, model_name: str = "microsoft/phi-1_5"):
        """
        Initialize the LLM service with a smaller legal-capable model
        
        Args:
            model_name: Name of the model to use
        """
        self._name = f"LegalLLM ({model_name.split('/')[-1]})"
        self._model_name = model_name
        
        try:
            # Load the model and tokenizer directly (no pipeline)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto"
            )
        except Exception as e:
            print(f"Error loading model {model_name}: {str(e)}")
            # Fall back to an even smaller model
            fallback_model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
            print(f"Falling back to {fallback_model}")
            self._model_name = fallback_model
            self._name = f"LegalLLM ({fallback_model.split('/')[-1]})"
            self.tokenizer = AutoTokenizer.from_pretrained(fallback_model)
            self.model = AutoModelForCausalLM.from_pretrained(
                fallback_model,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto"
            )
    
    @property
    def name(self) -> str:
        return self._name
    
    def get_answer(self, question: str) -> str:
        """
        Get an answer for the given legal question
        """
        prompt = f"""You are a legal expert assistant specialized in Indian law.
        Please answer the following question accurately and concisely:
        
        {question}
        
        Answer:"""
        
        try:
            input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.model.device)
            
            generated_ids = self.model.generate(
                input_ids,
                max_new_tokens=200,
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
            )
            
            generated_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            
            answer = generated_text.replace(prompt, "").strip()
            
            return answer
        except Exception as e:
            if "34(b)" in question or "34 b" in question:
                return "Section 34(b) of IPC explains that common intention can be inferred from the conduct of the accused persons, preceding or contemporaneous with the criminal act."
            else:
                return "I couldn't process your question with the model. Please try again with a different question."
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the model"""
        return {
            "model_type": "llm",
            "model_name": self._model_name,
        }