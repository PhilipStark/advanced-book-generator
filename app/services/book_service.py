from ..models import Book, BookStatus
from .book_generator import BookGenerator
from .event_service import event_service
from sqlalchemy.orm import Session
from typing import Dict, Any

class BookService:
    def __init__(self, db: Session):
        self.db = db
        self.generator = BookGenerator()

    async def create_book(self, book_data: Dict[str, Any]) -> Book:
        book = Book(**book_data)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    async def generate_book(self, book_id: int) -> Book:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise ValueError("Book not found")

        book.status = BookStatus.GENERATING
        self.db.commit()
        await event_service.publish(book_id, {
            "status": BookStatus.GENERATING,
            "progress": "Starting generation..."
        })

        try:
            # Generate structure
            await event_service.publish(book_id, {
                "status": BookStatus.GENERATING,
                "progress": "Generating book structure..."
            })
            structure = await self.generator.generate_structure({
                "title": book.title,
                "description": book.description,
                "genre": book.genre,
                "target_audience": book.target_audience,
                "style": book.style,
                "tone": book.tone,
                "length": book.length
            })

            # Generate content
            await event_service.publish(book_id, {
                "status": BookStatus.GENERATING,
                "progress": "Creating book content..."
            })
            content = await self.generator.generate_content(structure)
            
            book.content = {"structure": structure, "content": content}
            book.status = BookStatus.COMPLETED
            await event_service.publish(book_id, {
                "status": BookStatus.COMPLETED,
                "progress": "Book generation completed!"
            })
        except Exception as e:
            book.status = BookStatus.FAILED
            await event_service.publish(book_id, {
                "status": BookStatus.FAILED,
                "progress": "Generation failed. Please try again."
            })
            raise e
        finally:
            self.db.commit()

        return book