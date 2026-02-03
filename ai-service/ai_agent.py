import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import APIError, RateLimitError, APIConnectionError

from logger_config import logger

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TEMPERATURE = float(os.getenv('TEMPERATURE'))
OPENAI_MODEL = os.getenv('OPENAI_MODEL')


if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден в переменных окружения")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_llm_response(prompt_text: str) -> str:
    try:
        response = client.chat.completions.create(
            model=f"{OPENAI_MODEL}",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=TEMPERATURE,
            max_tokens=1000,
        )
        
        return response.choices[0].message.content
        
    except RateLimitError as e:
        logger.error(f"Ошибка лимитов API: {e}")
        return "Извините, превышен лимит запросов. Попробуйте позже."
    except APIConnectionError as e:
        logger.error(f"Ошибка соединения: {e}")
        return "Не удалось соединиться с сервером OpenAI."
    except APIError as e:
        logger.error(f"Ошибка API: {e}")
        return "Произошла ошибка при обработке запроса."
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        return "Произошла неизвестная ошибка."

# Тестируем локально
if __name__ == "__main__":
    user_prompt = "What is the meaning of life?"
    answer = get_llm_response(user_prompt)
    print(f"Ответ LLM: {answer}")
