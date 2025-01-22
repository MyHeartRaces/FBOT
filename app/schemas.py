from pydantic import BaseModel, Field

class ProductCreateSchema(BaseModel):
    artikul: str = Field(..., example="211695539")

class ProductResponseSchema(BaseModel):
    artikul: str
    name: str
    price: float
    rating: float
    total_quantity: int

    class Config:
        from_attributes = True
