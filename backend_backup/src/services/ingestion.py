import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import re
from typing import List
from src.models.chunk import ChunkCreate
from src.services.embedding import embedding_service
from src.services.storage import storage_service
from src.config.settings import settings
from uuid import uuid4
from datetime import datetime
import hashlib
import unicodedata
import logging
from uuid import UUID

class IngestionService:
    def __init__(self):
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
        self.logger = logging.getLogger(__name__)

    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text by cleaning and normalizing it
        """
        try:
            self.logger.debug("Starting text preprocessing")

            # Normalize unicode characters
            text = unicodedata.normalize('NFKD', text)

            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text)

            # Remove special characters but keep basic punctuation
            # This keeps letters, numbers, basic punctuation, and spaces
            text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\'\" ]', ' ', text)

            # Fix common text issues
            text = text.replace('\u00a0', ' ')  # Non-breaking space to regular space
            text = text.replace('\u200b', '')   # Zero-width space removal

            # Remove extra spaces again after cleanup
            text = re.sub(r'\s+', ' ', text).strip()

            self.logger.debug("Text preprocessing completed")
            return text
        except Exception as e:
            self.logger.error(f"Error during text preprocessing: {e}", exc_info=True)
            raise

    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text from PDF file using PyMuPDF
        """
        try:
            self.logger.info(f"Extracting text from PDF: {file_path}")

            doc = fitz.open(file_path)
            text = ""
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text += page.get_text()
            doc.close()

            self.logger.info(f"Successfully extracted text from PDF: {file_path}, length: {len(text)}")

            # Preprocess the extracted text
            text = self.preprocess_text(text)
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF {file_path}: {e}", exc_info=True)
            raise

    def extract_text_from_html(self, file_path: str) -> str:
        """
        Extract text from HTML file using BeautifulSoup
        """
        try:
            self.logger.info(f"Extracting text from HTML: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            soup = BeautifulSoup(content, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text()
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            self.logger.info(f"Successfully extracted text from HTML: {file_path}, length: {len(text)}")

            # Preprocess the extracted text
            text = self.preprocess_text(text)
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text from HTML {file_path}: {e}", exc_info=True)
            raise

    def extract_text_from_txt(self, file_path: str) -> str:
        """
        Extract text from TXT file
        """
        try:
            self.logger.info(f"Extracting text from TXT: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            self.logger.info(f"Successfully extracted text from TXT: {file_path}, length: {len(text)}")

            # Preprocess the extracted text
            text = self.preprocess_text(text)
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text from TXT {file_path}: {e}", exc_info=True)
            raise

    def chunk_text(self, text: str, strategy: str = "semantic") -> List[str]:
        """
        Chunk text based on the specified strategy
        """
        try:
            self.logger.debug(f"Starting text chunking with strategy: {strategy}")

            if strategy == "semantic":
                result = self._semantic_chunking(text)
            elif strategy == "overlapping":
                result = self._overlapping_chunking(text)
            else:
                result = self._fixed_size_chunking(text)

            self.logger.info(f"Text chunking completed. Created {len(result)} chunks using {strategy} strategy.")
            return result
        except Exception as e:
            self.logger.error(f"Error during text chunking: {e}", exc_info=True)
            raise

    def _fixed_size_chunking(self, text: str) -> List[str]:
        """
        Split text into fixed-size chunks
        """
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk = text[i:i + self.chunk_size]
            if chunk.strip():  # Only add non-empty chunks
                chunks.append(chunk)
        return chunks

    def _overlapping_chunking(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks
        """
        chunks = []
        start = 0

        while start < len(text):
            # Get a chunk of the desired size
            end = start + self.chunk_size
            chunk = text[start:end]

            # If we're near the end and the chunk is too small, include it with the previous one
            if end >= len(text) and len(chunk) < self.chunk_size // 2 and chunks:
                chunks[-1] += chunk  # Append to previous chunk
                break

            if chunk.strip():  # Only add non-empty chunks
                chunks.append(chunk)

            # Move the start position by chunk_size minus overlap
            start = end - self.chunk_overlap

        return chunks

    def _semantic_chunking(self, text: str) -> List[str]:
        """
        Attempt to chunk text semantically by sentences or paragraphs
        """
        try:
            # Split by paragraphs first
            paragraphs = text.split('\n\n')
            chunks = []
            current_chunk = ""

            for paragraph in paragraphs:
                # If adding the paragraph would exceed the chunk size
                if len(current_chunk) + len(paragraph) > self.chunk_size and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                else:
                    # Add to current chunk
                    if current_chunk:
                        current_chunk += "\n\n" + paragraph
                    else:
                        current_chunk = paragraph

                # If current chunk is getting large, split it further
                if len(current_chunk) > self.chunk_size:
                    # Try to split by sentences
                    sentences = re.split(r'(?<=[.!?])\s+', current_chunk)
                    temp_chunk = ""

                    for sentence in sentences:
                        if len(temp_chunk) + len(sentence) > self.chunk_size and temp_chunk:
                            chunks.append(temp_chunk.strip())
                            temp_chunk = sentence
                        else:
                            if temp_chunk:
                                temp_chunk += " " + sentence
                            else:
                                temp_chunk = sentence

                    # Add any remaining text to current chunk
                    current_chunk = temp_chunk

            # Add the last chunk if it exists
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            # Remove any chunks that are too small (less than 10 characters)
            chunks = [chunk for chunk in chunks if len(chunk) > 10]

            return chunks
        except Exception as e:
            self.logger.error(f"Error during semantic chunking: {e}", exc_info=True)
            raise

    def validate_file_size(self, file_path: str) -> bool:
        """
        Validates the file size against the settings limit
        """
        try:
            import os
            file_size = os.path.getsize(file_path)
            if file_size > settings.max_file_size:
                self.logger.error(f"File size {file_size} exceeds limit {settings.max_file_size}")
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error validating file size: {e}", exc_info=True)
            raise

    def process_book(self, file_path: str, content_type: str, book_id: str,
                    chunk_strategy: str = "semantic") -> List[ChunkCreate]:
        """
        Process a book file: extract text, chunk, embed, and store
        """
        try:
            self.logger.info(f"Starting book processing for ID: {book_id}, file: {file_path}")

            book_id = UUID(book_id)

            # Validate file size before processing
            if not self.validate_file_size(file_path):
                raise ValueError(f"File size exceeds the limit of {settings.max_file_size} bytes")

            # Extract text based on content type
            if content_type.lower() == "pdf":
                text = self.extract_text_from_pdf(file_path)
            elif content_type.lower() == "html":
                text = self.extract_text_from_html(file_path)
            elif content_type.lower() == "text":
                text = self.extract_text_from_txt(file_path)
            else:
                raise ValueError(f"Unsupported content type: {content_type}")

            # Check if the extracted text is empty
            if not text.strip():
                self.logger.warning(f"No text extracted from {file_path}, content type {content_type}")
                raise ValueError(f"No text content found in file: {file_path}")

            # Chunk the text
            text_chunks = self.chunk_text(text, chunk_strategy)

            self.logger.info(f"Created {len(text_chunks)} text chunks for book: {book_id}")

            # Create chunk objects with IDs and metadata
            chunks = []
            for idx, chunk_text in enumerate(text_chunks):
                chunk = ChunkCreate(
                    book_id=book_id,
                    text=chunk_text,
                    chunk_index=idx,
                    metadata={
                        "created_at": datetime.now().isoformat(),
                        "source_file": file_path,
                        "chunk_strategy": chunk_strategy
                        },
                        hash=hashlib.sha256(chunk_text.encode()).hexdigest()
                        )
                chunks.append(chunk)

            self.logger.info(f"Book processing completed for ID: {book_id}, created {len(chunks)} chunks")
            return chunks
        except Exception as e:
            self.logger.error(f"Error processing book {book_id} from {file_path}: {e}", exc_info=True)
            raise

ingestion_service = IngestionService()