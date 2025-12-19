from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

class BookStatus(str, Enum):
    PROCESSING = "PROCESSING"
    READY = "READY"
    ERROR = "ERROR"

class ContentType(str, Enum):
    PDF = "PDF"
    HTML = "HTML"
    TEXT = "TEXT"

class ChunkStrategy(str, Enum):
    SEMANTIC = "semantic"
    OVERLAPPING = "overlapping"
    FIXED_SIZE = "fixed_size"

class Book(BaseModel):
    id: UUID
    title: str
    author: str
    content_type: ContentType
    upload_date: datetime
    chunk_strategy: ChunkStrategy
    total_chunks: int
    status: BookStatus
    file_path: Optional[str] = None  # Path to the original file
    description: Optional[str] = None
    language: Optional[str] = "en"  # Language of the book

class BookCreate(BaseModel):
    title: str
    author: str
    content_type: ContentType
    chunk_strategy: ChunkStrategy = ChunkStrategy.SEMANTIC
    description: Optional[str] = None
    language: Optional[str] = "en"

class BookUpdateStatus(BaseModel):
    status: BookStatus
    total_chunks: Optional[int] = None
    processed_chunks: Optional[int] = None

class Chunk(BaseModel):
    id: UUID
    book_id: UUID
    text: str
    chunk_index: int
    # Note: embedding_vector is not included here as it's stored in the vector database
    metadata: dict
    hash: str
    created_at: datetime

class Query(BaseModel):
    id: UUID
    book_id: Optional[UUID]  # For full-book queries
    query_type: str  # "FULL_BOOK" or "SELECTED_TEXT"
    user_query: str
    selected_text: Optional[str] = None  # For selected-text queries
    response: str
    retrieved_chunks: Optional[List[UUID]] = []  # Chunk IDs for full-book queries
    query_time: datetime
    response_time: float  # In seconds
    tokens_used: int

class UploadBookResponse(BaseModel):
    status: str
    book_id: str
    message: str

class BookStatusResponse(BaseModel):
    book_id: str
    status: str
    title: Optional[str] = None
    progress: Optional[float] = 0.0
    total_chunks: Optional[int] = 0
    processed_chunks: Optional[int] = 0
    error_message: Optional[str] = None