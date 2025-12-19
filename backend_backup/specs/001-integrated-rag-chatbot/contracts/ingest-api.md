# API Contract: Ingestion Endpoints

## POST /ingest/upload

### Description
Upload a book file (PDF, HTML, or text) for processing and indexing.

### Request
- **Content-Type**: multipart/form-data
- **Headers**:
  - `Authorization: Bearer {API_KEY}` (or custom header as configured)
- **Body**:
  - `file`: The book file to upload (PDF, HTML, or text)
  - `title`: (Optional) Title of the book
  - `chunk_strategy`: (Optional) Strategy for chunking ("semantic", "overlapping", "fixed_size") - defaults to "semantic"

### Response
- **202 Accepted**: File accepted for processing
  ```json
  {
    "status": "accepted",
    "book_id": "uuid-of-book-being-processed",
    "message": "Book is being processed and will be available shortly"
  }
  ```
- **400 Bad Request**: Invalid file format or missing required fields
  ```json
  {
    "error": "Invalid file format. Supported formats: PDF, HTML, TEXT",
    "details": "string"
  }
  ```
- **401 Unauthorized**: Invalid API key
- **413 Payload Too Large**: File exceeds size limits

### Processing Flow
1. Validate file format and size
2. Save file temporarily
3. Start async processing (extract text, chunk, embed, store)
4. Return book_id for tracking status

---

## GET /ingest/status/{book_id}

### Description
Get the processing status of an uploaded book.

### Request
- **Headers**:
  - `Authorization: Bearer {API_KEY}`
- **Path Parameters**:
  - `book_id`: UUID of the book being processed

### Response
- **200 OK**: Processing status
  ```json
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
- **401 Unauthorized**: Invalid API key
- **404 Not Found**: Book ID not found