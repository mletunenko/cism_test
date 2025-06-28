import json

from aio_pika import Message
from aio_pika.abc import AbstractChannel
from sqlalchemy.ext.asyncio import AsyncSession

from core.consts import PRIORITY_MAP, TASKS_QUEUE
from core.logger import logger
from schemas.task import TaskOut
from services.task import TaskService
from utils.enums import TaskStatusEnum


class TaskPublisher:
    @staticmethod
    async def publish_task_message(data: TaskOut, session: AsyncSession, rabbit_channel: AbstractChannel) -> None:
        if not rabbit_channel:
            logger.warning("Не удалось получить канал RabbitMQ для отправки задачи.")
            return
        body = {"task_id": str(data.id)}
        json_body = json.dumps(body)
        await rabbit_channel.default_exchange.publish(
            Message(body=json_body.encode(), priority=PRIORITY_MAP[data.priority]),
            routing_key=TASKS_QUEUE,
        )
        await TaskService.update_task_status(data.id, session, TaskStatusEnum.PENDING)
