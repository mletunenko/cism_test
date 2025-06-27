import asyncio
import logging

import uvicorn
from fastapi import APIRouter, FastAPI

from api.task import router as tasks_router
from core.config import settings
from infra.rabbit import rabbitmq

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


combined_router = APIRouter(prefix="/api/v1")
combined_router.include_router(tasks_router)


app = FastAPI()
app.include_router(combined_router)


if __name__ == "__main__":
    logger.info("Запуск сервиса управления задачами...")
    asyncio.run(rabbitmq.declare_queues())
    uvicorn.run("web_server:app", host=settings.run.host, port=settings.run.port, reload=True)
    logger.info("Остановка сервиса управления задачами...")
