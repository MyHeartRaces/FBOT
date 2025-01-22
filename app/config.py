import os

DB_USER = os.getenv('DB_USER', 'myuser')
DB_PASS = os.getenv('DB_PASS', 'mypassword')
DB_NAME = os.getenv('DB_NAME', 'mydb')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

API_TOKEN = os.getenv('API_TOKEN', 'my_api_token')
BOT_TOKEN = os.getenv('BOT_TOKEN', '1234567:mybottoken')
