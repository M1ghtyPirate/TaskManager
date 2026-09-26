from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Входная модель для создания задания."""

    title: str = Field(..., min_length=3, max_length=100, description="Заголовок задания (3-100 символов)")
    description: Optional[str] = Field(None, description="Дополнительное описание задания (опционально)")
    priority: int = Field(..., ge=1, le=5, description="Приоритет задания: целое от 1 до 5")


class TaskResponse(BaseModel):
    """Модель ответа для представления задания."""

    id: int = Field(..., description="Уникальный идентификатор задания")
    title: str = Field(..., description="Заголовок задания")
    description: Optional[str] = Field(None, description="Подробное описание задания (опционально)")
    priority: int = Field(..., description="Приоритет задания (1-5)")
    created_at: datetime = Field(..., description="Метка времени создания записи")
