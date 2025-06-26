from contextlib import asynccontextmanager

import uvicorn
from aio_pika import connect_robust
from fastapi import APIRouter, FastAPI

from api.task import router as tasks_router
from core import infra
from core.config import settings
from core.consts import NEW_TASKS_QUEUE

combined_router = APIRouter(prefix="/api/v1")
combined_router.include_router(tasks_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        connection = await connect_robust(
            host=settings.rabbit.host,
            login=settings.rabbit.login,
            password=settings.rabbit.password,
        )
        infra.rabbit_channel = await connection.channel()
        await infra.rabbit_channel.declare_queue(NEW_TASKS_QUEUE, durable=True)
        infra.logger.info("Выполено подключение к RabbitMQ, очереди объявлены")
    except Exception as e:
        infra.logger.info(f"RabbitMQ не доступен: {e}")
        infra.rabbit_channel = None
    yield
    if infra.rabbit_channel:
        await infra.rabbit_channel.close()
        infra.logger.info("Закрыт канал RabbitMQ")


app = FastAPI(lifespan=lifespan)
app.include_router(combined_router)


if __name__ == "__main__":
    infra.logger.info("Запуск сервиса управления задачами...")
    uvicorn.run("web_server:app", host=settings.run.host, port=settings.run.port, reload=True)
    infra.logger.info("Остановка сервиса управления задачами...")
