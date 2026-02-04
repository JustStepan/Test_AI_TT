import os
import functools
from typing import Type, TypeVar

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import AsyncOpenAI, APIError, RateLimitError, APIConnectionError
from pydantic import BaseModel

from logger_config import logger


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден в переменных окружения")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

T = TypeVar("T", bound=BaseModel)


def openai_error_handler(func):
    """Декоратор для обработки ошибок OpenAI API."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RateLimitError as e:
            logger.error(f"Rate limit exceeded: {e}")
            raise HTTPException(
                status_code=429, detail="Превышен лимит запросов к AI"
            )
        except APIConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise HTTPException(
                status_code=503, detail="AI сервис временно недоступен"
            )
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise HTTPException(
                status_code=502, detail=f"Ошибка OpenAI API: {e}"
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(
                status_code=500, detail="Внутренняя ошибка сервера"
            )

    return wrapper


@openai_error_handler
async def get_text_response(
    prompt: str, system_prompt: str = "You are a helpful assistant."
) -> str:
    """Получить текстовый ответ от OpenAI"""
    response = await client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=TEMPERATURE,
        max_tokens=1000,
    )
    return response.choices[0].message.content


@openai_error_handler
async def get_structured_response(
    prompt: str,
    response_model: Type[T],
    system_prompt: str = "You are a helpful assistant.",
) -> T:
    """Получить структурированный ответ от OpenAI через Pydantic модель."""
    response = await client.beta.chat.completions.parse(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=TEMPERATURE,
        max_tokens=1000,
        response_format=response_model,
    )
    result = response.choices[0].message.parsed
    if result is None:
        raise HTTPException(
            status_code=502, detail="Не удалось распарсить ответ от AI"
        )
    return result
