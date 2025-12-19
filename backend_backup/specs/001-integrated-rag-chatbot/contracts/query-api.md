# API Contract: Query Endpoints

## POST /query/full

### Description
Query the system using full book content for context. This mode allows the system to draw from the entire book to answer the question.

### Request
- **Content-Type**: application/json
- **Headers**:
  - `Authorization: Bearer {API_KEY}`
- **Body**:
  ```json
  {
    "book_id": "uuid-of-book",
    "query": "What is the main theme of this book?",
    "max_results": 5,
    "temperature": 0.7
  }
  ```
- **Fields**:
  - `book_id`: UUID of the book to query
  - `query`: The question to ask about the book
  - `max_results`: (Optional) Maximum number of context chunks to retrieve (default: 5)
  - `temperature`: (Optional) Generation temperature (default: 0.7)

### Response
- **200 OK**: Successful query response
  ```json
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
- **400 Bad Request**: Invalid request format
- **401 Unauthorized**: Invalid API key
- **404 Not Found**: Book ID not found
- **500 Internal Server Error**: Processing error

---

## POST /query/selected

### Description
Query the system using only the provided selected text passage. This mode responds exclusively based on the provided text without referencing other parts of the book.

### Request
- **Content-Type**: application/json
- **Headers**:
  - `Authorization: Bearer {API_KEY}`
- **Body**:
  ```json
  {
    "selected_text": "The specific text passage selected by the user",
    "query": "What does this passage mean?",
    "temperature": 0.7
  }
  ```
- **Fields**:
  - `selected_text`: The text passage selected by the user
  - `query`: The question about the selected text
  - `temperature`: (Optional) Generation temperature (default: 0.7)

### Response
- **200 OK**: Successful query response
  ```json
  {
    "query_id": "uuid",
    "response": "Based on the provided text, this means...",
    "query_time": 0.876,
    "tokens_used": 32
  }
  ```
- **400 Bad Request**: Invalid request format or empty text
- **401 Unauthorized**: Invalid API key
- **500 Internal Server Error**: Processing error

---

## POST /query/generic

### Description
Generic query endpoint that can handle both modes. Allows specifying the query type in the request body.

### Request
- **Content-Type**: application/json
- **Headers**:
  - `Authorization: Bearer {API_KEY}`
- **Body** (Full-book mode):
  ```json
  {
    "query_type": "FULL_BOOK",
    "book_id": "uuid-of-book",
    "query": "What is the main theme of this book?",
    "max_results": 5
  }
  ```
- **Body** (Selected-text mode):
  ```json
  {
    "query_type": "SELECTED_TEXT",
    "selected_text": "The specific text passage selected by the user",
    "query": "What does this passage mean?"
  }
  ```

### Response
Same as above for each respective mode.