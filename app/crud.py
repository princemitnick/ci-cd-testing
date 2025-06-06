from app.models import Task
from app.fake_db import fake_db
fake_db = fake_db

def get_tasks():
    return fake_db

def get_task(task_id: int):
    return next((task for task in fake_db if task.id == task_id), None)

def create_task(task: Task):
    if get_task(task.id):
        raise ValueError("ID already used")
    fake_db.append(task)
    return task

def delete_task(task_id: int):
    global fake_db
    fake_db = [task for task in fake_db if task.id != task_id]




