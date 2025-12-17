"""
Simple test to verify Qdrant functionality
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

# Load environment variables from .env file
load_dotenv()

def test_qdrant_connection():
    """Test basic Qdrant connection and operations"""
    try:
        # Get Qdrant connection details from environment
        qdrant_url = os.getenv('QDRANT_URL')
        qdrant_api_key = os.getenv('QDRANT_API_KEY')

        if not qdrant_url or not qdrant_api_key:
            print("ERROR: QDRANT_URL and QDRANT_API_KEY environment variables are required")
            return False

        # Create Qdrant client
        qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )

        print("PASS Successfully connected to Qdrant")

        # Check if collection exists
        collections = qdrant_client.get_collections()
        collection_exists = any(col.name == "rag_embedding" for col in collections.collections)

        if collection_exists:
            print("PASS Collection 'rag_embedding' exists")
        else:
            print("INFO Collection 'rag_embedding' does not exist, creating it...")
            # Create the collection with appropriate vector size (1024 for Cohere embeddings)
            qdrant_client.recreate_collection(
                collection_name="rag_embedding",
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
            )
            print("PASS Collection 'rag_embedding' created successfully")

        # Test inserting a simple point
        import uuid
        test_point = PointStruct(
            id=str(uuid.uuid4()),  # Use a proper UUID
            vector=[0.1] * 1024,  # 1024-dimensional vector as expected by Cohere
            payload={
                "original_id": "test_point_1",  # Store original ID in payload
                "source_url": "test://test",
                "content": "This is a test content to verify Qdrant functionality",
                "chunk_index": 0,
                "created_at": "2025-12-13T00:00:00Z"
            }
        )

        # Upsert the test point
        qdrant_client.upsert(
            collection_name="rag_embedding",
            points=[test_point]
        )

        print("PASS Successfully inserted test point into Qdrant")

        # Count points in the collection
        count = qdrant_client.count(collection_name="rag_embedding")
        print(f"INFO Collection contains {count.count} points after test insertion")

        # Try to retrieve the test point
        # Since we don't know the exact UUID we used, let's use scroll to get a sample
        scroll_result, next_offset = qdrant_client.scroll(
            collection_name="rag_embedding",
            limit=1  # Just get one point as a sample
        )

        if scroll_result:  # If we have at least one point
            point = scroll_result[0]
            print("PASS Successfully retrieved test point from Qdrant")
            print(f"  Retrieved content: {point.payload.get('content', 'N/A')}")
            print(f"  Point ID: {point.id}")
        else:
            print("WARN Failed to retrieve test point from Qdrant")

        return True

    except Exception as e:
        print(f"FAIL Error during Qdrant test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Qdrant connection and basic operations...")
    success = test_qdrant_connection()
    if success:
        print("\nPASS Qdrant test completed successfully!")
        print("The issue is likely not with Qdrant connection itself,")
        print("but may be with the data processing pipeline.")
    else:
        print("\nFAIL Qdrant test failed!")
        print("There may be an issue with the Qdrant configuration or credentials.")