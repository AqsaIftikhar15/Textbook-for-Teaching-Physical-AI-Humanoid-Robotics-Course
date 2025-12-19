import cohere
from typing import List
from src.config.settings import settings

class EmbeddingService:
    def __init__(self):
        self.client = cohere.Client(settings.cohere_api_key)
        self.model = settings.cohere_embedding_model

    def embed_text(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Cohere
        """
        try:
            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type="search_document"
            )
            return [item for item in response.embeddings]
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise

    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a single query using Cohere
        """
        try:
            response = self.client.embed(
                texts=[query],
                model=self.model,
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            raise

embedding_service = EmbeddingService()