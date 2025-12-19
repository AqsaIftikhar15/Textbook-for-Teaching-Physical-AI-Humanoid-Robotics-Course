# Integrated RAG Chatbot API Documentation

## Overview

The Integrated RAG Chatbot API provides endpoints for ingesting books, querying book content, and monitoring system usage. The API follows REST principles and uses JSON for request/response bodies.

## Authentication

All API endpoints (except health check) require authentication via a Bearer token:

```
Authorization: Bearer YOUR_API_KEY
```

Set your API key in the `.env` file as `API_KEY=your_secret_api_key_here`.

## Endpoints

### Health Check

GET /

Returns basic health status of the API.

**Response**:
```
{
  "status": "healthy"
}
```

### Ingestion Endpoints

#### Upload Book

POST /ingest/upload

Upload a book file (PDF, HTML, or text) for processing and indexing.

**Parameters** (as form fields):
- `file` (required): The book file to upload (PDF, HTML, or text)
- `title` (required): Title of the book
- `chunk_strategy`: Strategy for chunking ("semantic", "overlapping", "fixed_size") - defaults to "semantic"
- `author`: Author of the book
- `description`: Description of the book

**Response**:
```
{
  "status": "accepted",
  "book_id": "uuid-of-book-being-processed",
  "message": "Book is being processed and will be available shortly"
}
```

#### Check Processing Status

GET /ingest/status/{book_id}

Get the processing status of an uploaded book.

**Response**:
```
{
  "book_id": "uuid",
  "status": "PROCESSING|READY|ERROR",
  "title": "Book title",
  "progress": 0.75,
  "total_chunks": 120,
  "processed_chunks": 90,
  "error_message": "null|string"
}
```

### Query Endpoints

#### Full Book Query

POST /query/full

Query the system using full book content for context.

**Request Body**:
```
{
  "book_id": "uuid-of-book",
  "query": "What is the main theme of this book?",
  "max_results": 5,
  "temperature": 0.7
}
```

**Response**:
```
{
  "query_id": "uuid",
  "response": "The main theme of this book is...",
  "citations": [
    {
      "chunk_id": "uuid",
      "text": "The relevant text chunk...",
      "similarity_score": 0.89
    }
  ],
  "query_time": 1.234,
  "tokens_used": 45
}
```

#### Selected Text Query

POST /query/selected

Query the system using only the provided selected text passage.

**Request Body**:
```
{
  "selected_text": "The specific text passage selected by the user",
  "query": "What does this passage mean?",
  "temperature": 0.7
}
```

**Response**:
```
{
  "query_id": "uuid",
  "response": "Based on the provided text, this means...",
  "query_time": 0.876,
  "tokens_used": 32
}
```

### Monitoring Endpoints

#### Usage Metrics

GET /monitor/usage

Get current usage metrics for Qdrant Cloud and Neon Serverless Postgres to ensure staying within free-tier limits.

**Response**:
```
{
  "timestamp": "2025-12-19T10:30:00Z",
  "qdrant_usage": {
    "collection_size": 15000,
    "max_collection_size": 50000,
    "upsert_count": 250,
    "max_upsert_per_month": 100000,
    "percentage_used": 30.0
  },
  "neon_usage": {
    "compute_time_used": 7200,  // in seconds
    "max_compute_time": 14400,  // in seconds (4 hours)
    "data_transfer_used": 0.5,  // in GB
    "max_data_transfer": 10,  // in GB
    "percentage_used": 50.0
  },
  "cohere_usage": {
    "api_calls_made": 450,
    "max_api_calls": 10000,  // per month if applicable
    "percentage_used": 4.5
  },
  "recommendations": [
    "Neon compute time at 50% - consider optimizing queries",
    "Qdrant usage at 30% - within safe limits"
  ]
}
```

#### System Status

GET /monitor/status

Get the overall system health status.

**Response**:
```
{
  "status": "healthy",
  "services": {
    "qdrant_connection": "connected",
    "neon_connection": "connected",
    "cohere_api": "connected",
    "application": "running"
  },
  "last_updated": "2025-12-19T10:30:00Z"
}
```

## Example Usage

### Uploading and Querying a Book

1. Upload a book file:
```bash
curl -X POST "http://localhost:8000/ingest/upload" \
  -H "Authorization: Bearer your_secret_api_key_here" \
  -F "file=@path/to/your/book.pdf" \
  -F "title=My Sample Book" \
  -F "author=John Doe"
```

2. Check processing status:
```bash
curl -X GET "http://localhost:8000/ingest/status/{book_id}" \
  -H "Authorization: Bearer your_secret_api_key_here"
```

3. Query the book after it's ready:
```bash
curl -X POST "http://localhost:8000/query/full" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_secret_api_key_here" \
  -d '{
    "book_id": "your-book-uuid",
    "query": "What is the main theme of this book?"
  }'
```

### Querying Selected Text

```bash
curl -X POST "http://localhost:8000/query/selected" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_secret_api_key_here" \
  -d '{
    "selected_text": "The specific text passage selected by the user",
    "query": "What does this passage mean?"
  }'
```

## Error Handling

Common HTTP response codes:

- `200 OK`: Request handled successfully
- `202 ACCEPTED`: Request accepted for processing (asynchronous)
- `400 BAD REQUEST`: Invalid request format or parameters
- `401 UNAUTHORIZED`: Missing or invalid authentication
- `404 NOT FOUND`: Requested resource not found
- `413 PAYLOAD TOO LARGE`: File exceeds size limits
- `500 INTERNAL SERVER ERROR`: Server error processing request

Error responses follow the format:
```
{
  "detail": "Human-readable error message"
}
```

## Rate Limits

This implementation does not include application-level rate limiting. However, the underlying services (Cohere, Qdrant, Neon) have their own rate limits based on free-tier usage.

## Security

All communication with the API should be done over HTTPS in production environments. The API key should be treated as a secret and not exposed in client-side code or version control systems.