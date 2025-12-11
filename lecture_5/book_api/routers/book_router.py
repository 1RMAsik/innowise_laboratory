from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional, List
import traceback

from ..database import get_db
from ..schemas import BookCreate, BookOut, BookUpdate
from ..services.book_service import BookService
from ..repositories.book_repository import BookRepository

router = APIRouter(prefix="/books", tags=["books"])

service = BookService(BookRepository())



@router.post("/", response_model=BookOut)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    return service.create_book(db, book)


@router.get("/", response_model=List[BookOut])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return service.get_books(db, skip, limit)


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    result = service.delete_book(db, book_id)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}


@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, updates: BookUpdate, db: Session = Depends(get_db)):
    return service.update_book(db, book_id, updates)


@router.get("/search/", response_model=List[BookOut])
def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return service.search_books(db, title, author, year)