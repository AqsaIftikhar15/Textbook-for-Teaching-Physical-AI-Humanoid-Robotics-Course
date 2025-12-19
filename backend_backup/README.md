# Integrated RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions based on full book content or user-selected text passages. The system uses Cohere for embeddings and generation, Qdrant for vector storage, and Neon Postgres for metadata management.

## Architecture

The application follows a service-oriented architecture with the following components:

- **Models**: Pydantic models for data validation
- **Services**: Business logic for ingestion, embedding, storage, and RAG operations
- **API Routes**: FastAPI endpoints for ingestion, querying, and monitoring
- **Middleware**: Authentication and other cross-cutting concerns
- **Configuration**: Settings management via pydantic-settings

## Prerequisites

- Python 3.11+
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
cd backend_backup
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
cd backend_backup
python -m pytest tests/ -v
```

## Monitoring Script

A monitoring script is available to track your usage of Qdrant Cloud and Neon Serverless Postgres:

```bash
python scripts/monitor_usage.py
```

This script will report current usage against free-tier limits and provide recommendations to optimize resource usage.

## API Documentation

The API includes comprehensive documentation available at `http://localhost:8000/docs` when the service is running. This includes:

- Detailed endpoint descriptions
- Request/response schemas
- Example requests
- Authentication requirements

## Troubleshooting

### Common Issues:

1. **API Key Authentication Failure**: Ensure the Authorization header is in the format `Bearer your_api_key`
2. **Qdrant Connection Issues**: Verify the QDRANT_URL and QDRANT_API_KEY in your .env file
3. **Database Connection Issues**: Check the NEON_DB_URL in your .env file
4. **File Upload Size Limits**: Default max file size is 50MB; adjust in settings if needed

### Environment Variables:

Make sure all required environment variables are set in your `.env` file as shown in the Setup section.

## Development

### Project Structure

```
backend_backup/
├── src/
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   ├── api/
│   │   ├── routes/      # API endpoints
│   │   └── middleware/  # Middleware components
│   └── config/          # Configuration
├── tests/               # Test files
├── scripts/             # Utility scripts
├── requirements.txt     # Dependencies
└── .env.example         # Environment variable template
```

### Testing

The project includes both unit and integration tests:

- Unit tests: Test individual components in isolation
- Integration tests: Test API endpoints and service interactions

Run all tests with:
```bash
python -m pytest tests/ -v
```

## Performance and Limitations

- Response latency target: <2 seconds for typical queries
- Supported file formats: PDF, HTML, TEXT
- Chunking strategies: Semantic, overlapping, fixed-size
- Free tier compliance: Monitored via usage tracking script

## Security

- All API endpoints require authentication via Bearer token
- API keys stored in environment variables, not in code
- Secure connection to external services (Qdrant, Neon, Cohere)
- Input validation on all endpoints

## License

This project is part of the Physical-AI-Robotics-Book and is subject to the repository's licensing terms.