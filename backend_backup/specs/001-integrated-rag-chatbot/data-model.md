# Data Model: Integrated RAG Chatbot

## Book Entity
- **id**: UUID - Unique identifier for the book
- **title**: String - Title of the book
- **author**: String - Author of the book
- **content_type**: Enum (PDF, HTML, TEXT) - The original format of the book
- **upload_date**: DateTime - When the book was uploaded
- **chunk_strategy**: String - Description of chunking approach used
- **total_chunks**: Integer - Number of chunks created from this book
- **status**: Enum (PROCESSING, READY, ERROR) - Current status of the book processing

## Chunk Entity
- **id**: UUID - Unique identifier for the chunk
- **book_id**: UUID - Reference to the parent book
- **text**: String (long text) - The actual text content of the chunk
- **chunk_index**: Integer - Order of the chunk within the book
- **embedding_vector**: Array of Floats - The vector representation of the text (dimension depends on Cohere model)
- **metadata**: JSON - Additional metadata about the chunk (page number, section, etc.)
- **hash**: String - Hash of the text content for duplicate detection
- **created_at**: DateTime - When the chunk was created

## Query Entity
- **id**: UUID - Unique identifier for the query
- **book_id**: UUID - Reference to the book being queried (for full-book mode)
- **query_type**: Enum (FULL_BOOK, SELECTED_TEXT) - The type of query
- **user_query**: String - The original query from the user
- **selected_text**: String (optional) - The text selected by user (for selected-text mode)
- **response**: String - The generated response
- **retrieved_chunks**: Array of Chunk IDs - The chunks that informed the response (for full-book mode)
- **query_time**: DateTime - When the query was made
- **response_time**: Float - How long the response took in seconds
- **tokens_used**: Integer - Number of tokens in the response

## QuerySession Entity (for future multi-user support)
- **id**: UUID - Unique identifier for the session
- **created_at**: DateTime - When the session was created
- **queries**: Array of Query IDs - All queries in this session
- **active**: Boolean - Whether the session is still active

## MetadataLink Entity (for linking vector storage to Postgres)
- **id**: UUID - Unique identifier
- **qdrant_point_id**: String - The ID of the point in Qdrant
- **chunk_id**: UUID - Reference to the corresponding chunk
- **book_id**: UUID - Reference to the book
- **created_at**: DateTime - When the link was created

## Relationships
- Book 1 -- * Chunk: A book has many chunks
- Book 1 -- * Query: A book can have many queries
- Chunk 1 -- * Query (via retrieved_chunks): A chunk can inform many queries
- QuerySession 1 -- * Query: A session contains many queries
- MetadataLink 1 -- 1 Chunk: Each link corresponds to one chunk