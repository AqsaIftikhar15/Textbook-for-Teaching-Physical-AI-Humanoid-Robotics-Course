from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class QueryType(str, Enum):
    FULL_BOOK = "FULL_BOOK"
    SELECTED_TEXT = "SELECTED_TEXT"

class Query(BaseModel):
    id: UUID
    book_id: Optional[UUID] = None  # Required for full-book queries
    query_type: QueryType
    user_query: str
    selected_text: Optional[str] = None  # Required for selected-text queries
    response: str
    retrieved_chunks: Optional[List[UUID]] = []  # For full-book queries
    query_time: datetime
    response_time: float  # In seconds
    tokens_used: int

class QueryCreate(BaseModel):
    book_id: Optional[UUID] = None  # Required for full-book queries
    query_type: QueryType
    user_query: str
    selected_text: Optional[str] = None  # Required for selected-text queries
    max_results: Optional[int] = 5  # For full-book queries
    temperature: Optional[float] = 0.7

class QueryResponse(BaseModel):
    query_id: UUID
    response: str
    citations: Optional[List[dict]] = []  # For full-book queries
    query_time: float  # Response time in seconds
    tokens_used: int

class FullBookQuery(BaseModel):
    book_id: UUID
    query: str
    max_results: Optional[int] = 5
    temperature: Optional[float] = 0.7

class SelectedTextQuery(BaseModel):
    selected_text: str
    query: str
    temperature: Optional[float] = 0.7