import os

from dotenv import load_dotenv
from openai import OpenAI, APIError, RateLimitError, APIConnectionError
from pydantic import BaseModel

from logger_config import logger


load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден в переменных окружения")

client = OpenAI(api_key=OPENAI_API_KEY)


def _OpenAi_api_errors(func):
    """Декоратор для обработки ошибок OpenAI API."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RateLimitError as e:
            logger.error(f"Rate limit exceeded: {e}")
            raise APIError(f"Превышен лимит запросов: {e}")
        except APIConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise APIError(f"Ошибка соединения с OpenAI: {e}")
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise APIError(f"Неожиданная ошибка: {e}")
    return wrapper


@_OpenAi_api_errors
def get_text_response(prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
    """Получить текстовый ответ от LLM."""
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=TEMPERATURE,
        max_tokens=1000
    )
    return response.choices[0].message.content


@_OpenAi_api_errors
def get_structured_response(
    prompt: str,
    model: BaseModel,
    system_prompt: str = "You are a helpful assistant."
) -> BaseModel:
    """Получаем структурированный(SO) ответ от LLM через Pydantic модель."""
    response = client.beta.chat.completions.parse(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=TEMPERATURE,
        max_tokens=1000,
        response_format=model
    )
    return response.choices[0].message.parsed