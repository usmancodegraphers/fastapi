from typing import List

from fastapi import APIRouter, HTTPException, status

from core.constants import ALREADY_EXISTS, NOT_FOUND
from core.middleware.db_middleware import SessionLocal
from .bookstore_models import Author, Book
from .bookstore_schemas import AuthorSchema, BookSchema

router = APIRouter()

db = SessionLocal()


@router.post("/books", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
def create_book(book: BookSchema) -> BookSchema:
    """
    Creates a new book in the database, associating it with existing authors.

    Args:
        book (BookSchema): A JSON object representing the new book data.

    Returns:
        BookSchema: The newly created book data as a `BookSchema` object.

    Raises:
        HTTPException:
            - 400 Bad Request:
                - If a book with the same title already exists.
                - If the book title is missing.
            - 404 Not Found: If any of the provided author IDs don't correspond to existing authors in the database.
    """
    existing_book = db.query(Book).filter(Book.title == book.title).first()
    if existing_book:
        raise HTTPException(status_code=400, detail=ALREADY_EXISTS)

    new_book = Book(
        id=book.id,
        title=book.title,
    )

    db.add(new_book)

    for author in book.authors:
        print(author)
        existing_author = db.query(Author).filter(Author.id == author.id).first()
        if existing_author:
            new_book.authors.append(existing_author)

    db.commit()
    return book


# Get all books
@router.get("/books", response_model=List[BookSchema])
def get_all_books():
    """
    Retrieves all books from the database.

    Returns:
        List[BookSchema]: A list of book data represented by `BookSchema` objects.
    """
    return db.query(Book).all()


@router.delete("/books/{book_id}")
def delete_book(book_id: int):
    """
    Deletes a book from the database by its ID.

    Args:
        book_id (int): The unique identifier of the book to delete.

    Raises:
        HTTPException:
            - 404 Not Found: If no book is found with the provided ID.
    """

    book_to_delete = db.query(Book).filter(Book.id == book_id).first()
    if not book_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)

    db.delete(book_to_delete)
    db.commit()


# Create an author
@router.post("/authors", response_model=AuthorSchema, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorSchema) -> AuthorSchema:
    """
        Creates a new author in the database.

        Args:
            author (AuthorSchema): A JSON object representing the new author data.

        Returns:
            AuthorSchema: The newly created author data as an `AuthorSchema` object.

        Raises:
            HTTPException:
                - 400 Bad Request: If an author with the same name already exists.
        """
    existing_author = db.query(Author).filter(Author.name == author.name).first()

    if existing_author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ALREADY_EXISTS)

    new_author = Author(
        id=author.id,
        name=author.name
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


# Get all authors
@router.get("/authors", response_model=List[AuthorSchema])
def get_all_authors():
    """
    Retrieves all author from the database.

    Returns:
        List[BookSchema]: A list of book data represented by `AuthorSchema` objects.
    """
    return db.query(Author).all()


@router.delete("/authors/{author_id}")
def delete_author(author_id: int):
    """
    Deletes an author from the database by its ID.

    Args:
        author_id (int): The unique identifier of the author to delete.

    Raises:
        HTTPException:
            - 404 Not Found: If no author is found with the provided ID.
    """

    author_to_delete = db.query(Author).filter(Author.id == author_id).first()
    if not author_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)

    db.delete(author_to_delete)
    db.commit()
