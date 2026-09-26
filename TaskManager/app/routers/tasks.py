from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from ..models import TaskCreate, TaskResponse
from ..state import AppState

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _state(request: Request) -> AppState:
    return request.app.state.state


@router.post(
    "",
    status_code=201,
    response_model=TaskResponse,
    responses={
        201: {
            "description": "Задание успешно создано",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Пример задания",
                        "description": "Короткое описание",
                        "priority": 3,
                        "created_at": "2024-01-01T12:00:00"
                    }
                }
            },
        },
        422: {
            "description": "Ошибка валидации входных данных",
            "content": {
                "application/json": {
                    "example": {"detail": "Ошибка валидации входных данных"}
                }
            },
        },
    },
)
async def create_task(payload: TaskCreate, request: Request) -> TaskResponse:
    """Создать новое задание.

    payload: тело запроса с полями задания (title, description, priority).
    request: объект запроса, используется для доступа к приложению и состоянию.
    Возвращает созданную запись задания в формате TaskResponse.
    """

    return _state(request).create_task(payload)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    responses={
        200: {
            "description": "Запись задания найдена",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Пример задания",
                        "description": "Короткое описание",
                        "priority": 3,
                        "created_at": "2024-01-01T12:00:00"
                    }
                }
            },
        },
        404: {
            "description": "Задание не найдено",
            "content": {
                "application/json": {
                    "example": {"detail": "Задание не найдено"}
                }
            },
            "headers": {
                "X-Task-Id": {
                    "description": "Идентификатор запрошенного задания",
                    "schema": {"type": "string"},
                }
            },
        },
        422: {
            "description": "Ошибка валидации параметров запроса или пути",
            "content": {
                "application/json": {
                    "example": {"detail": "Ошибка валидации параметров запроса или пути"}
                }
            },
        },
    },
)
async def get_task(task_id: int, request: Request) -> TaskResponse:
    """Получить задание по идентификатору.

    task_id: целочисленный идентификатор задания.
    request: объект запроса, используется для доступа к приложению и состоянию.
    Возвращает TaskResponse при успешном нахождении записи.
    Вызывает HTTPException(404) с заголовком X-Task-Id если запись не найдена.
    """

    task = _state(request).get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
            headers={"X-Task-Id": str(task_id)},
        )
    return task