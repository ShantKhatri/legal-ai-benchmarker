from functools import lru_cache
from typing import Dict, Tuple

# Simple in-memory cache with LRU (Least Recently Used) strategy
@lru_cache(maxsize=100)
def get_cached_response(model_name: str, question: str) -> str:
    """Cache decorator for model responses"""
    pass 