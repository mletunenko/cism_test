import logging
from typing import Annotated

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractConnection
from aio_pika.exceptions import AMQPException
from fastapi import Depends

from core.config import settings
from core.consts import TASKS_QUEUE

logger = logging.getLogger(__name__)


class RabbitMQConnection:
    def __init__(self) -> None:
        self.connection = None

    async def connect(self) -> AbstractConnection|None:
        if not self.connection or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(
                host=settings.rabbit.host,
                login=settings.rabbit.login,
                password=settings.rabbit.password,
            )
        return self.connection

    async def get_channel(self) -> AbstractChannel|None:
        try:
            connection = await self.connect()
            return await connection.channel()
        except AMQPException as e:
            logger.warning(f"Ошибка подключения к RabbitMQ: {e}")
            return None

    async def close(self) -> None:
        if self.connection:
            self.connection.close()

    async def declare_queues(self) -> None:
        channel = await self.get_channel()
        if channel:
            await channel.declare_queue(TASKS_QUEUE, durable=True)


rabbitmq = RabbitMQConnection()


async def get_rabbitmq_channel() -> AbstractChannel|None:
    channel = await rabbitmq.get_channel()
    if channel:
        async with await rabbitmq.get_channel() as channel:
            yield channel
    else:
        yield None



RabbitDep = Annotated[AbstractChannel, Depends(get_rabbitmq_channel)]