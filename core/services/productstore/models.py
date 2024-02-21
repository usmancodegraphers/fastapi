from sqlalchemy import String, Boolean, Integer, Column, Text, ForeignKey
from sqlalchemy.orm import relationship

from core.middleware.db_middleware import Base


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    email = Column(String, unique=True, index=True)

    items = relationship("models.Item", back_populates="company")
    __table_args__ = {'extend_existing': True}


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    on_offer = Column(Boolean, default=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("models.Company", back_populates="items")

    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return f"<Item name={self.name} price={self.price}>"
