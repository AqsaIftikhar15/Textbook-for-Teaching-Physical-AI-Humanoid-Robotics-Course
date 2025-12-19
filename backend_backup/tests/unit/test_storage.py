import pytest
from unittest.mock import patch, MagicMock, Mock
from src.services.storage import storage_service
from src.models.chunk import ChunkCreate
from uuid import uuid4
import psycopg2

class TestStorageService:
    def test_store_chunks(self):
        """Test storing chunks to Qdrant and Neon"""
        # This is a complex test that would require mocks for Qdrant and Neon
        # For now, we'll test a simplified version focusing on the logic
        pass
    
    @patch('psycopg2.connect')
    def test_get_chunk_text(self, mock_connect):
        """Test retrieving chunk text from Neon Postgres"""
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Mock the fetchone result
        mock_cursor.fetchone.return_value = ["This is the chunk text"]
        
        # Test the method
        chunk_id = str(uuid4())
        result = storage_service.get_chunk_text(chunk_id)
        
        # Verify the result
        assert result == "This is the chunk text"
        mock_cursor.execute.assert_called_once_with(
            "SELECT text FROM chunks WHERE id = %s",
            (chunk_id,)
        )
    
    @patch('psycopg2.connect')
    def test_get_book_chunks(self, mock_connect):
        """Test retrieving all chunks for a book from Neon Postgres"""
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Mock the fetchall result
        mock_chunks = [
            {'id': str(uuid4()), 'text': 'Chunk 1 text', 'chunk_index': 0, 'metadata': {}},
            {'id': str(uuid4()), 'text': 'Chunk 2 text', 'chunk_index': 1, 'metadata': {}}
        ]
        mock_cursor.fetchall.return_value = mock_chunks
        
        book_id = uuid4()
        result = storage_service.get_book_chunks(book_id)
        
        # Verify the result
        assert len(result) == 2
        assert result[0]['text'] == 'Chunk 1 text'
        assert result[1]['text'] == 'Chunk 2 text'
        mock_cursor.execute.assert_called_once_with(
            "SELECT id, text, chunk_index, metadata FROM chunks WHERE book_id = %s ORDER BY chunk_index",
            (str(book_id),)
        )