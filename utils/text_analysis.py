from typing import List, Tuple, Optional
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

def calculate_keyword_coverage(text: str, keywords: List[str]) -> Tuple[float, List[str]]:
    """
    Calculate what percentage of expected keywords are found in the text
    
    Args:
        text: The text to analyze
        keywords: List of keywords to look for
        
    Returns:
        Tuple of (coverage percentage, list of found keywords)
    """
    if not keywords:
        return 0.0, []
    
    text_lower = text.lower()
    found_keywords = []
    
    for keyword in keywords:
        # Look for the keyword in the text
        if keyword.lower() in text_lower:
            found_keywords.append(keyword)
    
    coverage = len(found_keywords) / len(keywords) * 100
    return coverage, found_keywords

def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """
    Extract potential keywords from text using simple NLP techniques
    
    Args:
        text: Text to extract keywords from
        max_keywords: Maximum number of keywords to extract
        
    Returns:
        List of potential keywords
    """
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())

    filtered_words = [w for w in word_tokens if w.isalnum() and w not in stop_words]

    word_freq = {}
    for word in filtered_words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [word for word, freq in sorted_words[:max_keywords]]
    
    return keywords

def assess_length(text: str) -> str:
    """
    Assess whether an answer is too short, too long, or good length
    
    Args:
        text: The text to assess
        
    Returns:
        Category as string: 'too_short', 'good', or 'too_long'
    """
    word_count = len(text.split())
    
    if word_count < 20:
        return "too_short"
    elif word_count > 300:
        return "too_long"
    else:
        return "good"
    
def calculate_confidence_score(answer: str) -> float:
    """
    Calculate a confidence score based on answer characteristics:
    - Presence of uncertainty phrases ("might be", "possibly")
    - Number of specifics/details provided
    - Presence of legal citations
    """
    uncertainty_phrases = ["may", "might", "possibly", "perhaps", "could be"]
    
    # Lower score for uncertain answers
    uncertainty_score = sum(phrase in answer.lower() for phrase in uncertainty_phrases)
    
    # Higher score for specific details
    detail_score = len(re.findall(r'\d+', answer))  # Count numbers as details
    
    # Higher score for legal citations
    citation_score = len(re.findall(r'section \d+|article \d+', answer.lower()))
    
    # Calculate final score (0-100)
    confidence = 50 - (uncertainty_score * 10) + (detail_score * 5) + (citation_score * 15)
    
    # Clamp between 0-100
    return max(0, min(100, confidence))