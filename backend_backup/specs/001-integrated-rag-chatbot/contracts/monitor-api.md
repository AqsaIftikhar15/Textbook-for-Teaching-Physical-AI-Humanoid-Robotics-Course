# API Contract: Monitoring Endpoints

## GET /monitor/usage

### Description
Get current usage metrics for Qdrant Cloud and Neon Serverless Postgres to ensure staying within free-tier limits.

### Request
- **Headers**:
  - `Authorization: Bearer {API_KEY}`

### Response
- **200 OK**: Current usage metrics
  ```json
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
- **401 Unauthorized**: Invalid API key
- **500 Internal Server Error**: Could not retrieve usage metrics (may indicate credential issues)

---

## GET /monitor/status

### Description
Get the overall system health status.

### Request
- **Headers**:
  - `Authorization: Bearer {API_KEY}`

### Response
- **200 OK**: System status
  ```json
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
- **401 Unauthorized**: Invalid API key
- **500 Internal Server Error**: One or more services are unavailable