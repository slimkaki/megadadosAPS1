from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
import uuid
from ..models import Task
from ..database import get_db, DBSession

router = APIRouter()

@router.get(
    '',
    summary='Reads task list',
    description='Reads the whole task list.',
    response_model=Dict[uuid.UUID, Task],
)
async def read_tasks(completed: bool = None, db: DBSession = Depends(get_db)):
    return db.read_tasks(completed)


@router.post(
    '',
    summary='Creates a new task',
    description='Creates a new task and returns its UUID.',
    response_model=uuid.UUID,
)
async def create_task(item: Task, db: DBSession = Depends(get_db)):
    return db.create_task(item)


@router.get(
    '/{uuid_}',
    summary='Reads task',
    description='Reads task from UUID.',
    response_model=Task,
)
async def read_task(uuid_: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        return db.read_task(uuid_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception

@router.put(
    '/{uuid_}',
    summary='Replaces a task',
    description='Replaces a task identified by its UUID.',
)
async def replace_task(uuid_: uuid.UUID, item: Task, db: DBSession = Depends(get_db)):
    try:
        db.replace_task(uuid_, item)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception

@router.patch(
    '/{uuid_}',
    summary='Alters task',
    description='Alters a task identified by its UUID',
)
async def alter_task(uuid_: uuid.UUID, item: Task, db: DBSession = Depends(get_db)):
    try:
        db.alter_task(uuid_, item)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception

@router.delete(
    '/{uuid_}',
    summary='Deletes task',
    description='Deletes a task identified by its UUID',
)
async def remove_task(uuid_: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        db.remove_task(uuid_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception