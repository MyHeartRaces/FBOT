import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Product
from .schemas import ProductOut

async def fetch_and_save_product(session: AsyncSession, sku: str) -> ProductOut:
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={sku}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()
    product_info = data['data']['products'][0]
    name = product_info['name']
    price = product_info['salePriceU'] / 100
    rating = float(product_info['rating'])
    total_quantity = 0
    for size in product_info.get('sizes', []):
        for stock in size.get('stocks', []):
            total_quantity += stock.get('qty', 0)
    stmt = select(Product).where(Product.sku == sku)
    result = await session.execute(stmt)
    existing = result.scalars().first()
    if existing:
        existing.name = name
        existing.price = price
        existing.rating = rating
        existing.total_quantity = total_quantity
    else:
        existing = Product(name=name, sku=sku, price=price, rating=rating, total_quantity=total_quantity)
        session.add(existing)
    await session.commit()
    await session.refresh(existing)
    return ProductOut(
        name=existing.name,
        sku=existing.sku,
        price=existing.price,
        rating=existing.rating,
        total_quantity=existing.total_quantity
    )
