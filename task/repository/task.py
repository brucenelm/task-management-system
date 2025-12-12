from sqlalchemy.orm import Session
from .. import models,schemas
from fastapi import HTTPException,status
import io
import csv

def get_all(db:Session,current_user: models.User):
    # tasks = db.query(models.Task).all()
    tasks = db.query(models.Task).filter(models.Task.user_id == current_user.id).all()

    return tasks

def create(request: schemas.Task, db:Session,current_user: models.User):
    
    new_task = models.Task(title=request.title,body=request.body,priority=request.priority,category =request.category,status=request.status,user_id= current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def destroy(id:int,db:Session,current_user: models.User):
    #task = db.query(models.Task).filter(models.Task.id == id)
    task = db.query(models.Task).filter(models.Task.id == id, models.Task.user_id == current_user.id)  # <-- only allow their own tasks


    if not task.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id} does not exist"
        )

    task.delete(synchronize_session=False)
    db.commit()

    return "done"

def update(id:int,request:schemas.Task, db:Session,current_user: models.User):
    #task = db.query(models.Task).filter(models.Task.id == id)
    task = db.query(models.Task).filter(models.Task.id == id, models.Task.user_id == current_user.id)  # <-- only allow their own tasks

    if not task.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id} not found"
        )

    task.update({
        "title": request.title,
        "body": request.body,
        "priority": request.priority,
        "category": request.category,
        "status": request.status
    })

    db.commit()

    return {"message": "Task updated successfully"}

def show(task_id:int,db:Session,current_user: models.User):
    # task = db.query(models.Task).filter(models.Task.id==task_id).first()
    task= (db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first())

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Task with id {task_id} does not exist")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"details":f"Task with id {id} does not exist"}
    return task

def create_csv(db: Session, current_user):
    tasks = db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "title", "body", "user_id","priority","category","status"])
    
    for task in tasks:
        writer.writerow([task.id, task.title, task.body, task.user_id,task.priority,task.category,task.status])
    
    output.seek(0)
    return output

