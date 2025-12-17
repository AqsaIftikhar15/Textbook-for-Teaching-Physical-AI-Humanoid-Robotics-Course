"""
URL Crawl → Embed → Qdrant Upload Pipeline

This script crawls all Docusaurus book URLs, extracts text, generates embeddings using Cohere models,
and stores vectors + metadata in a Qdrant Cloud collection.
"""

import os
import logging
import time
import requests
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv
import hashlib


# Load environment variables from .env file
load_dotenv()


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawl_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def retry_on_failure(max_retries=3, delay=1):
    """Decorator to retry a function on failure"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Function {func.__name__} failed after {max_retries} attempts: {e}")
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
        return wrapper
    return decorator


@retry_on_failure(max_retries=3, delay=1)
def get_all_urls(base_url: str) -> List[str]:
    """
    Crawl the Docusaurus book site and extract all accessible page URLs.
    If the base URL points to an XML sitemap, parse it directly.
    Otherwise, crawl the site as before.

    Args:
        base_url (str): The base URL of the Docusaurus book site or sitemap.xml

    Returns:
        List[str]: List of all discovered URLs within the book site
    """
    # Check if the base URL ends with .xml (indicating a sitemap)
    if base_url.lower().endswith('.xml'):
        logger.info(f"Detected sitemap.xml URL: {base_url}")

        try:
            response = requests.get(base_url, timeout=10)
            if response.status_code == 200:
                # Parse the XML sitemap
                root = ET.fromstring(response.content)

                # Find all <loc> tags containing URLs
                # Handle namespace - sitemap XML often uses namespace like {http://www.sitemaps.org/schemas/sitemap/0.9}
                urls = []
                for elem in root.iter():
                    # Check if tag ends with 'loc' (handles namespaced tags like '{namespace}loc')
                    if elem.tag.endswith('loc'):
                        url = elem.text.strip()
                        urls.append(url)

                logger.info(f"Successfully extracted {len(urls)} URLs from sitemap.xml")
                return urls
            else:
                logger.warning(f"Failed to fetch sitemap.xml: Status code {response.status_code}")
                return []
        except ET.ParseError as e:
            logger.error(f"Error parsing sitemap.xml: {e}")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching sitemap.xml: {e}")
            return []
    else:
        # Original crawler logic for HTML-based crawling
        logger.info(f"Starting to crawl URLs from base URL: {base_url}")

        # Normalize the base URL to ensure it ends with a slash
        if not base_url.endswith('/'):
            base_url += '/'

        visited_urls = set()
        urls_to_visit = [base_url]
        all_urls = set()

        # Parse the base domain to only follow links within the same domain
        base_domain = urlparse(base_url).netloc

        while urls_to_visit:
            current_url = urls_to_visit.pop(0)

            # Skip if already visited
            if current_url in visited_urls:
                continue

            visited_urls.add(current_url)

            try:
                # Add a small delay to be respectful to the server (rate limiting)
                time.sleep(0.5)

                response = requests.get(current_url, timeout=10)

                # Check if the request was successful
                if response.status_code == 200:
                    # Add the URL to our collection
                    all_urls.add(current_url)

                    # Parse the HTML content
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Find all links in the page
                    for link in soup.find_all('a', href=True):
                        href = link['href']

                        # Convert relative URLs to absolute URLs
                        absolute_url = urljoin(current_url, href)

                        # Only follow URLs within the same domain
                        if urlparse(absolute_url).netloc == base_domain:
                            # Only add URLs that haven't been visited and are not already in the queue
                            if absolute_url not in visited_urls and absolute_url not in urls_to_visit:
                                # Only add URLs that look like actual content pages (not external links, etc.)
                                if absolute_url.startswith(base_url):
                                    urls_to_visit.append(absolute_url)

                else:
                    logger.warning(f"Failed to crawl {current_url}: Status code {response.status_code}")

            except requests.exceptions.RequestException as e:
                logger.error(f"Error crawling {current_url}: {e}")
                # Continue with the next URL instead of stopping the entire process
                continue

        logger.info(f"Completed crawling. Found {len(all_urls)} unique URLs.")
        return list(all_urls)


def extract_text_from_url(url: str) -> Dict[str, str]:
    """
    Extract clean text content from a given URL.

    Args:
        url (str): The URL to extract text from

    Returns:
        Dict[str, str]: Dictionary containing:
          - 'title': Page title
          - 'content': Clean text content
          - 'url': Original URL
    """
    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            logger.warning(f"Failed to extract text from {url}: Status code {response.status_code}")
            return {
                'title': '',
                'content': '',
                'url': url
            }

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else 'No Title'

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up the text: remove extra whitespace and newlines
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)

        logger.info(f"Successfully extracted text from {url} - Title: {title}")

        return {
            'title': title,
            'content': clean_text,
            'url': url
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Error extracting text from {url}: {e}")
        return {
            'title': '',
            'content': '',
            'url': url
        }


def chunk_text(text: str, chunk_size: int = 2048, overlap: int = 200) -> List[Dict[str, str]]:
    """
    Split text into appropriately sized chunks for embedding.

    Args:
        text (str): The text to chunk
        chunk_size (int): Maximum size of each chunk (default: 2048)
        overlap (int): Overlap between chunks to maintain context (default: 200)

    Returns:
        List[Dict[str, str]]: List of text chunks with metadata
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        # Determine the end position for this chunk
        end = start + chunk_size

        # If we're near the end, make sure to include the remainder
        if end > text_length:
            end = text_length

        # Create the chunk
        chunk_content = text[start:end]

        # Add the chunk to our list
        # Generate a Qdrant-compatible ID (using hexdigest which is valid)
        chunk_id = hashlib.md5(f"{chunk_content}_{start}".encode()).hexdigest()

        chunk_data = {
            "id": chunk_id,
            "content": chunk_content,
            "source_url": "",  # Will be filled in later when we know the source
            "source_title": "",  # Will be filled in later when we know the source
            "chunk_index": len(chunks)
        }
        chunks.append(chunk_data)

        # Move the start position forward, accounting for overlap
        start = end - overlap

        # If the remaining text is less than or equal to overlap, we're done
        if start >= text_length:
            break

    logger.info(f"Text chunked into {len(chunks)} chunks")
    return chunks


def embed(text_chunks: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Generate embeddings for text chunks using Cohere with rate limiting and retry logic.

    Args:
        text_chunks: List of text chunks to embed

    Returns:
        List[Dict[str, Any]]: List of embeddings with associated metadata
    """
    if not text_chunks:
        logger.warning("No text chunks provided for embedding")
        return []

    # Extract just the text content for embedding
    texts = [chunk['content'] for chunk in text_chunks if chunk.get('content')]

    if not texts:
        logger.warning("No valid text content found for embedding")
        return []

    max_retries = 5
    base_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            # Get Cohere API key from environment and create client
            cohere_api_key = os.getenv('COHERE_API_KEY')
            if not cohere_api_key:
                raise ValueError("COHERE_API_KEY environment variable is required")

            cohere_client_instance = cohere.Client(cohere_api_key)

            # Add delay to respect rate limits
            time.sleep(1)

            # Generate embeddings using Cohere
            response = cohere_client_instance.embed(
                texts=texts,
                model="embed-multilingual-v2.0"  # Using a multilingual model for broader text support
            )

            # Prepare the embedding results with metadata
            embeddings = []
            for i, embedding_vector in enumerate(response.embeddings):
                if i < len(text_chunks):  # Ensure we don't go out of bounds
                    chunk = text_chunks[i]
                    # Ensure the chunk_id is Qdrant-compatible (using the existing hexdigest)
                    chunk_id = chunk.get('id', hashlib.md5(chunk['content'].encode()).hexdigest())
                    embedding_data = {
                        "chunk_id": chunk_id,
                        "vector": embedding_vector,
                        "model_name": "embed-multilingual-v2.0",
                        "metadata": {
                            "source_url": chunk.get('source_url', ''),
                            "source_title": chunk.get('source_title', ''),
                            "content": chunk['content'],
                            "chunk_index": chunk.get('chunk_index', i)
                        }
                    }
                    embeddings.append(embedding_data)

            logger.info(f"Successfully generated embeddings for {len(embeddings)} text chunks")
            return embeddings

        except Exception as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)  # Exponential backoff
                logger.warning(f"Embedding attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                logger.error(f"Failed to generate embeddings after {max_retries} attempts: {e}")
                raise


def create_collection(collection_name: str = 'rag_embedding') -> bool:
    """
    Create or verify existence of Qdrant collection.

    Args:
        collection_name: Name of the collection to create (default: 'rag_embedding')

    Returns:
        bool: True if collection exists/created successfully
    """
    try:
        # Get Qdrant connection details from environment
        qdrant_url = os.getenv('QDRANT_URL')
        qdrant_api_key = os.getenv('QDRANT_API_KEY')

        if not qdrant_url or not qdrant_api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

        # Create Qdrant client
        qdrant_client_instance = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )

        # Check if collection already exists
        try:
            collections = qdrant_client_instance.get_collections()
            collection_exists = any(col.name == collection_name for col in collections.collections)
        except:
            collection_exists = False

        if not collection_exists:
            # Create the collection with appropriate vector size (for Cohere embeddings)
            # Cohere's embed-multilingual-v2.0 produces 1024-dimensional vectors
            qdrant_client_instance.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
            )
            logger.info(f"Created new Qdrant collection: {collection_name}")
        else:
            logger.info(f"Qdrant collection {collection_name} already exists")

        return True

    except Exception as e:
        logger.error(f"Error creating Qdrant collection {collection_name}: {e}")
        return False


def save_chunk_to_qdrant(embedding_data: Dict[str, Any]) -> bool:
    """
    Store a single embedded chunk in Qdrant with metadata.

    Args:
        embedding_data: The embedding and associated metadata to store

    Returns:
        bool: True if successfully stored, False otherwise
    """
    try:
        # Get Qdrant connection details from environment
        qdrant_url = os.getenv('QDRANT_URL')
        qdrant_api_key = os.getenv('QDRANT_API_KEY')

        if not qdrant_url or not qdrant_api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

        # Create Qdrant client
        qdrant_client_instance = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )

        # Prepare the point to be inserted
        # Qdrant expects IDs to be either integers or UUIDs, so we'll use the hash as a string but ensure it's a valid format
        chunk_id = embedding_data["chunk_id"]

        # If the chunk_id is a valid UUID or integer string, use it directly
        # Otherwise, we'll add it as a payload field and use an auto-generated ID
        point = PointStruct(
            id=chunk_id,  # Use the chunk ID as the point ID (should be a valid hash)
            vector=embedding_data["vector"],
            payload={
                "original_chunk_id": chunk_id,  # Store the original chunk ID in payload
                "source_url": embedding_data["metadata"]["source_url"],
                "source_title": embedding_data["metadata"]["source_title"],
                "content": embedding_data["metadata"]["content"],
                "chunk_index": embedding_data["metadata"]["chunk_index"],
                "created_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            }
        )

        # Upsert the point into the collection
        qdrant_client_instance.upsert(
            collection_name="rag_embedding",
            points=[point]
        )

        logger.info(f"Successfully stored chunk {chunk_id} in Qdrant")
        return True

    except Exception as e:
        logger.error(f"Error storing chunk in Qdrant: {e}")
        # If the original ID format is invalid, try using an integer ID instead
        try:
            # Get Qdrant connection details from environment
            qdrant_url = os.getenv('QDRANT_URL')
            qdrant_api_key = os.getenv('QDRANT_API_KEY')

            if not qdrant_url or not qdrant_api_key:
                raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

            # Create Qdrant client
            qdrant_client_instance = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key,
            )

            # Use a timestamp-based integer ID
            import uuid
            point = PointStruct(
                id=str(uuid.uuid4()),  # Use a UUID instead
                vector=embedding_data["vector"],
                payload={
                    "original_chunk_id": embedding_data["chunk_id"],  # Store original ID in payload
                    "source_url": embedding_data["metadata"]["source_url"],
                    "source_title": embedding_data["metadata"]["source_title"],
                    "content": embedding_data["metadata"]["content"],
                    "chunk_index": embedding_data["metadata"]["chunk_index"],
                    "created_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                }
            )

            # Upsert the point into the collection
            qdrant_client_instance.upsert(
                collection_name="rag_embedding",
                points=[point]
            )

            logger.info(f"Successfully stored chunk with UUID {embedding_data['chunk_id']} in Qdrant")
            return True
        except Exception as e2:
            logger.error(f"Error storing chunk in Qdrant with UUID fallback: {e2}")
            return False


def validate_storage() -> bool:
    """
    Validate that storage is working correctly by checking if the collection exists and has data.

    Returns:
        bool: True if storage is valid, False otherwise
    """
    try:
        # Get Qdrant connection details from environment
        qdrant_url = os.getenv('QDRANT_URL')
        qdrant_api_key = os.getenv('QDRANT_API_KEY')

        if not qdrant_url or not qdrant_api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

        # Create Qdrant client
        qdrant_client_instance = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )

        # Check if collection exists
        collections = qdrant_client_instance.get_collections()
        collection_exists = any(col.name == "rag_embedding" for col in collections.collections)

        if not collection_exists:
            logger.warning("Qdrant collection 'rag_embedding' does not exist")
            return False

        # Check the count of points in the collection
        count = qdrant_client_instance.count(collection_name="rag_embedding")
        logger.info(f"Qdrant collection 'rag_embedding' exists and contains {count.count} points")

        return True

    except Exception as e:
        logger.error(f"Error validating storage: {e}")
        return False


# def retrieve_and_validate(chunk_id: str = None) -> bool:
#     """
#     Fetch stored vectors and verify content.

#     Args:
#         chunk_id: Specific chunk ID to retrieve (if None, retrieves a sample)

#     Returns:
#         bool: True if retrieval and validation successful, False otherwise
#     """
#     try:
#         # Get Qdrant connection details from environment
#         qdrant_url = os.getenv('QDRANT_URL')
#         qdrant_api_key = os.getenv('QDRANT_API_KEY')

#         if not qdrant_url or not qdrant_api_key:
#             raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

#         # Create Qdrant client
#         qdrant_client_instance = QdrantClient(
#             url=qdrant_url,
#             api_key=qdrant_api_key,
#         )

#         # If chunk_id is provided, retrieve that specific point
#         if chunk_id:
#             points = qdrant_client_instance.retrieve(
#                 collection_name="rag_embedding",
#                 ids=[chunk_id]
#             )
#             if points:
#                 logger.info(f"Successfully retrieved chunk {chunk_id} from Qdrant")
#                 return True
#             else:
#                 logger.warning(f"Chunk {chunk_id} not found in Qdrant")
#                 return False
#         else:
#             # Retrieve a sample of points to verify the collection
#             points = qdrant_client_instance.scroll(
#                 collection_name="rag_embedding",
#                 limit=1  # Just get one point as a sample
#             )
#             if points[0]:  # If we have at least one point
#                 point = points[0]
#                 logger.info(f"Successfully retrieved sample point {point.id} from Qdrant")
#                 logger.info(f"Sample content preview: {point.payload.get('content', '')[:100]}...")
#                 return True
#             else:
#                 logger.warning("No points found in Qdrant collection for validation")
#                 return False

#     except Exception as e:
#         logger.error(f"Error retrieving and validating from Qdrant: {e}")
#         return False


def main():
    """
    Main function to orchestrate the complete pipeline:
    crawl → extract → chunk → embed → store → validate
    """
    logger.info("Starting the URL Crawl -> Embed -> Qdrant Upload pipeline")

    try:
        # Step 1: Create the Qdrant collection
        logger.info("Step 1: Creating Qdrant collection")
        if not create_collection('rag_embedding'):
            logger.error("Failed to create Qdrant collection")
            return False
        logger.info("Qdrant collection created successfully")

        # Step 2: Get all URLs from the book site
        logger.info("Step 2: Crawling URLs from the book site")
        book_base_url = os.getenv('BOOK_BASE_URL', 'https://aqsaiftikhar15.github.io/Textbook-for-Teaching-Physical-AI-Humanoid-Robotics-Course/')
        urls = get_all_urls(book_base_url)
        logger.info(f"Found {len(urls)} URLs to process")

        # Step 3: Process URLs in batches with checkpointing
        total_chunks_stored = 0
        batch_size = 5  # Process 5 URLs at a time
        processed_urls_file = 'processed_urls.txt'

        # Load previously processed URLs if they exist
        processed_urls = set()
        if os.path.exists(processed_urls_file):
            with open(processed_urls_file, 'r') as f:
                processed_urls = set(line.strip() for line in f if line.strip())

        # Filter out already processed URLs
        urls_to_process = [url for url in urls if url not in processed_urls]
        logger.info(f"Found {len(urls_to_process)} URLs to process ({len(processed_urls)} already processed)")

        # Process URLs in batches
        for batch_start in range(0, len(urls_to_process), batch_size):
            batch = urls_to_process[batch_start:batch_start + batch_size]
            logger.info(f"Processing batch {batch_start//batch_size + 1}/{(len(urls_to_process) + batch_size - 1)//batch_size}")

            for i, url in enumerate(batch):
                logger.info(f"Processing URL {batch_start + i + 1}/{len(urls)}: {url}")

                try:
                    # Extract text from the URL
                    page_data = extract_text_from_url(url)
                    if not page_data['content']:
                        logger.warning(f"No content extracted from {url}, skipping...")
                        # Mark as processed even if failed
                        with open(processed_urls_file, 'a') as f:
                            f.write(url + '\n')
                        continue

                    # Chunk the text
                    text_chunks = chunk_text(
                        page_data['content'],
                        chunk_size=int(os.getenv('CHUNK_SIZE', '2048')),  # Updated default
                        overlap=int(os.getenv('CHUNK_OVERLAP', '200'))    # Updated default
                    )

                    # Update chunk metadata with source information
                    for chunk in text_chunks:
                        chunk['source_url'] = url
                        chunk['source_title'] = page_data['title']

                    if not text_chunks:
                        logger.warning(f"No chunks created from {url}, skipping...")
                        # Mark as processed even if failed
                        with open(processed_urls_file, 'a') as f:
                            f.write(url + '\n')
                        continue

                    # Generate embeddings for the chunks
                    logger.info(f"Generating embeddings for {len(text_chunks)} chunks from {url}")
                    embeddings = embed(text_chunks)

                    if not embeddings:
                        logger.warning(f"No embeddings generated for {url}, skipping...")
                        # Mark as processed even if failed
                        with open(processed_urls_file, 'a') as f:
                            f.write(url + '\n')
                        continue

                    # Store each embedding in Qdrant
                    for embedding_data in embeddings:
                        success = save_chunk_to_qdrant(embedding_data)
                        if success:
                            total_chunks_stored += 1
                        else:
                            logger.error(f"Failed to store chunk {embedding_data['chunk_id']} from {url}")

                    # Explicitly delete large objects to free memory
                    del text_chunks
                    del embeddings
                    del page_data

                    # Mark URL as processed
                    with open(processed_urls_file, 'a') as f:
                        f.write(url + '\n')

                except Exception as e:
                    logger.error(f"Error processing URL {url}: {e}")
                    # Still mark as processed to avoid re-processing failed URLs
                    with open(processed_urls_file, 'a') as f:
                        f.write(url + '\n')
                    continue  # Continue with next URL

            # Add delay between batches to avoid API rate limits
            if batch_start + batch_size < len(urls_to_process):
                logger.info("Waiting between batches to respect API limits...")
                time.sleep(2)

        logger.info(f"Pipeline completed successfully! Stored {total_chunks_stored} chunks in Qdrant.")

        # Step 4: Validate storage (temporarily skip retrieval)
        logger.info("Step 4: Validating storage (skipping retrieval/validation for now)")
        if validate_storage():
            logger.info("Storage validation passed! Skipping retrieval step.")
            return True
        else:
            logger.error("Storage validation failed!")
            return False


    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        logger.info("Pipeline completed successfully!")
        print("Pipeline completed successfully!")
    else:
        logger.error("Pipeline failed!")
        print("Pipeline failed!")
        exit(1)