from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

from logger_config import logger
from models import (
    DescriptionRequest, DescriptionResponse,
    DeadlineRequest, DeadlineResponse,
    PriorityRequest, PriorityResponse,
    ProcessTaskRequest, ProcessTaskResponse
)

app = FastAPI(
    title="AI_Service for Task project",
    description="API для ИИ-шной обработки запросов",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/ai")

@app.get('/')
def health_check():
    return {'health_check': 'ok'}


@router.post("/generate-description/", response_model=DescriptionResponse)
def generate_description(request: DescriptionRequest):
    logger.info('Запускаем приложение')
    response = {'description': "Something new and beautiful is builded now generate_description"}
    return response

@router.post("/suggest-deadline/", response_model=DeadlineResponse)
def suggest_deadline(request: DeadlineRequest):
    return {'data': 'Something new and beautiful is builded now suggest_deadline'}

@router.post("/analyze-priority/", response_model=PriorityResponse)
def analyze_priority(request: PriorityRequest):
    return {'data': 'Something new and beautiful is builded now analyze_priority'}

@router.post("/process-task/", response_model=ProcessTaskResponse)
def process_task(request: ProcessTaskRequest):
    return {'data': 'Something new and beautiful is builded now process_task'}

# Подключаем роутер к приложению
app.include_router(router)