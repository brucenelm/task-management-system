from pydantic import BaseModel
from typing import List, Optional
from .enumfile import CategoryEnum, PriorityEnum, StatusEnum


class TaskBase(BaseModel):
    title: str
    body: str
    category: CategoryEnum = CategoryEnum.other      # default value
    priority: PriorityEnum = PriorityEnum.medium     # default value
    status: StatusEnum = StatusEnum.todo            # default value

class Task(TaskBase):
    class Config():
            from_attributes = True

class User(BaseModel):
    name:str
    email:str
    password:str

class showUser(BaseModel):
    name:str
    email:str
    #tasks : List[Task] = []
    class Config():
        from_attributes = True

class ShowTask(Task):
    creator: showUser
    class Config():
        # orm_mode = True
        from_attributes = True

class Login(BaseModel):
     username: str
     password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

class TaskCreate(BaseModel):
    category: CategoryEnum
    priority: PriorityEnum
    status: StatusEnum
    tags: list[str] | None = None



    
