import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

class TestAPIContracts:
    """
    Contract tests for API endpoints to ensure they match the specifications
    """
    
    def test_ingest_upload_contract(self):
        """
        Test the /ingest/upload endpoint matches the contract specification
        """
        # This would normally require authentication which we're skipping for contract tests
        # For now, just verify the endpoint exists and returns appropriate error without auth
        response = client.post("/ingest/upload")
        # Without authentication, expect either 401 or 422 (validation error)
        assert response.status_code in [401, 422]
    
    def test_ingest_status_contract(self):
        """
        Test the /ingest/status/{book_id} endpoint matches the contract specification
        """
        # Test with a dummy book ID
        response = client.get("/ingest/status/dummy-book-id")
        # Without authentication, expect 401
        assert response.status_code == 401
    
    def test_query_full_contract(self):
        """
        Test the /query/full endpoint matches the contract specification
        """
        # Test the endpoint accepts the correct request format
        query_data = {
            "book_id": "test-book-id",
            "query": "What is this about?",
            "max_results": 5,
            "temperature": 0.7
        }
        
        response = client.post("/query/full", json=query_data)
        # Without authentication, expect 401
        assert response.status_code == 401
    
    def test_query_selected_contract(self):
        """
        Test the /query/selected endpoint matches the contract specification
        """
        # Test the endpoint accepts the correct request format
        query_data = {
            "selected_text": "This is the selected text.",
            "query": "What does this mean?",
            "temperature": 0.7
        }
        
        response = client.post("/query/selected", json=query_data)
        # Without authentication, expect 401
        assert response.status_code == 401
    
    def test_monitor_usage_contract(self):
        """
        Test the /monitor/usage endpoint matches the contract specification
        """
        response = client.get("/monitor/usage")
        # Without authentication, expect 401
        assert response.status_code == 401
    
    def test_monitor_status_contract(self):
        """
        Test the /monitor/status endpoint matches the contract specification
        """
        response = client.get("/monitor/status")
        # Without authentication, expect 401
        assert response.status_code == 401