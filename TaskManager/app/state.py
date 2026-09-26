from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .models import TaskCreate, TaskResponse


@dataclass(slots=True)
class AppState:
    tasks: list[TaskResponse] = field(default_factory=list)
    next_task_id: int = 1

    def create_task(self, payload: TaskCreate) -> TaskResponse:
        task = TaskResponse(
            id=self.next_task_id,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            created_at=datetime.now(timezone.utc),
        )
        self.next_task_id += 1
        self.tasks.append(task)
        return task

    def get_task(self, task_id: int) -> TaskResponse | None:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None