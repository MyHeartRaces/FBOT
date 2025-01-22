from sqlalchemy import Column, String, Integer, Float
from app.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    artikul = Column(String, unique=True, index=True)
    name = Column(String)
    price = Column(Float)
    rating = Column(Float)
    total_quantity = Column(Integer)
