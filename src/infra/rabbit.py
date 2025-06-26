from aio_pika import Channel, connect_robust
from aio_pika.exceptions import AMQPException
from infra.logger import logger
from typing import Optional
from core.consts import NEW_TASKS_QUEUE
from core.config import settings


class RabbitMQManager:
    _channel: Optional[Channel] = None
    _connection = None

    @classmethod
    async def init(cls):
        await cls._connect_and_setup()

    @classmethod
    async def _connect_and_setup(cls):
        try:
            cls._connection = await connect_robust(
                host=settings.rabbit.host,
                login=settings.rabbit.login,
                password=settings.rabbit.password,
            )
            cls._channel = await cls._connection.channel()
            await cls._channel.declare_queue(NEW_TASKS_QUEUE, durable=True)
            logger.info("RabbitMQ подключён.")
        except AMQPException as e:
            logger.warning(f"Ошибка подключения к RabbitMQ: {e}")
            cls._channel = None

    @classmethod
    async def get_channel(cls) -> Optional[Channel]:
        if cls._channel and not cls._channel.is_closed:
            return cls._channel
        logger.warning("Канал RabbitMQ закрыт, пробуем пересоздать...")
        await cls._connect_and_setup()
        return cls._channel

    @classmethod
    async def close(cls):
        if cls._channel and not cls._channel.is_closed:
            await cls._channel.close()
        if cls._connection and not cls._connection.is_closed:
            await cls._connection.close()
