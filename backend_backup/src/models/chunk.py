from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
from uuid import UUID, uuid4
import hashlib

class Chunk(BaseModel):
    id: UUID
    book_id: UUID
    text: str
    chunk_index: int
    # embedding_vector is handled separately in the service layer
    metadata: Dict
    hash: str
    created_at: datetime
    
    class Config:
        # Enable UUID serialization
        json_encoders = {
            UUID: str
        }

class ChunkCreate(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4) 
    book_id: UUID
    text: str
    chunk_index: int
    metadata: Optional[Dict] = {}
    hash: Optional[str] = None

    
    def compute_hash(self) -> str:
        """Compute hash of the text content for duplicate detection"""
        return hashlib.sha256(self.text.encode()).hexdigest()

class ChunkWithEmbedding(Chunk):
    embedding_vector: List[float]