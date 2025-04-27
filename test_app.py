import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns expected message"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "running" in response.json()["message"]

def test_benchmark_valid_request():
    """Test the benchmark endpoint with a valid request"""
    response = client.post(
        "/benchmark",
        json={
            "question": "What is IPC 420?",
            "expected_keywords": ["cheating", "fraud", "dishonesty"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "question" in data
    assert "models" in data
    assert len(data["models"]) >= 1
    
    # Check model evaluation fields
    model = data["models"][0]
    assert "model_name" in model
    assert "answer" in model
    assert "keyword_coverage" in model
    assert "keywords_found" in model
    assert "length_category" in model
    assert "response_time_ms" in model

def test_benchmark_empty_question():
    """Test the benchmark endpoint with an empty question"""
    response = client.post(
        "/benchmark",
        json={
            "question": "",
            "expected_keywords": ["cheating", "fraud"]
        }
    )
    assert response.status_code == 400
    assert "detail" in response.json()

def test_benchmark_short_question():
    """Test the benchmark endpoint with a too short question"""
    response = client.post(
        "/benchmark",
        json={
            "question": "Hi",
            "expected_keywords": ["cheating", "fraud"]
        }
    )
    assert response.status_code == 400
    assert "detail" in response.json()

def test_benchmark_no_keywords():
    """Test the benchmark endpoint without providing keywords"""
    response = client.post(
        "/benchmark",
        json={
            "question": "What is the punishment for theft under IPC?"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "question" in data
    assert "models" in data
    assert len(data["models"]) >= 1

def test_benchmark_invalid_json():
    """Test the benchmark endpoint with invalid JSON"""
    response = client.post(
        "/benchmark",
        data="This is not JSON"
    )
    assert response.status_code == 422