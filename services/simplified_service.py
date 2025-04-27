from typing import Dict, Any
import re
from services.base_service import ModelService

class SimplifiedModelService(ModelService):
    """A simplified model service that doesn't rely on external ML libraries"""
    
    def __init__(self):
        self._name = "Simplified Legal Model"
        self._legal_knowledge = {
            "34": """Section 34 of IPC deals with "Acts done by several persons in furtherance of common intention".
                  When a criminal act is done by several persons in furtherance of the common intention of all,
                  each person is liable for that act in the same manner as if it was done by them alone.
                  Subsection (b) specifically explains that common intention can be inferred from the conduct
                  of the accused persons, preceding or contemporaneous with the criminal act.""",
                  
            "420": """Section 420 of IPC deals with "Cheating and dishonestly inducing delivery of property".
                   It states that whoever cheats and thereby dishonestly induces the person deceived to deliver any property
                   shall be punished with imprisonment which may extend to seven years, and shall also be liable to fine.""",
                   
            "302": """Section 302 of IPC deals with punishment for murder. It states that whoever commits murder 
                   shall be punished with death, or imprisonment for life, and shall also be liable to fine.""",
                   
            "376": """Section 376 of IPC deals with punishment for sexual assault, which can extend to life imprisonment."""
        }
    
    @property
    def name(self) -> str:
        return self._name
    
    def get_answer(self, question: str) -> str:
        """Generate answer based on pattern matching and knowledge base"""
        question_lower = question.lower()
        
        # Handle section 34(b) specifically
        if "34(b)" in question_lower or "34 b" in question_lower:
            return ("Section 34(b) of IPC explains that common intention can be inferred from the conduct "
                   "of the accused persons, preceding or contemporaneous with the criminal act.")
        
        # Extract section numbers from question
        section_pattern = r'(?:section|sec)\s*(\d+)|(?:ipc|indian penal code)\s*(\d+)'
        matches = re.finditer(section_pattern, question_lower)
        
        for match in matches:
            section = match.group(1) if match.group(1) else match.group(2)
            if section in self._legal_knowledge:
                return self._legal_knowledge[section]
        
        # If no specific section found, try to give a general answer based on keywords
        if "murder" in question_lower:
            return self._legal_knowledge["302"]
        elif "cheating" in question_lower or "fraud" in question_lower:
            return self._legal_knowledge["420"]
        elif "rape" in question_lower or "sexual" in question_lower:
            return self._legal_knowledge["376"]
        elif "common intention" in question_lower:
            return self._legal_knowledge["34"]
        
        return ("I don't have specific information about this legal question. "
                "Please ask about a specific section of the Indian Penal Code.")
    
    def get_metadata(self) -> Dict[str, Any]:
        return {"model_type": "simplified", "version": "1.0"}