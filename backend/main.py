from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
import json
import os

app = FastAPI(title="Task Tracker API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data storage (in-memory, можно заменить на БД)
tasks_db = []
task_id_counter = 1

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    status: str = "pending"  # pending, in_progress, completed
    priority: str = "medium"  # low, medium, high
    deadline: Optional[str] = None
    created_at: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[str] = None

@app.get("/")
def root():
    return {"message": "Task Tracker API is running"}

@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    """Получить все задачи"""
    return tasks_db

@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Получить конкретную задачу"""
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/api/tasks", response_model=Task)
def create_task(task: Task):
    """Создать новую задачу"""
    global task_id_counter
    
    task_dict = task.dict()
    task_dict["id"] = task_id_counter
    task_dict["created_at"] = datetime.now().isoformat()
    
    tasks_db.append(task_dict)
    task_id_counter += 1
    
    return task_dict

@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    """Обновить задачу"""
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        task[key] = value
    
    return task

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    """Удалить задачу"""
    global tasks_db
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    return {"message": "Task deleted successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "tasks_count": len(tasks_db)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
