from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from .database import AsyncSessionLocal
from .schemas import ProductCreate, ProductOut
from .product_service import fetch_and_save_product
from .scheduler import schedule_sku
from .config import API_TOKEN

router = APIRouter()

async def verify_token(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")
    token = parts[1]
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/api/v1/products", response_model=ProductOut)
async def create_product(data: ProductCreate, session: AsyncSession = Depends(get_session), auth: None = Depends(verify_token)):
    result = await fetch_and_save_product(session, data.artikul)
    return result

@router.get("/api/v1/subscribe/{artikul}")
async def subscribe_product(artikul: str, auth: None = Depends(verify_token)):
    await schedule_sku(artikul)
    return {"message": f"Scheduled data collection for SKU {artikul} every 30 minutes"}
