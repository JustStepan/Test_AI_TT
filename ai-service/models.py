from pydantic import BaseModel
from typing import Literal, List
from datetime import date, datetime


class TitleRequest(BaseModel):
    title: str


class DescriptionResponse(BaseModel):
    description: str


class TitleDescriptRequest(TitleRequest):
    description: str


class DeadlineResponse(BaseModel):
    deadline: date
    reasoning: str


class PriorityResponse(BaseModel):
    priority: Literal['low', 'medium', 'high']
    reasoning: str


class CategoryResponse(BaseModel):
    category: Literal['bug', 'feature', 'improvement', 'docs', 'test']
    tags: List[str]


class ProcessTaskResponse(BaseModel):
    description: str
    priority: Literal['low', 'medium', 'high']
    deadline: datetime
    category: str
    tags: List[str]

