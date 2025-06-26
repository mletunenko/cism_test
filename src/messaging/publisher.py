import json

from aio_pika import Message

from core import infra
from core.consts import NEW_TASKS_QUEUE
from schemas.task import TaskOut


class TaskPublisher:
    @staticmethod
    async def create_task(data: TaskOut,
) -> None:
        if infra.rabbit_channel is None:
            infra.logger.warning("RabbitMQ не подключён")
            return

        body = {
            "task_id": str(data.id),
            "priority": data.priority.value
        }

        json_body = json.dumps(body)
        await infra.rabbit_channel.default_exchange.publish(
            Message(body=json_body.encode()),
            routing_key=NEW_TASKS_QUEUE,
        )
