import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

class TestSelectedTextQueryIntegration:
    @pytest.mark.skip(reason="Requires authentication header")
    def test_selected_text_query(self):
        """Test the selected text query endpoint"""
        # This test would require:
        # 1. A valid API key in headers
        # 2. Example request body
        query_data = {
            "selected_text": "This is the selected text passage.",
            "query": "What does this mean?",
            "temperature": 0.7
        }
        
        # Without a valid API key, this will fail authentication
        response = client.post("/query/selected", json=query_data)
        
        # The response should be 401 or 403 due to missing authentication
        # rather than testing the actual functionality
        assert response.status_code in [401, 403]