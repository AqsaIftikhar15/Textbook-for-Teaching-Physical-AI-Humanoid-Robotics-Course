from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, BackgroundTasks
from typing import Optional
from uuid import UUID
from src.models.book import BookCreate, ContentType, UploadBookResponse, BookStatusResponse, BookStatus
from src.services.ingestion import ingestion_service
from src.services.storage import storage_service
from src.services.embedding import embedding_service
from src.services.book_service import book_service
from src.config.settings import settings
from datetime import datetime
import tempfile
import os
import logging
from src.models.book import BookStatus

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)

# Dictionary to store processing status for books (in a real implementation, this would be in a database)
processing_status = {}

@router.post("/upload", response_model=UploadBookResponse)
async def upload_book(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Form(...),
    chunk_strategy: str = Form("semantic"),
    author: Optional[str] = Form(None),
    description: Optional[str] = Form(None)
):
    """
    Upload a book file (PDF, HTML, or text) for processing and indexing.
    """
    # Validate file type
    content_type = file.content_type
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in ['.pdf', '.html', '.htm', '.txt'] and content_type not in ['application/pdf', 'text/html', 'text/plain']:
        logger.error(f"Invalid file format upload: {file_ext}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Supported formats: PDF, HTML, TEXT"
        )

    # Check file size
    # Note: For large files, we might need to implement streaming or size checks differently
    # This is a basic size check and may need adjustment based on actual requirements
    if hasattr(file, 'size') and file.size > settings.max_file_size:
        logger.warning(f"File size exceeds limit: {file.size} bytes for file {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds limit of {settings.max_file_size} bytes"
        )

    # Create a temporary file to save the uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
        # Read and write the file content to the temporary file
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        # Determine content type based on file extension
        if file_ext == '.pdf':
            content_type_enum = ContentType.PDF
        elif file_ext in ['.html', '.htm']:
            content_type_enum = ContentType.HTML
        elif file_ext == '.txt':
            content_type_enum = ContentType.TEXT
        else:
            # Fallback based on content-type header
            if content_type == 'application/pdf':
                content_type_enum = ContentType.PDF
            elif content_type == 'text/html':
                content_type_enum = ContentType.HTML
            else:
                content_type_enum = ContentType.TEXT  # Default to text

        # Create book using the book service
        book_create = BookCreate(
            title=title,
            author=author or "Unknown Author",
            content_type=content_type_enum,
            chunk_strategy=chunk_strategy,
            description=description
        )

        book = book_service.create_book(book_create)
        book_id = str(book.id)

        # Add to processing status
        processing_status[book_id] = {
            "status": BookStatus.PROCESSING,
            "total_chunks": 0,
            "processed_chunks": 0,
            "error_message": None
        }

        # Process the book in the background
        background_tasks.add_task(process_book_async, book_id, temp_file_path, content_type_enum.value, chunk_strategy)

        logger.info(f"Book {book_id} upload initiated")
        return UploadBookResponse(
            status="accepted",
            book_id=book_id,
            message="Book is being processed and will be available shortly"
        )
    except HTTPException:
        # Clean up the temporary file in case of HTTP exceptions
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise
    except Exception as e:
        # Clean up the temporary file in case of error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )

def process_book_async(book_id: str, file_path: str, content_type: str, chunk_strategy: str):
    """
    Process the book asynchronously - extract text, chunk, embed, and store
    This would normally run in a background task queue
    """
    try:
        logger.info(f"Starting async processing for book {book_id}")

        # Update status to processing
        processing_status[book_id]["status"] = BookStatus.PROCESSING

        # Process the book: extract, chunk, embed
        chunks = ingestion_service.process_book(file_path, content_type, book_id, chunk_strategy)

        logger.info(f"Book {book_id} text extracted and chunked ({len(chunks)} chunks)")

        # Generate embeddings for the chunks
        chunk_texts = [chunk.text for chunk in chunks]
        embeddings = embedding_service.embed_text(chunk_texts)

        logger.info(f"Book {book_id} embeddings generated")

        # Store chunks in vector db (Qdrant) and metadata db (Neon)
        storage_service.store_chunks(chunks, embeddings)

        logger.info(f"Book {book_id} chunks stored in vector and metadata databases")

        # Update book record with completion info using book service
        from src.models.book import BookUpdateStatus
        status_update = BookUpdateStatus(
            status=BookStatus.READY,
            total_chunks=len(chunks)
        )
        book_service.update_book_status(UUID(book_id), status_update)

        logger.info(f"Book {book_id} status updated to READY")

        # Update processing status
        processing_status[book_id] = {
            "status": BookStatus.READY,
            "total_chunks": len(chunks),
            "processed_chunks": len(chunks),
            "error_message": None
        }

        logger.info(f"Processing completed for book {book_id}")

        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Temporary file {file_path} removed")
    except Exception as e:
        logger.error(f"Error during async processing for book {book_id}: {str(e)}", exc_info=True)
        # Update processing status with error
        processing_status[book_id] = {
            "status": BookStatus.ERROR,
            "total_chunks": 0,
            "processed_chunks": 0,
            "error_message": str(e)
        }

@router.get("/status/{book_id}", response_model=BookStatusResponse)
async def get_book_status(book_id: str):
    """
    Get the processing status of an uploaded book.
    """
    logger.info(f"Checking status for book {book_id}")

    # Try to get the book from the database
    try:
        book = book_service.get_book(UUID(book_id))
    except ValueError:
        logger.warning(f"Book ID not found: {book_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book ID not found"
        )
    except Exception as e:
        logger.error(f"Error retrieving book {book_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving book: {str(e)}"
        )

    # Get status from processing queue if available, otherwise from db
    status_info = processing_status.get(book_id, None)

    if status_info:
        status_val = status_info["status"].value if isinstance(status_info["status"], BookStatus) else str(status_info["status"])
        total_chunks = status_info.get("total_chunks", book.total_chunks) or 0
        processed_chunks = status_info.get("processed_chunks", 0)
        error_message = status_info.get("error_message", None)
    else:
        # If not in processing queue, use DB info
        status_val = book.status.value
        total_chunks = book.total_chunks
        processed_chunks = total_chunks
        error_message = None

    # Calculate progress
    progress = 0.0
    if total_chunks > 0:
        progress = min(1.0, processed_chunks / total_chunks) if processed_chunks > 0 else 0.0

    logger.info(f"Status for book {book_id}: {status_val}, progress: {progress}")

    return BookStatusResponse(
        book_id=book_id,
        status=status_val,
        title=book.title,
        progress=progress,
        total_chunks=total_chunks,
        processed_chunks=processed_chunks,
        error_message=error_message
    )