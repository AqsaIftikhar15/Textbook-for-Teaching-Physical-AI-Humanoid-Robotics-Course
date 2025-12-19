import pytest
from src.services.ingestion import ingestion_service
from src.models.chunk import ChunkCreate
from uuid import uuid4

class TestIngestionService:
    def test_preprocess_text(self):
        """Test the text preprocessing function"""
        raw_text = "This is   a test\u00a0with\u200b weird\u00a0 characters."
        processed_text = ingestion_service.preprocess_text(raw_text)
        
        # Should have normalized spaces and removed zero-width space
        assert "  " not in processed_text  # Multiple spaces normalized
        assert "\u00a0" not in processed_text  # Non-breaking space removed
        assert "\u200b" not in processed_text  # Zero-width space removed
        assert processed_text == "This is a test with weird characters."
    
    def test_chunk_text_semantic(self):
        """Test semantic chunking"""
        text = "This is the first paragraph.\n\nThis is the second paragraph.\n\nAnd this is the third paragraph."
        chunks = ingestion_service.chunk_text(text, "semantic")
        
        assert len(chunks) >= 1
        assert all(len(chunk) > 10 for chunk in chunks)  # Each chunk should have some content
        assert "first paragraph" in chunks[0]  # Should have content from the text
    
    def test_chunk_text_overlapping(self):
        """Test overlapping chunking"""
        # Set smaller chunk size for testing
        original_chunk_size = ingestion_service.chunk_size
        original_overlap = ingestion_service.chunk_overlap
        ingestion_service.chunk_size = 30
        ingestion_service.chunk_overlap = 5
        
        try:
            text = "This is a longer text that will be split into multiple overlapping chunks with some overlap between them."
            chunks = ingestion_service.chunk_text(text, "overlapping")
            
            assert len(chunks) >= 2  # Should be split into multiple chunks
            assert all(len(chunk) <= 30 for chunk in chunks)  # Each chunk should be within size limit
        finally:
            # Restore original values
            ingestion_service.chunk_size = original_chunk_size
            ingestion_service.chunk_overlap = original_overlap
    
    def test_chunk_text_fixed_size(self):
        """Test fixed-size chunking"""
        # Set smaller chunk size for testing
        original_chunk_size = ingestion_service.chunk_size
        original_overlap = ingestion_service.chunk_overlap
        ingestion_service.chunk_size = 20
        ingestion_service.chunk_overlap = 0
        
        try:
            text = "This is a longer text that will be split into fixed-size chunks."
            chunks = ingestion_service.chunk_text(text, "fixed_size")
            
            assert len(chunks) >= 2  # Should be split into multiple chunks
            # Check that chunks are approximately the right size
            for i, chunk in enumerate(chunks):
                if i < len(chunks) - 1:  # Not the last chunk
                    assert len(chunk) <= 20
                else:  # Last chunk may be shorter
                    assert len(chunk) > 0
        finally:
            # Restore original values
            ingestion_service.chunk_size = original_chunk_size
            ingestion_service.chunk_overlap = original_overlap