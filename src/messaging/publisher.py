import json

from aio_pika import Message

from infra.logger import logger
from core.consts import NEW_TASKS_QUEUE
from infra.rabbit import RabbitMQManager
from schemas.task import TaskOut


class TaskPublisher:
    @staticmethod
    async def create_task(data: TaskOut) -> None:
        rabbit_channel = await RabbitMQManager.get_channel()
        if not rabbit_channel:
            logger.warning("Не удалось получить канал RabbitMQ для отправки задачи.")
            return

        body = {
                "task_id": str(data.id),
                "priority": data.priority.value
            }

        json_body = json.dumps(body)
        await rabbit_channel.default_exchange.publish(
            Message(body=json_body.encode()),
            routing_key=NEW_TASKS_QUEUE,
        )
