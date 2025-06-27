import json
import logging

from aio_pika import Message
from aio_pika.abc import AbstractChannel

from core.consts import PRIORITY_MAP, TASKS_QUEUE
from schemas.task import TaskOut

logger = logging.getLogger(__name__)

class TaskPublisher:
    @staticmethod
    async def create_task(data: TaskOut, rabbit_channel: AbstractChannel) -> None:
        if not rabbit_channel:
            logger.warning("Не удалось получить канал RabbitMQ для отправки задачи.")
            return

        body = {
                "task_id": str(data.id)
            }

        json_body = json.dumps(body)
        await rabbit_channel.default_exchange.publish(
            Message(
                body=json_body.encode(),
                priority=PRIORITY_MAP[data.priority]
            ),
            routing_key=TASKS_QUEUE,
        )
