from fastapi import APIRouter

from logger_config import logger
from ai_agent import get_text_response, get_structured_response
from prompts import (
    GET_DESCRIPTIONS,
    dedline_prompt,
    priority_prompt,
    category_prompt,
    process_task_prompt,
)
from models import (
    TitleRequest,
    DescriptionResponse,
    TitleDescriptRequest,
    DeadlineResponse,
    PriorityResponse,
    CategoryResponse,
    ProcessTaskResponse,
)


router = APIRouter(prefix="/ai", tags=["ai_task"])


@router.post("/generate-description", response_model=DescriptionResponse)
def get_description(request: TitleRequest):
    logger.info(f"Начинаем формировать описание для задачи: {request.title}")
    prompt = f"{GET_DESCRIPTIONS}\nЗадача пользователя:{request.title}"
    response = get_text_response(prompt)
    logger.info(
        f"Описание задачи успешно сформировано. Длина ответа {len(response)}"
    )
    return {"description": response}


@router.post("/suggest-deadline", response_model=DeadlineResponse)
def get_deadline(request: TitleDescriptRequest):
    logger.info(f"Начинаем формировать дедлайн для задачи: {request.title}")
    prompt = dedline_prompt(request.title, request.description)
    response = get_structured_response(prompt, DeadlineResponse)
    logger.info(
        f"Дедлайн определен: {response.deadline}.\nОбоснование {response.reasoning}"
    )
    return response


@router.post("/analyze-priority", response_model=PriorityResponse)
def get_priority(request: TitleDescriptRequest):
    logger.info(f"Начинаем оценивать приоритет задачи: {request.title}")
    prompt = priority_prompt(request.title, request.description)
    response = get_structured_response(prompt, PriorityResponse)
    logger.info(
        f"Приоритет определен: {response.priority}.\nОбоснование {response.reasoning}"
    )
    return response


@router.post("/categorize", response_model=CategoryResponse)
def get_category(request: TitleDescriptRequest):
    logger.info(f"Начинаем оценивать категорию задачи: {request.title}")
    prompt = category_prompt(request.title, request.description)
    response = get_structured_response(prompt, CategoryResponse)
    logger.info(
        f"Категория определена: {response.category}.\nТеги: {response.tags}"
    )
    return response


@router.post("/process-task", response_model=ProcessTaskResponse)
async def process_task(request: TitleRequest):
    logger.info(f'Комплексная обработка задачи: {request.title}')
    prompt = process_task_prompt(request.title)
    response = get_structured_response(prompt, ProcessTaskResponse)
    logger.info(f"""Задача обработана:
                    Категория: {response.category},
                    Приоритет: {response.priority},
                    Теги: {response.tags},
                    Дедлайн: {response.deadline}""")
    return response
