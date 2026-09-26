from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class GenerateTextRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=8000)


class GenerateTextResponse(BaseModel):
    result: str


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = None
    priority: int = Field(ge=1, le=5)


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: int
    created_at: datetime