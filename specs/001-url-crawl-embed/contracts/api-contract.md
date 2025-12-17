# API Contract: URL Crawl → Embed → Qdrant Upload

## Overview
This document describes the internal functions and interfaces for the URL crawling, text extraction, embedding, and Qdrant storage pipeline.

## Functions Specification

### get_all_urls(base_url: str) -> List[str]
**Purpose**: Crawl the Docusaurus book site and extract all accessible page URLs

**Parameters**:
- base_url (str): The base URL of the Docusaurus book site

**Returns**:
- List[str]: List of all discovered URLs within the book site

**Error Handling**:
- Raises: ConnectionError if base URL is not accessible
- Logs: Individual URL failures but continues processing

### extract_text_from_url(url: str) -> Dict[str, str]
**Purpose**: Extract clean text content from a given URL

**Parameters**:
- url (str): The URL to extract text from

**Returns**:
- Dict[str, str]: Dictionary containing:
  - 'title': Page title
  - 'content': Clean text content
  - 'url': Original URL

**Error Handling**:
- Returns empty content if URL is not accessible
- Handles malformed HTML gracefully

### chunk_text(text: str, chunk_size: int = 1024, overlap: int = 100) -> List[Dict[str, str]]
**Purpose**: Split text into appropriately sized chunks for embedding

**Parameters**:
- text (str): The text to chunk
- chunk_size (int): Maximum size of each chunk (default: 1024)
- overlap (int): Overlap between chunks to maintain context (default: 100)

**Returns**:
- List[Dict[str, str]]: List of text chunks with metadata

### embed(text_chunks: List[Dict[str, str]]) -> List[Dict[str, Any]]
**Purpose**: Generate embeddings for text chunks using Cohere

**Parameters**:
- text_chunks (List[Dict[str, str]]): List of text chunks to embed

**Returns**:
- List[Dict[str, Any]]: List of embeddings with associated metadata

**Error Handling**:
- Implements retry logic for API failures
- Handles rate limiting from Cohere API

### create_collection(collection_name: str = 'rag_embedding') -> bool
**Purpose**: Create or verify existence of Qdrant collection

**Parameters**:
- collection_name (str): Name of the collection to create (default: 'rag_embedding')

**Returns**:
- bool: True if collection exists/created successfully

### save_chunk_to_qdrant(embedding_data: Dict[str, Any]) -> bool
**Purpose**: Store a single embedded chunk in Qdrant with metadata

**Parameters**:
- embedding_data (Dict[str, Any]): The embedding and associated metadata to store

**Returns**:
- bool: True if successfully stored, False otherwise

**Error Handling**:
- Handles Qdrant connection failures
- Validates vector dimensionality before storage

## Data Formats

### Text Chunk Format
```json
{
  "id": "unique_chunk_identifier",
  "content": "The actual text content of the chunk",
  "source_url": "https://example.com/original-page",
  "source_title": "Original Page Title",
  "chunk_index": 0
}
```

### Embedding Format
```json
{
  "chunk_id": "unique_chunk_identifier",
  "vector": [0.1, 0.2, 0.3, ...],
  "model_name": "embed-multilingual-v2.0",
  "metadata": {
    "source_url": "https://example.com/original-page",
    "source_title": "Original Page Title",
    "content": "The actual text content of the chunk"
  }
}
```

### Qdrant Payload Format
```json
{
  "source_url": "https://example.com/original-page",
  "source_title": "Original Page Title",
  "content": "The actual text content of the chunk",
  "chunk_index": 0,
  "created_at": "2025-12-13T10:00:00Z"
}
```

## Configuration

### Environment Variables
- `COHERE_API_KEY`: API key for Cohere embeddings service
- `QDRANT_URL`: URL for Qdrant Cloud instance
- `QDRANT_API_KEY`: API key for Qdrant Cloud
- `BOOK_BASE_URL`: Base URL of the Docusaurus book (default: https://aqsaiftikhar15.github.io/Textbook-for-Teaching-Physical-AI-Humanoid-Robotics-Course/)

### Default Parameters
- Chunk size: 1024 characters
- Chunk overlap: 100 characters
- Collection name: 'rag_embedding'
- Rate limiting: Appropriate delays to respect target server