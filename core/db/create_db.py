from core.middleware.db_middleware import Base, engine

print("Creating database ....")

Base.metadata.create_all(engine)

"""
common practice in SQLAlchemy applications to efficiently create database tables based on your model definitions. 
"""


