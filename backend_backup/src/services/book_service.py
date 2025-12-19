from src.models.book import Book, BookCreate, BookUpdateStatus, BookStatus
from src.services.storage import storage_service
from src.services.database import get_conn, release_conn
from uuid import UUID, uuid4
from datetime import datetime

class BookService:
    def __init__(self):
        pass

    def create_book(self, book_create: BookCreate) -> Book:
        """
        Create a new book record in the database
        """
        book_id = uuid4()
        conn = get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO books (id, title, author, content_type, upload_date, 
                                       chunk_strategy, total_chunks, status, description, language)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    str(book_id), book_create.title, book_create.author,
                    book_create.content_type.value, datetime.now(),
                    book_create.chunk_strategy.value, 0,
                    BookStatus.PROCESSING.value, book_create.description,
                    book_create.language
                ))
                conn.commit()
        finally:
            release_conn(conn)

        # Return book object
        return Book(
            id=book_id,
            title=book_create.title,
            author=book_create.author,
            content_type=book_create.content_type,
            upload_date=datetime.now(),
            chunk_strategy=book_create.chunk_strategy.value,
            total_chunks=0,
            status=BookStatus.PROCESSING,
            description=book_create.description,
            language=book_create.language
        )

    def update_book_status(self, book_id: UUID, status_update: BookUpdateStatus) -> Book:
        """
        Update the status of a book
        """
        conn = get_conn()
        try:
            with conn.cursor() as cursor:
                update_fields = []
                params = []

                if status_update.status:
                    update_fields.append("status = %s")
                    params.append(status_update.status.value)

                if status_update.total_chunks is not None:
                    update_fields.append("total_chunks = %s")
                    params.append(status_update.total_chunks)

                params.append(str(book_id))
                query = f"UPDATE books SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
                cursor.execute(query, params)
                result = cursor.fetchone()
                if not result:
                    raise ValueError(f"Book with id {book_id} not found")
                conn.commit()
        finally:
            release_conn(conn)

        return Book(
            id=UUID(result[0]),
            title=result[1],
            author=result[2],
            content_type=next(ct for ct in BookService.get_content_types() if ct.value == result[3]),
            upload_date=result[4],
            chunk_strategy=result[5],
            total_chunks=result[6],
            status=next(st for st in BookService.get_status_types() if st.value == result[7]),
            file_path=result[8],
            description=result[9],
            language=result[10]
        )

    @staticmethod
    def get_content_types():
        from src.models.book import ContentType
        return list(ContentType)

    @staticmethod
    def get_status_types():
        return list(BookStatus)

    def get_book(self, book_id: UUID) -> Book:
        """
        Retrieve a book by its ID
        """
        conn = get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id, title, author, content_type, upload_date, 
                           chunk_strategy, total_chunks, status, file_path, 
                           description, language
                    FROM books WHERE id = %s
                """, (str(book_id),))
                result = cursor.fetchone()
                if not result:
                    raise ValueError(f"Book with id {book_id} not found")
        finally:
            release_conn(conn)

        return Book(
            id=UUID(result[0]),
            title=result[1],
            author=result[2],
            content_type=next(ct for ct in self.get_content_types() if ct.value == result[3]),
            upload_date=result[4],
            chunk_strategy=result[5],
            total_chunks=result[6],
            status=next(st for st in self.get_status_types() if st.value == result[7]),
            file_path=result[8],
            description=result[9],
            language=result[10]
        )


book_service = BookService()
