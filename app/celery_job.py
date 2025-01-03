import os
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv


load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

celery = Celery("expiration_checker", broker=REDIS_URL)
celery.autodiscover_tasks(['celery_job'])
@celery.task(name="check_exp_dates")
def check_exp_dates():
    print("HELLO")
    # db = SessionLocal()
    # try:
    #     yield db
    # finally:
    #     db.close()
    # all_tasks = db.query(models.Task).filter(models.Task.status == models.TaskStatus.PENDING).all()
    # for task in all_tasks:
    #     if datetime.strptime(task.exp_date,"%Y-%m-%d %H:%M:%S") < datetime.utcnow():
    #         task.status = models.TaskStatus.EXPIRED
    #         db.add(task)
    # db.commit()
    # db.close()

# Configure periodic tasks
celery.conf.beat_schedule = {
    "check-exp-dates-every-minute": {
        "task": "celery_job.check_exp_dates",
        "schedule": crontab(minute="*"),
    },
}
    