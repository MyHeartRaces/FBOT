import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.database import async_session
from app.models import Product
from dotenv import load_dotenv
from sqlalchemy.future import select
import os

# Load environment variables from .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    kb = [
        [InlineKeyboardButton(text="Получить данные по товару", callback_data="get_product_data")]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("Информация о товарах с Wildberries", reply_markup=reply_markup)

@dp.callback_query()
async def handle_callback(query: types.CallbackQuery):
    if query.data == "get_product_data":
        await query.message.answer("Отправь Артикул Товара (SKU).")
        await query.answer()

@dp.message()
async def handle_artikul_input(message: types.Message):
    artikul = message.text
    async with async_session() as session:
        try:
            result = await session.execute(
                select(Product).where(Product.artikul == artikul)
            )
            product = result.scalars().first()
            if product:
                response_text = (
                    f"Артикул: {product.artikul}\n"
                    f"Название: {product.name}\n"
                    f"Цена: {product.price}\n"
                    f"Рейтинг: {product.rating}\n"
                    f"Количество: {product.total_quantity}"
                )
            else:
                response_text = "Нет информации по переданному артикулу."
        except Exception as e:
            response_text = f"Ошибка получения данных: {e}"
        await message.answer(response_text)

async def start_bot():
    await dp.start_polling(bot)
