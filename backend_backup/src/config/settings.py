from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_KEY: str = os.getenv("API_KEY", "your_default_secret_key_here")

    # Cohere Settings
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    cohere_embedding_model: str = os.getenv("COHERE_EMBEDDING_MODEL", "embed-english-v3.0")
    cohere_generation_model: str = os.getenv("COHERE_GENERATION_MODEL", "command-r-plus")

    # Qdrant Settings
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "books_collection")

    # Neon Postgres Settings
    neon_db_url: str = os.getenv("NEON_DB_URL", "")

    # Application Settings
    app_name: str = "Integrated RAG Chatbot"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", 52428800))  # 50MB default (50 * 1024 * 1024)
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))  # 1000 characters default
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "100"))  # 100 characters default

    class Config:
        env_file = ".env"

settings = Settings()