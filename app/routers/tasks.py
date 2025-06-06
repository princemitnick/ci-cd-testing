from fastapi import APIRouter, HTTPException
from app.models import Task

from app.crud import get_task, get_tasks, create_task, delete_task

router = APIRouter()

@router.get("/", response_model=list[Task])
def read_tasks():
    return get_tasks()

@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=Task)
def add_task(task: Task):
    return create_task()

@router.delete("/{task_id}")
def remove_task(task_id: int):
    result = delete_task(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}