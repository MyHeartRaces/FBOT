from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.scheduler import init_scheduler
from app.telegram_bot import start_bot
from app.services import product_router
import asyncio
import uvicorn

app = FastAPI(title="FBOT Wildberries Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    init_scheduler()
    asyncio.create_task(start_bot())

@app.get("/api/v1/healthcheck")
async def healthcheck():
    return {"status": "ok"}

app.include_router(product_router, prefix="/api/v1", tags=["products"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
