from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# from sql alchemy docs --- format: postgresql://<user>:<password>@<host>:<port>/<database>

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:usman@localhost/company_db'

engine = create_engine(SQLALCHEMY_DATABASE_URI, future=True, echo=True)
"""The echo=True parameter enables logging of SQL statements, which can be helpful for debugging and understanding 
database interactions."""

Base = declarative_base()  # This class serves as a foundation for your SQLAlchemy models, providing features like automatic table creation, relationship management, and inheritance.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# ensuring that sessions created from it will use the established database connection.


