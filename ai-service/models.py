from pydantic import BaseModel
from typing import Literal, List
from datetime import date, datetime


class DescriptionRequest(BaseModel):
    title: str


class DescriptionResponse(BaseModel):
    description: str


class DeadlineRequest(BaseModel):
    title: str
    description: str


class DeadlineResponse(BaseModel):
    deadline: date
    reasoning: str


class PriorityRequest(BaseModel):
    title: str
    description: str


class PriorityResponse(BaseModel):
    priority: Literal['low', 'medium', 'high']
    reasoning: str


class ProcessTaskRequest(BaseModel):
    title: str


class ProcessTaskResponse(BaseModel):
    description: str
    priority: Literal['low', 'medium', 'high']
    deadline: datetime
    category: str
    tags: List[str]
