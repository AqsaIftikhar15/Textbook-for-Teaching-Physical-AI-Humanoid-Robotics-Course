from typing import List, Dict
from src.services.storage import storage_service
from src.services.embedding import embedding_service
from src.services.ingestion import ingestion_service
from src.models.query import QueryCreate, QueryResponse, Query, QueryType
from src.config.settings import settings
from uuid import uuid4
from datetime import datetime
import time
import cohere
import logging

class RAGService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = cohere.Client(settings.cohere_api_key)
        self.generation_model = settings.cohere_generation_model

    def query_full_book(self, book_id: str, query_text: str, max_results: int = 5,
                       temperature: float = 0.7) -> QueryResponse:
        """
        Perform a full-book query using RAG approach
        """
        start_time = time.time()
        self.logger.info(f"Starting full-book query for book_id: {book_id}, query: {query_text[:100]}...")

        try:
            # Generate embedding for the query
            self.logger.debug("Generating embedding for query")
            query_embedding = embedding_service.embed_query(query_text)

            # Search for relevant chunks in the specified book
            self.logger.debug(f"Searching for relevant chunks in book_id: {book_id}")
            search_results = storage_service.search_chunks(
                query_embedding=query_embedding,
                book_id=book_id,
                limit=max_results
            )

            if not search_results:
                self.logger.info(f"No relevant results found for query in book_id: {book_id}")
                return QueryResponse(
                    query_id=uuid4(),
                    response="No relevant information found in the book for your query.",
                    citations=[],
                    query_time=time.time() - start_time,
                    tokens_used=0
                )

            # Format context from retrieved chunks
            context_parts = []
            citations = []

            for result in search_results:
                context_parts.append(result['text'])
                citations.append({
                    'chunk_id': result['id'],
                    'text': result['text'][:200] + "..." if len(result['text']) > 200 else result['text'],  # Truncate for citation
                    'similarity_score': result['score']
                })

            context = "\n\n".join(context_parts)

            # Generate response using the context and query
            prompt = f"""
            Context information is below.
            ---------------------
            {context}
            ---------------------
            Given the context information and not prior knowledge, answer the question: {query_text}
            If the context does not provide enough information to answer the question, respond with: "I couldn't find relevant information in the provided text to answer your question."
            """

            self.logger.debug("Sending generation request to Cohere")
            try:
                response = self.client.generate(
                    model=self.generation_model,
                    prompt=prompt,
                    max_tokens=300,  # Adjust based on requirements
                    temperature=temperature
                )
            except Exception as e:
                self.logger.error(f"Error communicating with Cohere API: {e}", exc_info=True)
                raise

            generated_text = response.generations[0].text.strip()

            # Count tokens (approximate)
            tokens_used = len(generated_text.split())

            response_time = time.time() - start_time
            self.logger.info(f"Full-book query completed successfully in {response_time:.2f}s for book_id: {book_id}")

            return QueryResponse(
                query_id=uuid4(),
                response=generated_text,
                citations=citations,
                query_time=response_time,
                tokens_used=tokens_used
            )
        except Exception as e:
            self.logger.error(f"Error in full-book query for book_id {book_id}: {e}", exc_info=True)
            raise

    def query_selected_text(self, selected_text: str, query: str,
                           temperature: float = 0.7) -> QueryResponse:
        """
        Perform a query based only on the provided selected text
        """
        start_time = time.time()
        self.logger.info(f"Starting selected-text query, query: {query[:100]}...")

        try:
            # Generate response using only the selected text as context
            prompt = f"""
            Context information is below.
            ---------------------
            {selected_text}
            ---------------------
            Given the context information and not prior knowledge, answer the question: {query}
            If the context does not provide enough information to answer the question, respond with: "I couldn't find relevant information in the provided text to answer your question."
            """

            self.logger.debug("Sending selected-text generation request to Cohere")
            try:
                response = self.client.generate(
                    model=self.generation_model,
                    prompt=prompt,
                    max_tokens=300,  # Adjust based on requirements
                    temperature=temperature
                )
            except Exception as e:
                self.logger.error(f"Error communicating with Cohere API: {e}", exc_info=True)
                raise

            generated_text = response.generations[0].text.strip()

            # Count tokens (approximate)
            tokens_used = len(generated_text.split())

            response_time = time.time() - start_time
            self.logger.info(f"Selected-text query completed successfully in {response_time:.2f}s")

            return QueryResponse(
                query_id=uuid4(),
                response=generated_text,
                citations=[],  # No citations for selected-text mode
                query_time=response_time,
                tokens_used=tokens_used
            )
        except Exception as e:
            self.logger.error(f"Error in selected-text query: {e}", exc_info=True)
            raise

rag_service = RAGService()