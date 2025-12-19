import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from uuid import uuid4

client = TestClient(app)

class TestFullBookQueryIntegration:
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    @pytest.mark.skip(reason="Requires authentication header")
    def test_full_book_query_endpoint(self):
        """Test the full book query endpoint (requires authentication and existing book)"""
        # This test would require:
        # 1. A valid API key in headers
        # 2. An existing book in the system
        # For now, we'll skip this test
        pass
    
    @pytest.mark.skip(reason="Requires authentication header")
    def test_selected_text_query_endpoint(self):
        """Test the selected text query endpoint (requires authentication)"""
        # This test would require:
        # 1. A valid API key in headers
        # For now, we'll skip this test
        pass
    
    @pytest.mark.skip(reason="Requires authentication header")
    def test_ingest_upload_endpoint(self):
        """Test the ingest upload endpoint (requires authentication and file upload)"""
        # This test would require:
        # 1. A valid API key in headers
        # 2. A file to upload
        # For now, we'll skip this test
        pass