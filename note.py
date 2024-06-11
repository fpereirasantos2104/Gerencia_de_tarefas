from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db

router = APIRouter()

@router.get('/')
def get_tasks(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    tasks = db.query(models.Task).filter(
        models.Task.title.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(tasks), 'tasks': tasks}

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_task(payload: schemas.TaskBaseSchema, db: Session = Depends(get_db)):
    new_task = models.Task(**payload.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"status": "success", "task": new_task}

@router.patch('/{taskId}')
def update_task(taskId: int, payload: schemas.TaskBaseSchema, db: Session = Depends(get_db)):
    task_query = db.query(models.Task).filter(models.Task.id == taskId)
    db_task = task_query.first()

    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {taskId} found')
    update_data = payload.dict(exclude_unset=True)
    task_query.filter(models.Task.id == taskId).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_task)
    return {"status": "success", "note": db_task}

@router.get('/{taskId}')
def get_post(taskId: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == taskId).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No task with this id: {id} found")
    return {"status": "success", "task": task}


@router.delete('/{taskId}')
def delete_post(taskId: int, db: Session = Depends(get_db)):
    task_query = db.query(models.Task).filter(models.Task.id == taskId)
    task = task_query.first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No task with this id: {id} found')
    task_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)