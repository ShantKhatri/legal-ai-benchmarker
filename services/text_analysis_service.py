import re
from typing import List, Dict, Any

class TextAnalysisService:
    def __init__(self):
        # Initialize sentence transformer if available
        try:
            from sentence_transformers import SentenceTransformer
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.semantic_similarity_available = True
        except ImportError:
            self.semantic_similarity_available = False
    
    def semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        if not self.semantic_similarity_available:
            return 0.0
            
        embeddings = self.sentence_model.encode([text1, text2])
        similarity = embeddings[0] @ embeddings[1].T  # Cosine similarity
        return float(similarity)
    
    def extract_citations(self, text: str) -> List[str]:
        """Extract legal citations from text"""
        # Pattern for common legal citations
        patterns = [
            r'\b\d+\s+U\.S\.\s+\d+\b',
            r'\b\d+\s+S\.\s*Ct\.\s+\d+\b',
            r'\b\d+\s+F\.\s*\d+d\s+\d+\b',
            r'section\s+\d+(\(\w+\))?',
            r'article\s+\d+(\(\w+\))?',
        ]
        
        citations = []
        for pattern in patterns:
            citations.extend(re.findall(pattern, text, re.IGNORECASE))
        
        return citations
    
    def detect_hallucinations(self, text: str) -> Dict[str, Any]:
        """Detect potential hallucinations in legal text"""
        # Look for indicators of potentially made-up information
        indicators = {
            "uncertain_language": ["possibly", "maybe", "might be", "could be", "I think", "I believe"],
            "non_existent_patterns": ["Code Section 999999", "Imaginary Act of"],
            "excessive_specificity": []  # Would need more context-specific rules
        }
        
        results = {
            "contains_hallucination_indicators": False,
            "hallucination_score": 0.0,
            "flagged_segments": []
        }
        
        # Check for uncertain language
        uncertainty_count = 0
        for phrase in indicators["uncertain_language"]:
            if phrase.lower() in text.lower():
                uncertainty_count += 1
                results["flagged_segments"].append(f"Uncertainty phrase: {phrase}")
        
        # Check for non-existent patterns
        for pattern in indicators["non_existent_patterns"]:
            if pattern.lower() in text.lower():
                results["contains_hallucination_indicators"] = True
                results["flagged_segments"].append(f"Likely non-existent reference: {pattern}")
        
        # Calculate hallucination score (0-100)
        results["hallucination_score"] = min(100, uncertainty_count * 20)
        if results["hallucination_score"] > 30:
            results["contains_hallucination_indicators"] = True
        
        return results