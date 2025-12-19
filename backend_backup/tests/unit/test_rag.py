import pytest
from unittest.mock import patch, MagicMock
from src.services.rag import rag_service
from src.models.query import QueryResponse

class TestRAGService:
    @patch('cohere.Client')
    def test_query_full_book(self, mock_cohere_client):
        """Test full-book query functionality"""
        # Mock the Cohere response
        mock_generate_response = MagicMock()
        mock_generation = MagicMock()
        mock_generation.text = "This is the generated response based on the context."
        mock_generate_response.generations = [mock_generation]
        mock_cohere_client.return_value.generate.return_value = mock_generate_response
        
        # Mock the embedding service
        with patch('src.services.rag.embedding_service') as mock_embedding_service, \
             patch('src.services.rag.storage_service') as mock_storage_service:
            
            # Mock embedding generation
            mock_embedding_service.embed_query.return_value = [0.1, 0.2, 0.3]
            
            # Mock search results
            mock_search_results = [
                {
                    'id': 'chunk1',
                    'score': 0.9,
                    'payload': {'book_id': 'book123'},
                    'text': 'This is relevant context text from the book.'
                }
            ]
            mock_storage_service.search_chunks.return_value = mock_search_results
            
            # Test the method
            response = rag_service.query_full_book(
                book_id='book123',
                query_text='What is this about?',
                max_results=5,
                temperature=0.7
            )
            
            # Verify the result
            assert isinstance(response, QueryResponse)
            assert 'generated' in response.response.lower()
            assert len(response.citations) == 1
            assert response.tokens_used > 0
            assert response.query_time >= 0
    
    @patch('cohere.Client')
    def test_query_selected_text(self, mock_cohere_client):
        """Test selected-text query functionality"""
        # Mock the Cohere response
        mock_generate_response = MagicMock()
        mock_generation = MagicMock()
        mock_generation.text = "This is the generated response based on the selected text."
        mock_generate_response.generations = [mock_generation]
        mock_cohere_client.return_value.generate.return_value = mock_generate_response
        
        # Test the method
        response = rag_service.query_selected_text(
            selected_text='This is the selected text passage.',
            query='What does this mean?',
            temperature=0.7
        )
        
        # Verify the result
        assert isinstance(response, QueryResponse)
        assert 'generated' in response.response.lower()
        assert len(response.citations) == 0  # No citations for selected-text mode
        assert response.tokens_used > 0
        assert response.query_time >= 0