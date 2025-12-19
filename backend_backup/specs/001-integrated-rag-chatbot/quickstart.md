# Quickstart Guide: Integrated RAG Chatbot

## Prerequisites

- Python 3.11+
- Git
- Access to Cohere API (with provided API key)
- Access to Qdrant Cloud (with provided URL and API key)
- Access to Neon Serverless Postgres (with provided connection URL)

## Setup

### 1. Clone and Navigate to Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with the following:

```env
COHERE_API_KEY=WbAwWzUs98w1sDr3hNaDhdN2htTfUiQMe5CcSyte
QDRANT_URL=https://705a8158-d445-4c4c-87db-3abf3671d5a3.eu-west-1-0.aws.cloud.qdrant.io
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.p4D3J25bPykUKU7DGQFHsusYNRTQ4KCRiF9ep64zUp8
NEON_DB_URL=postgresql://neondb_owner:npg_IHZt5iGNgSE4@ep-wild-tooth-ahsd5q00-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
API_KEY=your_secret_api_key_here
```

**Note**: Use the exact credentials provided in the specification for development.

### 5. Run the Application

```bash
cd backend
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

## Basic Usage

### 1. Upload a Book

Upload a PDF, HTML, or text file for processing:

```bash
curl -X POST "http://localhost:8000/ingest/upload" \
  -H "Authorization: Bearer your_secret_api_key_here" \
  -F "file=@path/to/your/book.pdf" \
  -F "title=My Book Title"
```

### 2. Check Processing Status

```bash
curl -X GET "http://localhost:8000/ingest/status/{book_id}" \
  -H "Authorization: Bearer your_secret_api_key_here"
```

### 3. Query Full Book Content

After the book is processed (status is READY):

```bash
curl -X POST "http://localhost:8000/query/full" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_secret_api_key_here" \
  -d '{
    "book_id": "your-book-uuid",
    "query": "What is the main theme of this book?"
  }'
```

### 4. Query Selected Text

Query using only specific text without referencing other parts of the book:

```bash
curl -X POST "http://localhost:8000/query/selected" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_secret_api_key_here" \
  -d '{
    "selected_text": "The specific text passage selected by the user",
    "query": "What does this passage mean?"
  }'
```

### 5. Check Usage Metrics

Monitor your usage of Qdrant Cloud, Neon, and Cohere to stay within free-tier limits:

```bash
curl -X GET "http://localhost:8000/monitor/usage" \
  -H "Authorization: Bearer your_secret_api_key_here"
```

## Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

## Monitoring Script

A monitoring script is available to track your usage of Qdrant Cloud and Neon Serverless Postgres:

```bash
python scripts/monitor_usage.py
```

This script will report current usage against free-tier limits and provide recommendations to optimize resource usage.