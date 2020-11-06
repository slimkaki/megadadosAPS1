# pylint: disable=missing-module-docstring, missing-function-docstring, invalid-name
import uuid

from typing import Dict

from fastapi import APIRouter, HTTPException, Depends

from ..database import DBSession, get_db
from ..models import Task

router = APIRouter()


# FOR TASKS
@router.get(
    '/tasks',
    summary='Reads task list',
    description='Reads the whole task list.',
    response_model=Dict[str, Task],
)
async def read_tasks(username: str, completed: bool = None, db: DBSession = Depends(get_db)):
    return db.read_tasks(username, completed)


@router.post(
    '/tasks',
    summary='Creates a new task',
    description='Creates a new task to the username passed and returns its UUID.',
    response_model=uuid.UUID,
)
async def create_task(username: str, item: Task, db: DBSession = Depends(get_db)):
    return db.create_task(username, item)


@router.get(
    '/tasks/{uuid_}',
    summary='Reads task',
    description='Reads single task from UUID and username.',
    response_model=Task,
)
async def read_task(username: str, uuid_: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        return db.read_task(uuid_, username)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception


@router.put(
    '/tasks/{uuid_}',
    summary='Replaces a task',
    description='Replaces a task identified by its UUID.',
)
async def replace_task(
        username: str,
        uuid_: uuid.UUID,
        item: Task,
        db: DBSession = Depends(get_db),
):
    try:
        db.replace_task(username, uuid_, item)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception


@router.patch(
    '/tasks/{uuid_}',
    summary='Alters task',
    description='Alters a task identified by its UUID',
)
async def alter_task(
        username: str,
        uuid_: uuid.UUID,
        item: Task,
        db: DBSession = Depends(get_db),
):
    try:
        old_item = db.read_task(uuid_, username)
        update_data = item.dict(exclude_unset=True)
        new_item = old_item.copy(update=update_data)
        db.replace_task(username, uuid_, new_item)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception


@router.delete(
    '/tasks/{uuid_}',
    summary='Deletes task',
    description='Deletes a task identified by its UUID',
)
async def remove_task(uuid_: uuid.UUID, username: str, db: DBSession = Depends(get_db)):
    try:
        db.remove_task(uuid_, username)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception


@router.delete(
    '/tasks',
    summary='Deletes all tasks, use with caution',
    description='Deletes all tasks, use with caution',
)
async def remove_all_tasks(username: str, db: DBSession = Depends(get_db)):
    db.remove_all_tasks(username)


# FOR USERS
@router.post(
    '/users',
    summary='Creates a new user',
    description='Creates a new user and returns its UUID.',
    response_model=uuid.UUID,
)
async def create_user(username, db: DBSession = Depends(get_db)):
    return db.create_user(username)

@router.delete(
    '/users/{username}',
    summary='Deletes specific user',
    description='Deletes a user identified by its username',
)
async def remove_user(username: str, db: DBSession = Depends(get_db)):
    try:
        uuid = db.get_id_by_username(username)
        db.delete_user(uuid)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        ) from exception

@router.get(
    '/users',
    summary='Reads users list',
    description='Reads the whole users list.',
    response_model=Dict[uuid.UUID, str],
)
async def read_users(db: DBSession = Depends(get_db)):
    return db.read_users()

@router.get(
    '/users/{username}',
    summary='Get user',
    description='Get username by UUID.',
)
async def read_user(username: str, db: DBSession = Depends(get_db)):
    try:
        return db.get_id_by_username(username)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        ) from exception

@router.patch(
    '/users/{uuid_}',
    summary='Alters user',
    description='Alters a user identified by its UUID',
)
async def alter_user(old_username: str, new_username, db: DBSession = Depends(get_db),):
    try:
        id_user = db.get_id_by_username(old_username)
        db.update_user(id_user, new_username)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception
