from sqlalchemy.orm import Session
from typing import List
from repositories.book_repository import BookRepository
from schemas import BookCreate, BookUpdate, BookOut

class BookService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def create_book(self, db: Session, book: BookCreate) -> BookOut:
        db_book = self.repo.create(db, book)
        return BookOut.from_orm(db_book)

    def update_book(self, db: Session, book_id: int, updates: BookUpdate) -> BookOut:
        book = self.repo.update(db, book_id, updates)
        return BookOut.from_orm(book)

    def get_books(self, db: Session, skip: int = 0, limit: int = 10) -> List[BookOut]:
        books = self.repo.get_all(db, skip, limit)
        return [BookOut.from_orm(b) for b in books]
