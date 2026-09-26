from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from ..models import TaskCreate, TaskResponse
from ..state import AppState

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _state(request: Request) -> AppState:
    return request.app.state.state


@router.post("", status_code=201, response_model=TaskResponse)
async def create_task(payload: TaskCreate, request: Request) -> TaskResponse:
    return _state(request).create_task(payload)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, request: Request) -> TaskResponse:
    task = _state(request).get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
            headers={"X-Task-Id": str(task_id)},
        )
    return task