import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

job_stores = {
    "default": SQLAlchemyJobStore(url=os.getenv("SCHEDULER_DB_URL", "sqlite:///jobs.sqlite"))
}
scheduler = AsyncIOScheduler(jobstores=job_stores)

def init_scheduler():
    scheduler.start()

def schedule_artikul(artikul: str):
    from app.services import fetch_and_save_product_data  # Local import to avoid circular import
    job_id = f"job_{artikul}"
    existing_job = scheduler.get_job(job_id)
    if not existing_job:
        scheduler.add_job(
            fetch_and_save_product_data,
            "interval",
            minutes=30,
            args=[artikul],
            id=job_id,
            replace_existing=True
        )
