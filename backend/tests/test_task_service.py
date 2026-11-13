from datetime import date, timedelta
from uuid import UUID

import pytest

from app.domain.task import TaskCreate, TaskStatus
from app.services.task_service import TaskService


@pytest.fixture
def service() -> TaskService:
    return TaskService()


def test_create_valid_task(service: TaskService) -> None:
    data = TaskCreate(title="Implement strict typing")
    task = service.create(data)
    assert isinstance(task.id, UUID)
    assert task.title == "Implement strict typing"
    assert task.status == TaskStatus.TODO
    assert task.description is None
    assert len(service.list()) == 1


def test_due_date_in_past_rejected() -> None:
    past = date.today() - timedelta(days=1)
    with pytest.raises(ValueError, match="Due date cannot be in the past"):
        TaskCreate(title="Invalid task", due_date=past)


def test_due_date_today_accepted() -> None:
    today = date.today()
    data = TaskCreate(title="Valid", due_date=today)
    assert data.due_date == today


def test_update_status(service: TaskService) -> None:
    task = service.create(TaskCreate(title="Progress me"))
    updated = service.update_status(task.id, TaskStatus.IN_PROGRESS)
    assert updated is not None
    assert updated.status == TaskStatus.IN_PROGRESS
    assert updated.updated_at >= task.created_at
    assert service.get(task.id).status == TaskStatus.IN_PROGRESS


def test_update_nonexistent_returns_none(service: TaskService) -> None:
    fake_id = UUID("00000000-0000-0000-0000-000000000000")
    assert service.update_status(fake_id, TaskStatus.DONE) is None


def test_list_filters_by_status(service: TaskService) -> None:
    service.create(TaskCreate(title="A"))
    t2 = service.create(TaskCreate(title="B"))
    service.update_status(t2.id, TaskStatus.DONE)
    assert len(service.list()) == 2
    assert len(service.list(TaskStatus.TODO)) == 1
    assert len(service.list(TaskStatus.DONE)) == 1


def test_extra_fields_forbidden() -> None:
    with pytest.raises(ValueError):
        TaskCreate(title="Ok", unknown_field="boom")  # type: ignore
