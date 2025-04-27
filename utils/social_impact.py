"""
Utility functions for evaluating the social impact of legal AI models
in terms of access to justice metrics.
"""
import re
from textstat import flesch_reading_ease, syllable_count
from typing import Dict, Any

def calculate_simplicity_score(text: str) -> float:
    """
    Calculate how simple and accessible the language is.
    
    Returns a score between 0-100 where higher is more simple/accessible.
    """
    try:
        score = flesch_reading_ease(text)
        return min(100, max(0, score))
    except:
        words = text.split()
        if not words:
            return 0
            
        avg_word_length = sum(len(word) for word in words) / len(words)
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = sum(len(sentence.split()) for sentence in sentences if sentence) / max(1, len([s for s in sentences if s]))
        
        return max(0, min(100, 100 - (avg_word_length * 3 + avg_sentence_length * 0.8)))

def calculate_actionable_score(text: str) -> float:
    """
    Calculate how actionable the information is, based on presence of 
    procedural steps, concrete instructions, and action verbs.
    
    Returns a score between 0-100.
    """
    action_verbs = ["file", "submit", "apply", "complete", "contact", "visit", "call", 
                   "request", "fill", "sign", "pay", "go", "send", "obtain"]
    procedural_indicators = ["first", "second", "third", "finally", "next", "then", "step"]
    concrete_indicators = ["form", "document", "office", "court", "police", "fee", "deadline", 
                          "date", "number", "address", "website", "online"]
    
    text_lower = text.lower()
    
    action_score = sum(text_lower.count(verb) for verb in action_verbs) * 5
    procedural_score = sum(text_lower.count(indicator) for indicator in procedural_indicators) * 8
    concrete_score = sum(text_lower.count(indicator) for indicator in concrete_indicators) * 4

    total_score = action_score + procedural_score + concrete_score

    return min(100, total_score)

def calculate_cultural_relevance(text: str) -> float:
    """
    Evaluate cultural relevance through mention of Indian legal terms,
    local processes, and contextual appropriateness.
    
    Returns a score between 0-100.
    """
    indian_legal_terms = ["IPC", "CrPC", "Indian Penal Code", "panchayat", "lok adalat", 
                        "RTI", "Right to Information", "FIR", "PIL", "High Court", "Supreme Court"]

    text_lower = text.lower()
    relevance_score = sum(text_lower.count(term.lower()) for term in indian_legal_terms) * 10

    return min(100, relevance_score)

def calculate_accessibility_score(model_result) -> float:
    """
    Calculate overall accessibility based on multiple factors
    including response time and other metrics.
    
    Returns a score between 0-100.
    """
    response_time_ms = getattr(model_result, 'response_time_ms', 5000) 
    time_factor = max(0, 100 - (response_time_ms / 100))

    answer_length = len(getattr(model_result, 'answer', ''))
    if answer_length < 50:
        length_factor = answer_length * 2
    elif answer_length > 1000:
        length_factor = max(0, 100 - ((answer_length - 1000) / 20))
    else:
        length_factor = 100

    return (time_factor * 0.3) + (length_factor * 0.7)

def evaluate_social_impact(model_results) -> Dict[str, float]:
    """
    Evaluate models based on factors relevant to access to justice
    
    Args:
        model_results: The model evaluation results containing the answer
        
    Returns:
        Dictionary with social impact metrics
    """
    metrics = {
        "language_simplicity": calculate_simplicity_score(model_results.answer),
        "actionable_guidance": calculate_actionable_score(model_results.answer),
        "cultural_relevance": calculate_cultural_relevance(model_results.answer),
        "accessibility": calculate_accessibility_score(model_results)
    }

    metrics["overall_social_impact"] = (
        metrics["language_simplicity"] * 0.3 +
        metrics["actionable_guidance"] * 0.4 +
        metrics["cultural_relevance"] * 0.2 +
        metrics["accessibility"] * 0.1
    )
    
    return metrics