"""
Test script for the URL Crawl -> Embed -> Qdrant Upload pipeline
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import get_all_urls, extract_text_from_url, chunk_text, embed, create_collection, save_chunk_to_qdrant, validate_storage, retrieve_and_validate

def test_pipeline():
    """Test the complete pipeline functionality"""
    print("Testing the URL Crawl -> Embed -> Qdrant Upload pipeline...")

    # Test 1: Create Qdrant collection
    print("\n1. Testing Qdrant collection creation...")
    success = create_collection('rag_embedding')
    if success:
        print("PASS Qdrant collection created successfully")
    else:
        print("FAIL Failed to create Qdrant collection")
        return False

    # Test 2: Validate storage
    print("\n2. Testing storage validation...")
    success = validate_storage()
    if success:
        print("PASS Storage validation passed")
    else:
        print("FAIL Storage validation failed")
        return False

    # Test 3: Test text chunking
    print("\n3. Testing text chunking...")
    sample_text = "This is a sample text for testing the chunking functionality. " * 50  # Make it long enough to chunk
    chunks = chunk_text(sample_text, chunk_size=100, overlap=20)
    if len(chunks) > 0:
        print(f"PASS Text chunked successfully into {len(chunks)} chunks")
    else:
        print("FAIL Text chunking failed")
        return False

    # Test 4: Test embedding (with a smaller sample for efficiency)
    print("\n4. Testing embedding functionality...")
    small_sample = [{"content": "This is a test sentence for embedding.", "source_url": "test", "source_title": "test", "chunk_index": 0}]
    try:
        embeddings = embed(small_sample)
        if len(embeddings) > 0:
            print(f"PASS Embedding generated successfully with vector dimension: {len(embeddings[0]['vector'])}")
        else:
            print("FAIL No embeddings generated")
            return False
    except Exception as e:
        print(f"FAIL Embedding failed: {e}")
        return False

    # Test 5: Test saving to Qdrant
    print("\n5. Testing save to Qdrant...")
    if len(embeddings) > 0:
        success = save_chunk_to_qdrant(embeddings[0])
        if success:
            print("PASS Chunk saved to Qdrant successfully")
        else:
            print("FAIL Failed to save chunk to Qdrant")
            return False

    # Test 6: Test retrieval from Qdrant
    print("\n6. Testing retrieval from Qdrant...")
    success = retrieve_and_validate()
    if success:
        print("PASS Retrieval and validation successful")
    else:
        print("FAIL Retrieval and validation failed")
        return False

    print("\nPASS All tests passed! The pipeline is functional.")
    return True

if __name__ == "__main__":
    success = test_pipeline()
    if success:
        print("\nPipeline test completed successfully!")
    else:
        print("\nPipeline test failed!")
        sys.exit(1)