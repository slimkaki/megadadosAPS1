# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import json
import uuid

from functools import lru_cache

import mysql.connector as conn

from fastapi import Depends

from utils.utils import get_config_test_filename, get_admin_secrets_filename

from .models import Task

class DBSession:
    def __init__(self, connection: conn.MySQLConnection):
        self.connection = connection

    def read_tasks(self, username, completed: bool = None):
        owner_id = self.get_id_by_username(username)
        query = 'SELECT BIN_TO_UUID(id_task), description, completed FROM tasks'
        if completed is not None:
            query += ' WHERE id_user=UUID_TO_BIN(%s) AND completed = '
            if completed:
                query += 'True'
            else:
                query += 'False'
        else:
            query += ' WHERE id_user=UUID_TO_BIN(%s)'
        

        with self.connection.cursor() as cursor:
            cursor.execute(query, (str(owner_id),))
            db_results = cursor.fetchall()

        return {
            uuid_: Task(
                description=field_description,
                completed=bool(field_completed)
            )
            for uuid_, field_description, field_completed in db_results
        }

    def create_task(self, username, item: Task):
        uuid_ = uuid.uuid4()
        if not self.__user_exists_by_username(username):
            raise KeyError()
        user_id = self.get_id_by_username(username)
        with self.connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO tasks VALUES (UUID_TO_BIN(%s), %s, %s, UUID_TO_BIN(%s))',
                (str(uuid_), item.description, item.completed, user_id),
            )
        self.connection.commit()

        return uuid_

    def read_task(self, uuid_: uuid.UUID, username: str):
        if not self.__task_exists(uuid_):
            raise KeyError()
        if not self.__user_exists_by_username(username):
            raise KeyError()
        id_user = self.get_id_by_username(username)

        with self.connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT description, completed
                FROM tasks
                WHERE id_task = UUID_TO_BIN(%s) AND id_user = UUID_TO_BIN(%s)
                ''',
                (str(uuid_), str(id_user)),
            )
            result = cursor.fetchone()

        return Task(description=result[0], completed=bool(result[1]))

    def replace_task(self, username, uuid_, item):
        if not self.__task_exists(uuid_):
            raise KeyError()
        id_user = self.get_id_by_username(username)
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''
                UPDATE tasks SET description=%s, completed=%s
                WHERE id_task=UUID_TO_BIN(%s) AND id_user=UUID_TO_BIN(%s)
                ''',
                (item.description, item.completed, str(uuid_), str(id_user)),
            )
        self.connection.commit()

    def remove_task(self, uuid_, username):
        id_user = self.get_id_by_username(username)
        if not self.__task_exists(uuid_):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                'DELETE FROM tasks WHERE id_task=UUID_TO_BIN(%s) AND id_user=UUID_TO_BIN(%s)',
                (str(uuid_), str(id_user)),
            )
        self.connection.commit()

    def remove_all_tasks(self, username):
        id_user = self.get_id_by_username(username)
        with self.connection.cursor() as cursor:
            cursor.execute('DELETE FROM tasks WHERE id_user = UUID_TO_BIN(%s)', (str(id_user), ), )
        self.connection.commit()

    def __task_exists(self, uuid_: uuid.UUID):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT EXISTS(
                    SELECT 1 FROM tasks WHERE id_task=UUID_TO_BIN(%s)
                )
                ''',
                (str(uuid_), ),
            )
            results = cursor.fetchone()
            found = bool(results[0])

        return found

    def create_user(self, username):
        uuid_ = uuid.uuid4()
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''
                INSERT INTO users VALUES (UUID_TO_BIN(%s), %s)
                ''',
                (str(uuid_), username),
            )
        self.connection.commit()

        return uuid_

    def __user_exists_by_username(self, username: str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT EXISTS(
                    SELECT 1 FROM users WHERE username=%s
                )
                ''',
                (username, ),
            )
            results = cursor.fetchone()
            found = bool(results[0])

        return found
    
    def __user_exists(self, uuid_: uuid.UUID):
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT EXISTS(
                    SELECT 1 FROM users WHERE id_user=UUID_TO_BIN(%s)
                )
                ''',
                (str(uuid_), ),
            )
            results = cursor.fetchone()
            found = bool(results[0])

        return found

    def delete_user(self, uuid_):
        if not self.__user_exists(uuid_):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                'DELETE FROM users WHERE id_user=UUID_TO_BIN(%s)',
                (str(uuid_),)
            )
        self.connection.commit()

    def update_user(self, uuid_, new_username):
        if not self.__user_exists(uuid_):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                '''
                UPDATE users SET username=%s
                WHERE id_user=UUID_TO_BIN(%s)
                ''',
                (new_username, str(uuid_)),
            )
        self.connection.commit()
    
    def get_id_by_username(self, username):
        if not self.__user_exists_by_username(username):
            raise KeyError()
        with self.connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT BIN_TO_UUID(id_user)
                FROM users
                WHERE username=%s
                ''',
                (username,)
            )
            user_id = cursor.fetchone()
            return user_id[0]

    def read_users(self):
        query = 'SELECT BIN_TO_UUID(id_user), username FROM users'

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            db_results = cursor.fetchall()

        return {
            id_user: username
            for id_user, username in db_results
            }


@lru_cache
def get_credentials(
        config_file_name: str = Depends(get_config_test_filename),     # mudar para get_config_filename
        secrets_file_name: str = Depends(get_admin_secrets_filename),  # mudar para get_app_secrets_filename
):
    with open(config_file_name, 'r') as file:
        config = json.load(file)
    with open(secrets_file_name, 'r') as file:
        secrets = json.load(file)
    return {
        'user': secrets['user'],
        'password': secrets['password'],
        'host': config['db_host'],
        'database': config['database'],
    }


def get_db(credentials: dict = Depends(get_credentials)):
    try:
        connection = conn.connect(**credentials)
        yield DBSession(connection)
    finally:
        connection.close()
