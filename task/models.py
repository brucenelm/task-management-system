from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey,Enum as SqlEnum
from sqlalchemy.orm import relationship
from .enumfile import CategoryEnum, PriorityEnum, StatusEnum



class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    body = Column(String,nullable=False)
    category = Column(SqlEnum(CategoryEnum), nullable=False, default=CategoryEnum.other)
    priority = Column(SqlEnum(PriorityEnum), nullable=False, default=PriorityEnum.medium)
    status = Column(SqlEnum(StatusEnum), nullable=False, default=StatusEnum.todo)

    user_id = Column(Integer,ForeignKey('users.id'))
    creator = relationship("User",back_populates="tasks")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String) 
    password= Column(String)
    tasks = relationship("Task",back_populates="creator")

