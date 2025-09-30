from typing import List

from sqlalchemy.orm import Session

from . import models, schemas


def get_tasks(db: Session) -> List[models.Task]:
    return db.query(models.Task).all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    db_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        due_date=task.due_date,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(
    db: Session, task_db: models.Task, task_update: schemas.TaskUpdate
) -> models.Task:
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task_db, field, value)
    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return task_db


def delete_task(db: Session, task_db: models.Task) -> None:
    db.delete(task_db)
    db.commit()
