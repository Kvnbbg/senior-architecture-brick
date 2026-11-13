from typing import List, Optional
from uuid import UUID

from app.domain.task import Task, TaskCreate, TaskStatus


class TaskService:
    """Isolated in-memory service implementing core business rules.

    In a real system this would be backed by a repository (PostgreSQL via SQLAlchemy).
    Kept pure for unit-testability and architectural isolation.
    """

    def __init__(self) -> None:
        self._store: dict[UUID, Task] = {}

    def create(self, data: TaskCreate) -> Task:
        task = Task(
            title=data.title,
            description=data.description,
            due_date=data.due_date,
        )
        self._store[task.id] = task
        return task

    def update_status(self, task_id: UUID, status: TaskStatus) -> Optional[Task]:
        existing = self._store.get(task_id)
        if existing is None:
            return None
        updated = existing.with_status(status)
        self._store[task_id] = updated
        return updated

    def list(self, status: Optional[TaskStatus] = None) -> List[Task]:
        tasks = list(self._store.values())
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

    def get(self, task_id: UUID) -> Optional[Task]:
        return self._store.get(task_id)
