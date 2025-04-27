import csv
import os
from datetime import datetime
from typing import List, Optional

from models import ModelEvaluation

def log_benchmark_to_csv(
    question: str, 
    evaluations: List[ModelEvaluation], 
    expected_keywords: Optional[List[str]] = None
):
    """
    Log benchmark results to a CSV file for future analysis and model improvement
    
    Args:
        question: The benchmarked question
        evaluations: List of model evaluation results
        expected_keywords: Optional list of expected keywords
    """
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    csv_path = os.path.join(logs_dir, "benchmark_logs.csv")
    file_exists = os.path.isfile(csv_path)
    
    keywords_str = ",".join(expected_keywords) if expected_keywords else ""

    timestamp = datetime.now().isoformat()

    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                'timestamp', 'question', 'expected_keywords',
                'model_name', 'answer', 'keyword_coverage',
                'keywords_found', 'length_category', 'response_time_ms'
            ])

        for eval in evaluations:
            writer.writerow([
                timestamp,
                question,
                keywords_str,
                eval.model_name,
                eval.answer,
                f"{eval.keyword_coverage:.2f}%",
                ",".join(eval.keywords_found),
                eval.length_category,
                eval.response_time_ms
            ])