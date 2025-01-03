from sqlalchemy.orm import Session
from . import models, schemas

def create_task(db: Session, task: schemas.Task):
    db_task = models.Task(
        name=task.name,
        description=task.description,
        exp_date=task.exp_date,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session):
    return db.query(models.Task).all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id==task_id).first()

def delete_task(db: Session, task_id: int):
    db.query(models.Task).filter(models.Task.id==task_id).delete()
    db.commit()
    return

def update_task(db: Session, task_id:int,task: schemas.Task):
    result_set = db.query(models.Task).filter(models.Task.id==task_id).first()
    
    if task.name:
        result_set.name=task.name
    if task.description:
        result_set.description=task.description
    if task.status:
        result_set.status=task.status
    if task.exp_date:
        result_set.exp_date=task.exp_date

    db.commit()
    db.refresh(result_set)
    return result_set

def complete_task(db: Session, task_id: int):
    result_set = db.query(models.Task).filter(models.Task.id==task_id).first()
    result_set.status=schemas.TaskStatus.COMPLETED
    db.commit()
    db.refresh(result_set)
    return result_set
    