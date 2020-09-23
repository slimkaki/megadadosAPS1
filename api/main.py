# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import uuid
from typing import Dict
from .database import DBSession, get_db
from .models import Task
from fastapi import FastAPI, HTTPException, Depends

tags_metadata = [
    {
        'name': 'task',
        'description': 'Operations related to tasks.',
    },
]

app = FastAPI(
    title='Task list',
    description='Task-list project for the **Megadados** course',
    openapi_tags=tags_metadata,
)
