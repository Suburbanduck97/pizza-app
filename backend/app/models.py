from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Size(Base):
    __tablename__ = "sizes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    price = Column(Float, nullable=False) # PREÇO FINAL AQUI
    max_flavors = Column(Integer, default=2)
    slices = Column(Integer) # Apenas informativo (6, 8, 12 fatias)
    active = Column(Boolean, default=True)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class Flavor(Base):
    __tablename__ = "flavors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String) # Ingredientes
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")

class Beverage(Base):
    __tablename__ = "beverages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    active = Column(Boolean, default=True)