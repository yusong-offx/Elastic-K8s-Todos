from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

from components.user import user
from components.todo import todo

servers = [
    {
        "url" : "http://127.0.0.1:8000",
        "description" : "FastAPI(Python3) server",
    },
    {
        "url" : "http://127.0.0.1:8000",
        "description" : "Fiber(Go) server",
    },
    {
        "url" : "http://127.0.0.1:8000",
        "description" : "Actix-web(Rust) server",
    },
]

app = FastAPI(
    title="todo-list",
    servers=servers
)

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(todo.router)


