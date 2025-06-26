import json

from aio_pika import Message
from aio_pika.abc import AbstractChannel

from core.consts import NEW_TASKS_QUEUE
from schemas.task import TaskOut


class TaskPublisher:
    @staticmethod
    async def create_task(data: TaskOut, rabbit_channel: AbstractChannel,
) -> None:
        body = {
            "task_id": str(data.id),
            "priority": data.priority.value
        }


        json_body = json.dumps(body)
        await rabbit_channel.default_exchange.publish(
            Message(body=json_body.encode()),
            routing_key=NEW_TASKS_QUEUE,
        )
