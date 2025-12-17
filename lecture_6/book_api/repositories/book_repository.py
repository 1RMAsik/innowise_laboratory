from sqlalchemy.orm import Session
from typing import Optional, List
from models import Book
from schemas import BookCreate, BookUpdate
from fastapi import HTTPException

class BookRepository:
    def get_by_id(self, db: Session, book_id: int) -> Optional[Book]:
        return db.query(Book).filter(Book.id == book_id).first()

    def get_all(self, db: Session, skip: int, limit: int) -> List[Book]:
        return db.query(Book).offset(skip).limit(limit).all()

    def create(self, db: Session, book: BookCreate) -> Book:
        db_book = Book(**book.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    def update(self, db: Session, book_id: int, updates: BookUpdate) -> Book:
        book = self.get_by_id(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        update_data = updates.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        for field, value in update_data.items():
            setattr(book, field, value)

        try:
            db.commit()
            db.refresh(book)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        return book
