# Legal AI Model Benchmarker

A comprehensive platform for benchmarking AI models on legal question answering tasks, with special emphasis on access to justice metrics. This tool evaluates models based on keyword coverage, response time, and social impact indicators to help identify the most effective AI solutions for legal assistance.

## 🌟 Features

- **Multi-model Benchmarking**: Compare responses from different AI models side-by-side
- **Social Impact Analysis**: Measure access to justice metrics like language simplicity and actionable guidance
- **Performance Metrics**: Track keyword coverage, response time, and confidence scores
- **Interactive Dashboard**: Visualize benchmark results with charts and detailed comparisons
- **Flexible Model Integration**: Support for OpenAI, Hugging Face, and custom legal LLM models
- **Parallel Processing**: Efficient handling of multiple model evaluations
- **A/B Testing**: Compare different model configurations systematically
- **Batch Processing**: Run benchmarks on multiple questions simultaneously

## 💻 Architecture Overview

The system consists of several key components:

- **Model Services**: Standardized interface for different AI providers
  - `HuggingFaceService`: For transformer-based QA models
  - `OpenAIService`: For GPT models via API
  - `LegalLLMService`: For specialized legal language models
  - `SimplifiedModelService`: Rule-based fallback solution
- **Benchmark Engine**: Core evaluation system
  - Parallel and sequential benchmarking
  - Keyword coverage assessment
  - Response time measurement
  - Social impact evaluation
- **Dashboard**: Interactive visualization of results
  - Response time comparisons
  - Keyword coverage metrics
  - Social impact radar charts
  - Individual model responses
- **Utilities**:
  - Text analysis tools
  - Result logging
  - Response caching
  - Social impact metrics calculation

## 📋 API Reference

### Benchmark Endpoint

**POST** `/benchmark`

Compares multiple AI models on a legal question.

**Request Format:**

```json
{
  "question": "What is IPC 420?",
  "expected_keywords": ["cheating", "fraud", "dishonesty", "imprisonment"]
}
```

**Response Format:**

```json
{
  "question": "What is IPC 420?",
  "models": [
    {
      "model_name": "HuggingFace (roberta-base-squad2)",
      "answer": "Section 420 of the Indian Penal Code deals with cheating and dishonestly inducing delivery of property.",
      "keyword_coverage": 75.0,
      "keywords_found": ["cheating", "dishonesty", "section 420"],
      "length_category": "good",
      "response_time_ms": 1243,
      "social_impact_metrics": {
        "language_simplicity": 65.8,
        "actionable_guidance": 35.0,
        "cultural_relevance": 80.0,
        "accessibility": 72.5,
        "overall_social_impact": 58.7
      },
      "metadata": {
        "model_type": "huggingface",
        "model_name": "deepset/roberta-base-squad2"
      }
    },
    {
      "model_name": "OpenAI (gpt-3.5-turbo)",
      "answer": "IPC 420 is a section of the Indian Penal Code that deals with the offense of cheating and dishonestly inducing delivery of property. It prescribes punishment of imprisonment up to 7 years and a fine for those convicted of fraud under this section.",
      "keyword_coverage": 100.0,
      "keywords_found": ["cheating", "fraud", "dishonesty", "imprisonment"],
      "length_category": "good",
      "response_time_ms": 872,
      "social_impact_metrics": {
        "language_simplicity": 72.4,
        "actionable_guidance": 45.0,
        "cultural_relevance": 90.0,
        "accessibility": 78.5,
        "overall_social_impact": 67.3
      },
      "metadata": {
        "model_type": "openai",
        "model_name": "gpt-3.5-turbo"
      }
    }
  ],
  "expected_keywords": ["cheating", "fraud", "dishonesty", "imprisonment"]
}
```

### A/B Test Endpoint

**POST** `/ab-test`

Performs A/B testing on different model configurations.

### Batch Benchmark Endpoint

**POST** `/batch-benchmark`

Processes multiple benchmark requests in a single call.

### Dashboard

**GET** `/dashboard`

Interactive visualization of benchmark results.

### Access to Justice Demo

**GET** `/access-to-justice-demo`

Demo focused on access to justice use cases.

## 🚀 Setup & Installation

### Prerequisites

- Python 3.9+
- [Optional] CUDA-compatible GPU for faster inference

### Method 1: Direct Python Installation

Clone this repository:

```bash
git clone https://github.com/shantkhatri/legal-ai-benchmarker.git
cd legal-ai-benchmarker
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up environment variables for OpenAI:

On Windows Command Prompt:
```bash
set OPENAI_API_KEY=your_openai_api_key_here
```

On Windows PowerShell:
```bash
$env:OPENAI_API_KEY="your_openai_api_key_here"
```

On Linux/macOS:
```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

Alternatively, create a `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

Run the application:

```bash
uvicorn main:app --reload
```

Access the application:

- Dashboard: [http://localhost:8000/dashboard](http://localhost:8000/dashboard)
- API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

### Method 2: Using Docker

1. Create a `.env` file with your OpenAI API key.
```bash
OPENAI_API_KEY=your_openai_api_key_here
```


2. Build the Docker image:
```bash
docker build -t legal-ai-benchmarker .
```

3. Run the container:
```bash
docker run --env-file .env -p 8000:8000 legal-ai-benchmarker
```


Access at: [http://localhost:8000](http://localhost:8000)

## 🔧 Configuration Options

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `MODEL_CACHE_SIZE`: Max model responses to cache (default: 100)
- `LOG_TO_CSV`: Log results to CSV (default: false)

### Model Configuration

- HuggingFace Models:
  - Default: `deepset/roberta-base-squad2`
- OpenAI Models:
  - Default: `gpt-3.5-turbo`
- Legal LLM Models:
  - Default: `microsoft/phi-1_5`
- Simplified Model:
  - Rule-based fallback for common legal questions

## 📊 Social Impact Metrics

- **Language Simplicity**:
    - Measures how accessible the language is
    - Based on reading ease scores and sentence complexity
    - Higher scores indicate more accessible language 
- **Actionable Guidance**:
    - Evaluates how practical and useful the information is
    - Detects procedural steps and concrete actions
    - Higher scores indicate more actionable advice
- **Cultural Relevance**:
    - Assesses how well the response relates to Indian legal context
    - Recognizes mentions of relevant legal terms and concepts
    - Higher scores indicate better cultural/contextual fit
- **Accessibility**:
    - Considers factors like response time and answer length
    - Optimizes for content that loads quickly and is digestible
    - Higher scores indicate more accessible content

## 🔍 Running Tests

Run all tests:

```bash
pytest
```

Run a specific test:

```bash
pytest test_app.py::test_benchmark_valid_request
```

## 💻 Tech Stack

- FastAPI
- Hugging Face Transformers
- PyTorch
- NLTK
- Chart.js & ApexCharts
- Pydantic
- Jinja2
- Python 3.9+
- Docker
- Pytest

## 🧹 Project Structure

```
LegalAIModelBenchmarker/
├── main.py                 # FastAPI application entry point
├── models.py               # Pydantic data models
├── benchmarker.py          # Core benchmarking logic
├── parallel_benchmarker.py # Async benchmarking
├── requirements.txt        # Dependencies
├── templates/              # Dashboard templates
│   └── dashboard.html
├── services/               # Model services
│   ├── base_service.py
│   ├── huggingface_service.py
│   ├── openai_service.py
│   ├── llm_service.py
│   ├── simplified_service.py
│   └── ab_test_service.py
├── utils/                  # Utility scripts
│   ├── text_analysis.py
│   ├── social_impact.py
│   ├── cache.py
│   └── csv_logger.py
└── test/                   # Tests
    └── test_app.py
```

## ⚙️ Code Examples

### Benchmarking a Question with cURL

```bash
curl -X POST http://localhost:8000/benchmark \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are my rights as a tenant?",
    "expected_keywords": ["rent", "eviction", "notice", "deposit", "maintenance"]
  }'
```

### Accessing the Dashboard

Navigate to:

[http://localhost:8000/dashboard](http://localhost:8000/dashboard)

### Running a Batch Benchmark

```bash
curl -X POST http://localhost:8000/batch-benchmark \
  -H "Content-Type: application/json" \
  -d '[
    {"question": "What is IPC 420?", "expected_keywords": ["cheating", "fraud"]},
    {"question": "How do I file an RTI application?", "expected_keywords": ["form", "fee", "public information officer"]}
  ]'
```

## 📊 Future Improvements

1. Enhanced Benchmarking Metrics:
    - Add semantic similarity scoring to evaluate answers beyond keyword matching
    - Implement factual accuracy checking against authoritative legal sources
    - Add support for named entity recognition accuracy for legal entities
    - Develop specialized metrics for different legal domains (criminal, civil, etc.)

2. Additional Models:
    - Support for other model providers (Azure, Anthropic, Claude, etc.)
    - Fine-tuned legal domain models on Indian law
    - Multilingual models to support regional Indian languages
    - Domain-specific legal expert models

3. Advanced Dashboard Features:
    - Historical benchmark comparison across multiple runs
    - Advanced filtering and sorting of results
    - Export functionality for reports
    - Customizable visualization preferences
    - User annotation capabilities for model responses

4. Extended Features:
    - Authentication and user management for API access
    - Webhook notifications for benchmark completion
    - Support for more complex legal queries with context
    - Integration with legal databases for validation
    - Automated report generation

5. Infrastructure:
    - CI/CD pipeline for automated testing and deployment
    - Load balancing for high-throughput benchmarking
    - Database integration for persistent results storage
    - Horizontal scaling for benchmarking large model sets
    - Performance optimization for mobile devices


## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (git checkout -b feature/work-feature)
3. Commit your changes (git commit -m 'Add some work feature')
4. Push to the branch (git push origin feature/work-feature)
5. Open a Pull Request


## 🔍 Troubleshooting
Common Issues
1. **OpenAI API errors**:
    - Ensure your API key is set correctly in the environment
    - Check your API usage limits and billing status
2. **"NumPy is not available" error**:
    - Downgrade to numpy 1.24.3 (pip install numpy==1.24.3)
    - This is a known compatibility issue with transformers
3. **GPU memory errors**:
    - Try setting device_map="cpu" in the model services
    - Or reduce model size by using quantization
4. **Long load times for first request**:
    - This is normal as models are loaded into memory
    - Subsequent requests will be much faster


## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact
For questions or support, please open an issue on the GitHub repository.#   l e g a l - a i - b e n c h m a r k e r  
 