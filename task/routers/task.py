from fastapi import APIRouter,Depends,status,HTTPException
from .. import schemas,database,models, oauth2
from typing import List
from sqlalchemy.orm import Session
from .. repository import task



get_db = database.get_db

router = APIRouter(
                    prefix="/task",
                    tags=['Tasks']
                    
                    )

@router.get('/',response_model= List[schemas.ShowTask])
def get_tasks(db: Session = Depends(database.get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.get_all(db)

@router.post('/',status_code = status.HTTP_201_CREATED)
def create_task(request :schemas.Task, db: Session = Depends(database.get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.create(request,db)

@router.get('/{id}',status_code = status.HTTP_202_ACCEPTED,response_model= schemas.ShowTask)
def get_task_by_id(task_id,db:Session= Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.show(id,db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
   return task.destroy(id,db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_task(id: int, request: schemas.Task, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.update(id,request,db)

