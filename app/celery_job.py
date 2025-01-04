from datetime import datetime
import os
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
from app.database import SessionLocal
from app.models import Task,TaskStatus
load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

celery = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)

@celery.task(name="check_exp_dates")
def check_exp_dates():
    db = SessionLocal()
    try:
        all_tasks = db.query(Task).filter(Task.status == TaskStatus.PENDING).all()
        for task in all_tasks:
            taskExpDate = datetime.strptime(task.exp_date, "%Y-%m-%d %H:%M:%S")
            if taskExpDate < datetime.now():
                task.status = TaskStatus.EXPIRED
                db.commit()
                db.refresh(task)
    finally:
        db.close()

    

# Configure periodic tasks
celery.conf.beat_schedule = {
    "check-exp-dates-every-minute": {
        "task": "check_exp_dates",
        "schedule": crontab(minute="*"),
    },
}

celery.conf.timezone = 'UTC'