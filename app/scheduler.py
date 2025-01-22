from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from .database import AsyncSessionLocal
from .product_service import fetch_and_save_product
from .models import Product

scheduler = AsyncIOScheduler()
subscriptions = []

async def schedule_sku(sku: str):
    if sku not in subscriptions:
        subscriptions.append(sku)
        scheduler.add_job(fetch_data_job, 'interval', minutes=30, args=[sku], id=sku, replace_existing=True)

async def fetch_data_job(sku: str):
    async with AsyncSessionLocal() as session:
        await fetch_and_save_product(session, sku)

async def load_existing_subscriptions():
    async with AsyncSessionLocal() as session:
        result = await session.execute("SELECT sku FROM products")
        skus = [row[0] for row in result]
        for sku in skus:
            if sku not in subscriptions:
                await schedule_sku(sku)

def start_scheduler():
    scheduler.start()
