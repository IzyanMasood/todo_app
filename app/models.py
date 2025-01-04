from sqlalchemy import Column, Integer, String, Enum
from .database import Base
from .schemas import TaskStatus
class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    exp_date = Column(String(50), nullable=True)