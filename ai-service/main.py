from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.task_ai_post import router


app = FastAPI(
    title="AI_Service for Task project",
    description="API для ИИ-шной обработки запросов",
)
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def health_check():
    return {'health_check': 'ok'}
