from pydantic import BaseModel

class ProductCreate(BaseModel):
    artikul: str

class ProductOut(BaseModel):
    name: str
    sku: str
    price: float
    rating: float
    total_quantity: int
