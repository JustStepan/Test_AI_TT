from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class TitleRequest(BaseModel):
    """Запрос с названием задачи."""
    title: str = Field(..., min_length=3, max_length=500)


class DescriptionResponse(BaseModel):
    """Ответ с описанием задачи."""
    description: str


class TitleDescriptRequest(TitleRequest):
    """Запрос с названием и описанием задачи."""
    description: str = Field(..., min_length=5, max_length=2000)


class DeadlineResponse(BaseModel):
    """Ответ с предложенным дедлайном."""
    deadline: date
    reasoning: str


class PriorityResponse(BaseModel):
    """Ответ с определённым приоритетом."""
    priority: Literal['low', 'medium', 'high']
    reasoning: str


class CategoryResponse(BaseModel):
    """Ответ с категорией и тегами."""
    category: Literal['bug', 'feature', 'improvement', 'docs', 'test']
    tags: list[str]


class ProcessTaskResponse(BaseModel):
    """Комплексный ответ с полным анализом задачи."""
    description: str
    priority: Literal['low', 'medium', 'high']
    deadline: datetime
    category: str
    tags: list[str]
