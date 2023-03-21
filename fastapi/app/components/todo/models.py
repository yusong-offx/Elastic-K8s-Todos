from datetime import datetime

from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, validator
from enum import Enum

from .validations import (
    title_must_max_500,
    contents_must_max_1000
)

# 할 일 가져오기 요일 Enum class에 구현
class ResponseTodo(BaseModel):
    id: int
    title: str | None
    contents: str | None
    done: bool
    create_at: datetime
    modified_at: datetime

class GetTodosEnum(Enum):
    MON = 'mon'
    TUE = 'tue'
    WED = 'wed'
    THU = 'thu'
    FRI = 'fri'
    SAT = 'sat'
    SUN = 'sun'

    async def get_todos(self, weekday, conn):
        try:
            user_id = 2
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                        SELECT
                            A.id,
                            title,
                            contents,
                            done,
                            create_at,
                            modified_at
                        from todos as A
                        JOIN (
                            SELECT id
                            FROM todo_routines
                            WHERE routine = %s
                        ) as B
                        ON A.id = B.id
                        WHERE user_id = %s;
                    """,
                    (
                        weekday,
                        user_id
                    )
                )
                todos = cursor.fetchall()
                conn.commit()
            response_todos = list()
            for todo in todos:
                response_todos.append(
                    ResponseTodo(
                        id=todo[0],
                        title=todo[1],
                        contents=todo[2],
                        done=todo[3],
                        create_at=todo[4],
                        modified_at=todo[5]
                    )
                )
            return jsonable_encoder(response_todos)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

to_database = {
    GetTodosEnum.MON : '0',
    GetTodosEnum.TUE : '1',
    GetTodosEnum.WED : '2',
    GetTodosEnum.THU : '3',
    GetTodosEnum.FRI : '4',
    GetTodosEnum.SAT : '5',
    GetTodosEnum.SUN : '6',
}

# 할 일 등록
class RegisterTodo(BaseModel):
    title: str | None = None
    contents: str | None = None
    done: bool = False
    routines: set[GetTodosEnum] | None = None

    _title_checker = validator("title", allow_reuse=True)(title_must_max_500)
    _contents_checker = validator("contents", allow_reuse=True)(contents_must_max_1000)
    
    async def db_insert(self, conn):
        try:
            # JWT 유저 추가
            user_id = 2
            now = datetime.now()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO todos (
                        user_id,
                        title,
                        contents,
                        done,
                        create_at,
                        modified_at
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        user_id,
                        self.title,
                        self.contents,
                        self.done,
                        now,
                        now
                    )
                )
                todo_id = cursor.fetchone()[0]
                for day in self.routines:
                    cursor.execute(
                        """
                        INSERT INTO todo_routines (
                            id,
                            routine
                        ) VALUES (%s, %s)
                        """,
                        (
                            todo_id,
                            to_database[day]
                        )
                    )
                conn.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# 할 일 삭제
async def db_delete(todo_id: int, conn):
    try:
        # JWT 유저
        user_id = 2
        
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM todos
                WHERE
                user_id = %s AND
                id = %s
                RETURNING
                id
                """,
                (
                    user_id,
                    todo_id
                )
            )
            todo_id = cursor.fetchone()
            conn.commit()
            if not todo_id:
                raise ValueError("todo does not exist")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))