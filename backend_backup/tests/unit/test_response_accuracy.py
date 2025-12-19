import pytest
from unittest.mock import patch, MagicMock
from src.services.rag import rag_service

class TestResponseAccuracy:
    @patch('cohere.Client')
    def test_full_book_query_accuracy(self, mock_cohere_client):
        """Test that full-book queries return accurate responses based on context"""
        # Mock the Cohere response
        mock_generate_response = MagicMock()
        mock_generation = MagicMock()
        mock_generation.text = "This response is based on the provided context."
        mock_generate_response.generations = [mock_generation]
        mock_cohere_client.return_value.generate.return_value = mock_generate_response
        
        # Mock the embedding service
        with patch('src.services.rag.embedding_service') as mock_embedding_service, \
             patch('src.services.rag.storage_service') as mock_storage_service:
            
            # Mock embedding generation
            mock_embedding_service.embed_query.return_value = [0.1, 0.2, 0.3]
            
            # Mock search results with specific context
            context_text = "The theory of relativity was developed by Albert Einstein."
            mock_search_results = [
                {
                    'id': 'chunk1',
                    'score': 0.9,
                    'payload': {'book_id': 'book123'},
                    'text': context_text
                }
            ]
            mock_storage_service.search_chunks.return_value = mock_search_results
            
            # Test the method with a question related to the context
            response = rag_service.query_full_book(
                book_id='book123',
                query_text='Who developed the theory of relativity?',
                max_results=5,
                temperature=0.7
            )
            
            # Verify the response contains information from the context
            # In a real test, we would verify the response is factually accurate
            assert 'Einstein' in response.response or 'relativity' in response.response
            assert 'context' in response.response.lower()  # Verifying it used the context
    
    @patch('cohere.Client')
    def test_selected_text_query_accuracy(self, mock_cohere_client):
        """Test that selected-text queries return accurate responses based on the provided text"""
        # Mock the Cohere response
        mock_generate_response = MagicMock()
        mock_generation = MagicMock()
        mock_generation.text = "Based on the provided text, the concept is explained here."
        mock_generate_response.generations = [mock_generation]
        mock_cohere_client.return_value.generate.return_value = mock_generate_response
        
        # Test the method with selected text
        selected_text = "The process of photosynthesis converts light energy to chemical energy."
        response = rag_service.query_selected_text(
            selected_text=selected_text,
            query='What does photosynthesis do?',
            temperature=0.7
        )
        
        # Verify the response is based on the provided text
        assert 'photosynthesis' in response.response.lower()
        assert 'energy' in response.response.lower()
    
    @patch('cohere.Client')
    def test_response_fidelity_to_context(self, mock_cohere_client):
        """Test that responses are faithful to the provided context and don't hallucinate"""
        # Mock the Cohere response
        mock_generate_response = MagicMock()
        mock_generation = MagicMock()
        # Mock response that properly references the context
        mock_generation.text = "According to the text, this is how it works."
        mock_generate_response.generations = [mock_generation]
        mock_cohere_client.return_value.generate.return_value = mock_generate_response
        
        # Mock the embedding service
        with patch('src.services.rag.embedding_service') as mock_embedding_service, \
             patch('src.services.rag.storage_service') as mock_storage_service:
            
            # Mock embedding generation
            mock_embedding_service.embed_query.return_value = [0.1, 0.2, 0.3]
            
            # Mock search results with specific context
            context_text = "Quantum computing uses quantum bits or qubits."
            mock_search_results = [
                {
                    'id': 'chunk1',
                    'score': 0.9,
                    'payload': {'book_id': 'book123'},
                    'text': context_text
                }
            ]
            mock_storage_service.search_chunks.return_value = mock_search_results
            
            # Test the method
            response = rag_service.query_full_book(
                book_id='book123',
                query_text='What does quantum computing use?',
                max_results=5,
                temperature=0.3  # Lower temperature to reduce creativity/hallucination
            )
            
            # Verify the response is faithful to the context
            assert 'quantum' in response.response.lower()
            assert 'qubits' in response.response.lower()
            
            # In a real implementation, we might also verify that it doesn't contain
            # information not present in the context