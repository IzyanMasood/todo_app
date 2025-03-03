from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    EXPIRED = "EXPIRED"


class Task(BaseModel):
    name: str
    description: str = None
    exp_date: str
    status: TaskStatus
    

class TaskResponse(Task):
    id: int
    