import qdrant_client
from qdrant_client import models
from typing import List, Dict, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from src.config.settings import settings
from src.models.chunk import ChunkCreate
from uuid import UUID
import json
import logging

class StorageService:
    def __init__(self):
        # Set up logging
        self.logger = logging.getLogger(__name__)

        # Initialize Qdrant client
        self.qdrant_client = qdrant_client.QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )

        # Initialize Neon Postgres connection
        try:
            self.neon_connection = psycopg2.connect(settings.neon_db_url)
            self.logger.info("Neon Postgres connection established")
        except Exception as e:
            self.logger.error(f"Failed to connect to Neon Postgres: {e}", exc_info=True)
            raise

        # Ensure database tables exist
        self._initialize_database()

        # Ensure collection exists in Qdrant
        self._ensure_collection()

    def _initialize_database(self):
        """
        Initialize database tables if they don't exist
        """
        try:
            self.logger.info("Initializing database tables")
            with self.neon_connection.cursor() as cursor:
                # Create chunks table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS chunks (
                        id UUID PRIMARY KEY,
                        book_id UUID NOT NULL,
                        text TEXT NOT NULL,
                        metadata JSONB,
                        chunk_index INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Create books table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS books (
                        id UUID PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        author VARCHAR(255),
                        content_type VARCHAR(10) NOT NULL,
                        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        chunk_strategy VARCHAR(50),
                        total_chunks INTEGER DEFAULT 0,
                        status VARCHAR(20) DEFAULT 'PROCESSING',
                        file_path VARCHAR(500),
                        description TEXT,
                        language VARCHAR(10) DEFAULT 'en'
                    )
                """)

                self.neon_connection.commit()
                self.logger.info("Database tables initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}", exc_info=True)
            raise

    from qdrant_client import models

    def _ensure_collection(self):
        """
        Ensure the Qdrant collection exists and has required payload indexes
        """
        try:
            self.logger.info("Ensuring Qdrant collection exists")

            collections = self.qdrant_client.get_collections()
            collection_names = [c.name for c in collections.collections]
            
            if settings.qdrant_collection_name not in collection_names:
                self.logger.info(f"Creating Qdrant collection: {settings.qdrant_collection_name}")
                self.qdrant_client.create_collection(
                    collection_name=settings.qdrant_collection_name,
                    vectors_config=models.VectorParams(
                        size=1024,  # embed-english-v3.0
                        distance=models.Distance.COSINE,
                        ), 
                )
                self.logger.info("Qdrant collection created")

        # Always ensure payload index exists
            try:
                self.qdrant_client.create_payload_index(
                    collection_name=settings.qdrant_collection_name,
                    field_name="book_id",
                    field_schema=models.PayloadSchemaType.KEYWORD,
                    )
                self.logger.info("Payload index for 'book_id' created")

            except Exception as e:
            # Index already exists → safe to ignore
                if "already exists" in str(e).lower():
                    self.logger.info("Payload index for 'book_id' already exists")
                else:
                    raise

        except Exception as e:
            self.logger.error("Failed to ensure Qdrant collection", exc_info=True)
            raise

    def reconnect_neon_if_needed(self):
        """
        Reconnect to Neon if the connection is broken
        """
        try:
            # Test the connection
            with self.neon_connection.cursor() as cursor:
                cursor.execute("SELECT 1;")  # Simple test query
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            self.logger.warning("Neon connection lost, attempting to reconnect")
            self.neon_connection = psycopg2.connect(settings.neon_db_url)
            self.logger.info("Neon connection reestablished")

    def store_chunks(self, chunks: List[ChunkCreate], embeddings: List[List[float]]):
        """
        Store chunks in both Qdrant (vectors) and Neon Postgres (metadata)
        """
        try:
            self.logger.info(f"Storing {len(chunks)} chunks in storage (Qdrant and Neon Postgres)")

            # Prepare data for Qdrant
            points = []
            postgres_data = []

            for chunk, embedding in zip(chunks, embeddings):
                point_id = str(chunk.id)

                # Prepare point for Qdrant
                points.append(
                    models.PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload={
                            "book_id": str(chunk.book_id),
                            "chunk_index": chunk.chunk_index,
                            "metadata": chunk.metadata
                        }
                    )
                )

                # Prepare data for Neon Postgres
                postgres_data.append((
                    str(chunk.id),
                    str(chunk.book_id),
                    chunk.text,
                    json.dumps(chunk.metadata),
                    chunk.chunk_index
                ))

            # Upsert points to Qdrant
            self.qdrant_client.upsert(
                collection_name=settings.qdrant_collection_name,
                points=points
            )
            self.logger.info(f"Upserted {len(points)} vectors to Qdrant")

            # Insert metadata to Neon Postgres
            self.reconnect_neon_if_needed()
            with self.neon_connection.cursor() as cursor:
                insert_query = """
                    INSERT INTO chunks (id, book_id, text, metadata, chunk_index)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        book_id = EXCLUDED.book_id,
                        text = EXCLUDED.text,
                        metadata = EXCLUDED.metadata,
                        chunk_index = EXCLUDED.chunk_index
                """
                cursor.executemany(insert_query, postgres_data)
                self.neon_connection.commit()
                self.logger.info(f"Stored {len(chunks)} chunk metadata records in Neon Postgres")

        except Exception as e:
            self.logger.error(f"Error storing chunks: {e}", exc_info=True)
            raise
    def search_chunks(
            self,
            query_embedding: List[float],
            book_id: Optional[UUID] = None,
            limit: int = 5) -> List[Dict]:
        """
        Search for relevant chunks based on query embedding
        """
        try:
            self.logger.info(
                f"Searching for chunks, limit: {limit}, book_id: {book_id}"
                )
            filters = None
            if book_id:
                filters = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="book_id",
                            match=models.MatchValue(value=str(book_id))
                    )
                ]
            )

        # Query Qdrant
            search_results = self.qdrant_client.query_points(
                collection_name=settings.qdrant_collection_name,
                query=query_embedding,
                query_filter=filters,
                limit=limit
                )

            results = []

        # IMPORTANT: iterate over search_results.points
            for hit in search_results.points:
                 results.append({
                    "id": hit.id,
                    "score": hit.score,
                    "payload": hit.payload,
                    "text": self.get_chunk_text(str(hit.id))
                    })

            self.logger.info(
                f"Found {len(results)} relevant chunks for query"
                )
            return results

        except Exception as e:
            self.logger.error(
                f"Error searching chunks: {e}",
                exc_info=True
            )
            raise


    def get_chunk_text(self, chunk_id: str) -> str:
        """
        Retrieve chunk text from Neon Postgres by chunk ID
        """
        try:
            self.logger.debug(f"Retrieving text for chunk ID: {chunk_id}")

            self.reconnect_neon_if_needed()
            with self.neon_connection.cursor() as cursor:
                cursor.execute(
                    "SELECT text FROM chunks WHERE id = %s",
                    (chunk_id,)
                )
                result = cursor.fetchone()

                if result:
                    text = result[0]
                    self.logger.debug(f"Successfully retrieved text (length: {len(text)}) for chunk ID: {chunk_id}")
                    return text
                else:
                    self.logger.warning(f"No chunk found with ID: {chunk_id}")
                    return ""
        except Exception as e:
            self.logger.error(f"Error retrieving chunk text for ID {chunk_id}: {e}", exc_info=True)
            raise

    def get_book_chunks(self, book_id: UUID) -> List[Dict]:
        """
        Retrieve all chunks for a specific book from Neon Postgres
        """
        try:
            self.logger.info(f"Retrieving all chunks for book ID: {book_id}")

            self.reconnect_neon_if_needed()
            with self.neon_connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT id, text, chunk_index, metadata FROM chunks WHERE book_id = %s ORDER BY chunk_index",
                    (str(book_id),)
                )
                results = cursor.fetchall()

                self.logger.info(f"Retrieved {len(results)} chunks for book ID: {book_id}")
                return results
        except Exception as e:
            self.logger.error(f"Error retrieving book chunks for book ID {book_id}: {e}", exc_info=True)
            raise

    def get_book_by_id(self, book_id: UUID):
        """
        Retrieve book details by ID from Neon Postgres
        """
        try:
            self.logger.debug(f"Retrieving book details for ID: {book_id}")

            self.reconnect_neon_if_needed()
            with self.neon_connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, title, status FROM books WHERE id = %s",
                    (str(book_id),)
                )
                result = cursor.fetchone()

                if not result:
                    self.logger.warning(f"Book with id {book_id} not found")
                    raise ValueError(f"Book with id {book_id} not found")

                book_data = {
                    'id': result[0],
                    'title': result[1],
                    'status': result[2]
                }

                self.logger.debug(f"Successfully retrieved book details for ID: {book_id}")
                return book_data
        except ValueError:
            raise
        except Exception as e:
            self.logger.error(f"Error retrieving book by ID {book_id}: {e}", exc_info=True)
            raise

storage_service = StorageService()