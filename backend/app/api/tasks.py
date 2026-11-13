from fastapi import APIRouter, HTTPException
from typing import List, Optional
from uuid import UUID

from app.domain.task import Task, TaskCreate, TaskStatus
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])
service = TaskService()  # In production: dependency injection


@router.post("/", response_model=Task, status_code=201)
def create_task(data: TaskCreate) -> Task:
    return service.create(data)


@router.get("/", response_model=List[Task])
def list_tasks(status: Optional[TaskStatus] = None) -> List[Task]:
    return service.list(status)


@router.patch("/{task_id}/status", response_model=Task)
def update_task_status(task_id: UUID, status: TaskStatus) -> Task:
    updated = service.update_status(task_id, status)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated
