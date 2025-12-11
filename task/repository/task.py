from sqlalchemy.orm import Session
from .. import models,schemas
from fastapi import HTTPException,status

def get_all(db:Session):
    tasks = db.query(models.Task).all()
    return tasks

def create(request: schemas.Task, db:Session):
    new_task = models.Task(title=request.title,body=request.body,user_id =1)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def destroy(id:int,db:Session):
    task = db.query(models.Task).filter(models.Task.id == id)

    if not task.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id} does not exist"
        )

    task.delete(synchronize_session=False)
    db.commit()

    return "done"

def update(id:int,request:schemas.Task, db:Session):
    task = db.query(models.Task).filter(models.Task.id == id)

    if not task.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id} not found"
        )

    task.update({
        "title": request.title,
        "body": request.body
    })

    db.commit()

    return {"message": "Task updated successfully"}

def show(id:int,db:Session):
    task = db.query(models.Task).filter(models.Task.id==id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Task with id {id} does not exist")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"details":f"Task with id {id} does not exist"}
    return task

