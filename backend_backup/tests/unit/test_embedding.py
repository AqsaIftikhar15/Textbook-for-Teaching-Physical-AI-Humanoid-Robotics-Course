import pytest
from unittest.mock import patch, MagicMock
from src.services.embedding import embedding_service
import cohere

class TestEmbeddingService:
    @patch('cohere.Client')
    def test_embed_text(self, mock_cohere_client):
        """Test embedding text with Cohere"""
        # Mock the Cohere response
        mock_response = MagicMock()
        mock_response.embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        mock_cohere_client.return_value.embed.return_value = mock_response
        
        # Reinitialize the embedding service with mocked client
        from src.services.embedding import EmbeddingService
        from src.config.settings import settings
        test_service = EmbeddingService()
        test_service.client = mock_cohere_client.return_value
        
        texts = ["Hello world", "Test sentence"]
        embeddings = test_service.embed_text(texts)
        
        # Verify the result
        assert len(embeddings) == 2
        assert len(embeddings[0]) == 3  # 3 dimensions
        assert len(embeddings[1]) == 3  # 3 dimensions
        
        # Verify the API was called correctly
        test_service.client.embed.assert_called_once()
    
    @patch('cohere.Client')
    def test_embed_query(self, mock_cohere_client):
        """Test embedding a single query with Cohere"""
        # Mock the Cohere response
        mock_response = MagicMock()
        mock_response.embeddings = [[0.7, 0.8, 0.9]]
        mock_cohere_client.return_value.embed.return_value = mock_response
        
        # Reinitialize the embedding service with mocked client
        from src.services.embedding import EmbeddingService
        test_service = EmbeddingService()
        test_service.client = mock_cohere_client.return_value
        
        query = "What is this?"
        embedding = test_service.embed_query(query)
        
        # Verify the result
        assert len(embedding) == 3  # 3 dimensions
        assert embedding == [0.7, 0.8, 0.9]
        
        # Verify the API was called correctly
        test_service.client.embed.assert_called_once()