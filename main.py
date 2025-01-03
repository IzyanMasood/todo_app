from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, task_service
from app.database import SessionLocal, engine
from app.celery_job import check_exp_dates
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/tasks/", response_model=schemas.TaskResponse)
def create_task(task: schemas.Task, db: Session = Depends(get_db)):
    return task_service.create_task(db, task)

@app.get('/tasks',response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return task_service.get_tasks(db)

@app.get("/task/{task_id}",response_model=schemas.TaskResponse)
def get_task(task_id: int,db: Session = Depends(get_db)):
    return task_service.get_task(db,task_id)

@app.put("/task/{task_id}",response_model=schemas.TaskResponse)
def update_task(task_id: int,updated_task: schemas.Task,db: Session = Depends(get_db)):
    return task_service.update_task(db,task_id,updated_task)

@app.delete("/task/{task_id}",status_code=200)
def delete_task(task_id: int,db: Session = Depends(get_db)):
    return task_service.delete_task(db,task_id)

@app.patch("/task/{task_id}",response_model=schemas.TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.complete_task(db,task_id)



