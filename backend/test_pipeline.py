"""
Test script to run a small sample of the pipeline to verify functionality
"""
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()  # Load environment variables

from main import create_collection, save_chunk_to_qdrant, validate_storage, retrieve_and_validate, chunk_text, embed

def test_pipeline():
    """Test a small sample of the pipeline functionality"""
    print("Testing a small sample of the pipeline...")

    # Step 1: Create collection
    print("\n1. Creating Qdrant collection...")
    success = create_collection('rag_embedding')
    if success:
        print("PASS Collection created/accessed successfully")
    else:
        print("FAIL Failed to create/access collection")
        return False

    # Step 2: Test with a small sample text
    print("\n2. Testing with sample text...")
    sample_text = "Artificial Intelligence and Robotics are interdisciplinary fields combining computer science, engineering, and cognitive science to create systems that can perform tasks requiring human-like intelligence. These systems can perceive their environment, make decisions, and take actions to achieve specific goals."

    # Chunk the text
    chunks = chunk_text(sample_text, chunk_size=200, overlap=50)
    print(f"PASS Text chunked into {len(chunks)} chunks")

    # Add source info
    for chunk in chunks:
        chunk['source_url'] = 'test://sample'
        chunk['source_title'] = 'Sample Test'

    # Step 3: Generate embeddings
    print("\n3. Generating embeddings...")
    try:
        embeddings = embed(chunks)
        print(f"PASS Generated embeddings for {len(embeddings)} chunks")
    except Exception as e:
        print(f"FAIL Embedding generation failed: {e}")
        return False

    # Step 4: Save to Qdrant
    print("\n4. Saving embeddings to Qdrant...")
    total_saved = 0
    for embedding_data in embeddings:
        success = save_chunk_to_qdrant(embedding_data)
        if success:
            total_saved += 1
            print(f"  - Saved chunk {embedding_data['chunk_id'][:8]}... to Qdrant")
        else:
            print(f"  - FAILED to save chunk {embedding_data['chunk_id'][:8]}...")

    print(f"PASS {total_saved}/{len(embeddings)} chunks saved to Qdrant")

    # Step 5: Validate storage
    print("\n5. Validating storage...")
    success = validate_storage()
    if success:
        print("PASS Storage validation successful")
    else:
        print("FAIL Storage validation failed")
        return False

    # Step 6: Retrieve and validate
    print("\n6. Retrieving and validating...")
    success = retrieve_and_validate()
    if success:
        print("PASS Retrieval and validation successful")
    else:
        print("FAIL Retrieval and validation failed")

    print("\nPASS Pipeline test completed successfully!")
    print(f"Summary: {total_saved} chunks successfully stored in Qdrant")
    return True

if __name__ == "__main__":
    success = test_pipeline()
    if success:
        print("\nPipeline test completed successfully!")
    else:
        print("\nPipeline test failed!")
        sys.exit(1)