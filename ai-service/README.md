# AI Service для Task Tracker

Асинхронный микросервис для интеллектуальной обработки задач с использованием OpenAI API.

## Возможности

- Генерация описания задачи по названию
- Автоматическое определение дедлайна
- Анализ приоритета задачи
- Категоризация и тегирование
- Комплексная обработка задачи (все функции сразу)

## Технологии

- Python 3.11+
- FastAPI (асинхронный)
- OpenAI API (AsyncOpenAI, GPT-4o-mini)
- Pydantic v2 (валидация с Field constraints)
- Loguru (структурированное логирование)

## Архитектура

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Frontend   │────▶│  AI Service │────▶│  OpenAI API │
│  :3000      │     │  :8001      │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Получение OpenAI API ключа

1. Перейдите на [platform.openai.com](https://platform.openai.com/)
2. Зарегистрируйтесь или войдите в аккаунт
3. Перейдите в **Settings → API Keys**
4. Нажмите **Create new secret key**
5. Скопируйте ключ (показывается только один раз)
6. Пополните баланс в **Billing** (минимум $5)

## Установка и запуск

### Локальный запуск

```bash
cd ai-service

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Настроить переменные окружения
cp .env.example .env
# Отредактируйте .env и добавьте OPENAI_API_KEY

# Запустить сервер
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Запуск через Docker

```bash
docker-compose up --build ai-service
```

### Запуск всей системы

```bash
docker-compose up --build
```

## Конфигурация

Переменные окружения (файл `.env`):

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `OPENAI_API_KEY` | API ключ OpenAI | обязательный |
| `OPENAI_MODEL` | Модель GPT | gpt-4o-mini |
| `TEMPERATURE` | Креативность (0.0-1.0) | 0.7 |
| `ALLOWED_ORIGINS` | CORS origins через запятую | http://localhost:3000 |

## API Endpoints

Базовый URL: `http://localhost:8001`

### Health Check
```http
GET /
Response: {"status": "ok"}
```

### Генерация описания
```http
POST /ai/generate-description
Content-Type: application/json

Request:
{
  "title": "Реализовать авторизацию"  // min 3, max 500 символов
}

Response:
{
  "description": "Необходимо разработать систему авторизации..."
}
```

### Предложение дедлайна
```http
POST /ai/suggest-deadline
Content-Type: application/json

Request:
{
  "title": "Исправить критический баг",
  "description": "Баг в продакшене вызывает падение сервиса"  // min 5, max 2000
}

Response:
{
  "deadline": "2026-02-05",
  "reasoning": "Критические баги требуют немедленного исправления"
}
```

### Анализ приоритета
```http
POST /ai/analyze-priority
Content-Type: application/json

Request:
{
  "title": "Добавить темную тему",
  "description": "Улучшение UX для пользователей"
}

Response:
{
  "priority": "low",  // low | medium | high
  "reasoning": "Улучшение UX, не критично для функционала"
}
```

### Категоризация
```http
POST /ai/categorize
Content-Type: application/json

Request:
{
  "title": "Написать unit тесты для API",
  "description": "Покрыть тестами основные endpoints"
}

Response:
{
  "category": "test",  // bug | feature | improvement | docs | test
  "tags": ["testing", "quality", "api"]
}
```

### Комплексная обработка
```http
POST /ai/process-task
Content-Type: application/json

Request:
{
  "title": "Оптимизировать запросы к базе данных"
}

Response:
{
  "description": "Провести анализ и оптимизацию SQL-запросов...",
  "priority": "high",
  "deadline": "2026-02-10T00:00:00",
  "category": "improvement",
  "tags": ["database", "performance", "optimization"]
}
```

## Примеры curl

```bash
# Генерация описания
curl -X POST http://localhost:8001/ai/generate-description \
  -H "Content-Type: application/json" \
  -d '{"title": "Добавить кэширование"}'

# Комплексная обработка
curl -X POST http://localhost:8001/ai/process-task \
  -H "Content-Type: application/json" \
  -d '{"title": "Рефакторинг модуля авторизации"}'
```

## Структура проекта

```
ai-service/
├── main.py              # Точка входа FastAPI
├── ai_agent.py          # AsyncOpenAI клиент и обработка ошибок
├── models.py            # Pydantic модели с валидацией
├── prompts.py           # Системные промпты
├── logger_config.py     # Конфигурация loguru
├── routes/
│   ├── __init__.py
│   └── task_ai_post.py  # Async API endpoints
├── logs/                # Логи приложения
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

## Обработка ошибок

Сервис возвращает понятные HTTP-коды:

| Код | Ситуация |
|-----|----------|
| 422 | Невалидные входные данные (title < 3 символов и т.д.) |
| 429 | Превышен лимит запросов к OpenAI |
| 502 | Ошибка ответа от OpenAI API |
| 503 | OpenAI API недоступен |

## Логирование

- **stdout** — INFO и выше, цветной вывод
- **logs/app.log** — DEBUG, ротация в 10:00, хранение 30 дней, сжатие zip

## Swagger

После запуска: `http://localhost:8001/docs`
