from fastapi import APIRouter, HTTPException, status
from src.models.query import QueryCreate, QueryResponse, FullBookQuery, SelectedTextQuery
from src.services.rag import rag_service
from src.services.storage import storage_service
from uuid import UUID
import logging

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)

@router.post("/full", response_model=QueryResponse)
async def query_full_book(query_data: FullBookQuery):
    """
    Query the system using full book content for context.
    This mode allows the system to draw from the entire book to answer the question.
    """
    logger.info(f"Full-book query requested for book ID: {query_data.book_id}")

    # Verify book exists and is ready
    try:
        book = storage_service.get_book_by_id(query_data.book_id)
        if book['status'] != "READY":
            logger.warning(f"Book {query_data.book_id} is not ready for querying. Status: {book['status']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book is not ready for querying. Current status: {book['status']}"
            )
    except ValueError:
        logger.warning(f"Book with ID {query_data.book_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {query_data.book_id} not found"
        )
    except Exception as e:
        logger.error(f"Error accessing book information for {query_data.book_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error accessing book information: {str(e)}"
        )

    # Perform the full-book query
    try:
        response = rag_service.query_full_book(
            book_id=str(query_data.book_id),
            query_text=query_data.query,
            max_results=query_data.max_results,
            temperature=query_data.temperature
        )
        logger.info(f"Full-book query for book {query_data.book_id} completed successfully")
        return response
    except Exception as e:
        logger.error(f"Error processing full-book query for {query_data.book_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )

@router.post("/selected", response_model=QueryResponse)
async def query_selected_text(query_data: SelectedTextQuery):
    """
    Query the system using only the provided selected text passage.
    This mode responds exclusively based on the provided text without referencing other parts of the book.
    """
    logger.info("Selected-text query requested")

    # Validate that selected text is provided
    if not query_data.selected_text or not query_data.selected_text.strip():
        logger.warning("Selected text query received with empty text")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected text cannot be empty"
        )

    # Perform the selected-text query
    try:
        response = rag_service.query_selected_text(
            selected_text=query_data.selected_text,
            query=query_data.query,
            temperature=query_data.temperature
        )
        logger.info("Selected-text query completed successfully")
        return response
    except Exception as e:
        logger.error(f"Error processing selected-text query: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )