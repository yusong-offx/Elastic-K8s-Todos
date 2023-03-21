from fastapi import APIRouter, Response, Depends
from fastapi.responses import JSONResponse

from components.database import get_db
from components.todo.models import (
    GetTodosEnum,
    RegisterTodo,
    to_database,
    db_delete,
)

router = APIRouter(
    prefix="/todo",
    tags=["Todos"]
)

@router.post("/register")
async def todo_test(todo: RegisterTodo, db = Depends(get_db)):
    await todo.db_insert(db)
    return Response(status_code=201)

@router.get("/{weekday}")
async def get_todo(weekday: GetTodosEnum, db = Depends(get_db)):
    return JSONResponse(content=await weekday.get_todos(to_database[weekday], db))

@router.put("/{todo_id}")
async def update_todo(todo_id: int):
    return

@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, db = Depends(get_db)):
    await db_delete(todo_id, db)
    return Response(status_code=200)