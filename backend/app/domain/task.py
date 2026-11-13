from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskCreate(BaseModel):
    """Input model for creating a task. Sealed: frozen + extra forbid."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[date] = None

    @field_validator("due_date")
    @classmethod
    def due_date_not_in_past(cls, v: Optional[date]) -> Optional[date]:
        if v is not None and v < date.today():
            raise ValueError("Due date cannot be in the past")
        return v


class Task(BaseModel):
    """Domain entity. Immutable after creation. Sealed model."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[date] = None

    def with_status(self, status: TaskStatus) -> "Task":
        """Return a new immutable Task with updated status and timestamp."""
        return self.model_copy(
            update={"status": status, "updated_at": datetime.utcnow()}
        )
