from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    id: int
    task: str
    done: bool = False

todos: List[Item] = []
next_id = 0

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/create-todo")
def create_todo(item: str = Form(...)):
    global next_id
    todos.append(Item(id=next_id, task=item, done=False))
    next_id += 1
    return RedirectResponse("/", status_code=303)

@app.post("/complete-todo")
def complete_todo(completed: List[int] = Form([])):
    for todo in todos:
        todo.done = todo.id in completed
    return RedirectResponse("/", status_code=303)
