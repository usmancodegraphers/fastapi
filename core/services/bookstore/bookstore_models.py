from sqlalchemy import String, Integer, Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from core.middleware.db_middleware import Base

# Association table
book_authors = Table(
    'book_authors',
    Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('author_id', ForeignKey('authors.id'), primary_key=True),
    extend_existing = True
)


# Models
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    authors = relationship("Author", secondary="book_authors", back_populates="books")
    __table_args__ = {'extend_existing': True}


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("Book", secondary="book_authors", back_populates='authors')
    __table_args__ = {'extend_existing': True}
