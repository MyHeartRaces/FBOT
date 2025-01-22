from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Float, Integer

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    sku: Mapped[str] = mapped_column(String, unique=True, index=True)
    price: Mapped[float] = mapped_column(Float)
    rating: Mapped[float] = mapped_column(Float)
    total_quantity: Mapped[int] = mapped_column(Integer)
