from contextlib import asynccontextmanager

import uvicorn
from aiormq import AMQPConnectionError
from fastapi import APIRouter, FastAPI

from api.task import router as tasks_router
from core.config import settings
from infra.rabbit import RabbitMQManager
from infra.logger import logger

combined_router = APIRouter(prefix="/api/v1")
combined_router.include_router(tasks_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await RabbitMQManager.init()
        logger.info("Выполено подключение к RabbitMQ, очереди объявлены")
    except AMQPConnectionError as e:
        logger.info(f"RabbitMQ не доступен: {e}")
        rabbit_channel = None
    yield
    if rabbit_channel:
        await rabbit_channel.close()
        logger.info("Закрыт канал RabbitMQ")


app = FastAPI(lifespan=lifespan)
app.include_router(combined_router)


if __name__ == "__main__":
    logger.info("Запуск сервиса управления задачами...")
    uvicorn.run("web_server:app", host=settings.run.host, port=settings.run.port, reload=True)
    logger.info("Остановка сервиса управления задачами...")
