from app.services import fetch_and_save_product_data
from app.scheduler import scheduler

def schedule_artikul(artikul: str):
    job_id = f"job_{artikul}"
    existing_job = scheduler.get_job(job_id)
    if not existing_job:
        scheduler.add_job(
            fetch_and_save_product_data,
            "interval",
            minutes=30,
            args=[artikul],
            id=job_id,
            replace_existing=True,
        )
