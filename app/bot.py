import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession
from .config import BOT_TOKEN
from .database import AsyncSessionLocal
from .models import Product

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

@dp.message(F.text == "Get product data")
async def on_get_product_data(message: Message):
    await message.answer("Please enter the product SKU")

@dp.message()
async def handle_sku(message: Message):
    sku = message.text
    async with AsyncSessionLocal() as session:
        result = await session.execute("SELECT name, sku, price, rating, total_quantity FROM products WHERE sku = :sku", {"sku": sku})
        row = result.fetchone()
        if not row:
            await message.answer("No data found for this SKU")
        else:
            name, sku, price, rating, total_qty = row
            await message.answer(f"Name: {name}\nSKU: {sku}\nPrice: {price}\nRating: {rating}\nTotal Quantity: {total_qty}")

async def on_startup():
    button = KeyboardButton("Get product data")
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(button)
    await bot.set_my_commands([])
    await bot.send_message(chat_id=12345, text="Bot started", reply_markup=kb)

async def run_bot():
    await dp.start_polling(bot)
