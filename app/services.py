import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.database import async_session
from app.models import Product
from app.schemas import ProductCreateSchema, ProductResponseSchema
from app.auth import get_current_user
from sqlalchemy.future import select

product_router = APIRouter()

async def fetch_and_save_product_data(artikul: str):
    try:
        print(f"Получение данных по артикулу: {artikul}")
        url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={artikul}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            print(f"API Response: {data}")

        # Extract product details
        products = data.get("data", {}).get("products", [])
        if not products:
            raise ValueError("Нет данных по переданному запросу")

        product_info = products[0]
        name = product_info.get("name", "Unknown Product")
        price = product_info.get("salePriceU", 0) / 100  # Convert to RUB
        rating = product_info.get("rating", 0)
        total_quantity = sum(
            stock.get("qty", 0)
            for size in product_info.get("sizes", [])
            for stock in size.get("stocks", [])
        )
        print(f"Parsed Product: {name}, Price: {price}, Rating: {rating}, Quantity: {total_quantity}")

        # Save or update product in the database
        async with async_session() as session:
            result = await session.execute(
                select(Product).where(Product.artikul == artikul)
            )
            existing = result.scalars().first()
            if not existing:
                product = Product(
                    artikul=artikul,
                    name=name,
                    price=price,
                    rating=rating,
                    total_quantity=total_quantity,
                )
                session.add(product)
            else:
                existing.name = name
                existing.price = price
                existing.rating = rating
                existing.total_quantity = total_quantity
            await session.commit()
            print(f"Product saved to DB: {artikul}")
    except Exception as e:
        print(f"Ошибка получения данных по артикулу {artikul}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@product_router.post("/products", response_model=ProductResponseSchema)
async def create_product(
    request: ProductCreateSchema,
    user: bool = Depends(get_current_user)
):
    artikul = request.artikul
    await fetch_and_save_product_data(artikul)
    async with async_session() as session:
        query = select(Product).where(Product.artikul == artikul)
        result = await session.execute(query)
        product = result.scalars().first()
        if not product:
            return JSONResponse(status_code=404, content={"message": "Товары не найдены."})
        return product

@product_router.get("/products/{artikul}", response_model=ProductResponseSchema)
async def get_and_save_product_info(artikul: str):
    """
    Fetch product data from Wildberries API, save it to the database, and return it.
    """
    await fetch_and_save_product_data(artikul)
    async with async_session() as session:
        query = select(Product).where(Product.artikul == artikul)
        result = await session.execute(query)
        product = result.scalars().first()
        if not product:
            raise HTTPException(status_code=404, detail="Товары не найдены в базе.")
        return product

@product_router.get("/subscribe/{artikul}")
async def subscribe_artikul(artikul: str, user: bool = Depends(get_current_user)):
    from app.scheduler import schedule_artikul  # Local import to avoid circular import
    schedule_artikul(artikul)
    return {"message": f"Обновление по артикулу запланировано: {artikul}"}
