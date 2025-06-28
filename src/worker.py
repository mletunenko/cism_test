import asyncio
import datetime
import json

import aio_pika
from aio_pika import IncomingMessage

from core.config import settings
from core.consts import TASKS_QUEUE
from core.logger import logger
from db.postgres import get_session_context
from services.task import TaskService
from utils.enums import TaskStatusEnum


async def process_task(message: IncomingMessage) -> None:
    try:
        message_data = json.loads(message.body.decode())
        task_id = message_data["task_id"]
        logger.info(f"Получена задача: {task_id}")

        async with await get_session_context() as session:
            task = await TaskService.get_task_by_id(task_id, session)
            if not task:
                logger.warning(f"Задача {task_id} не найдена")
                await message.ack()
                return
            if task.status == TaskStatusEnum.CANCELLED:
                logger.info(f"Задача {task_id} отменена")
                await message.ack()
                return

            try:
                task.status = TaskStatusEnum.IN_PROGRESS
                task.started_at = datetime.datetime.now(datetime.timezone.utc)
                await session.commit()

                await asyncio.sleep(2)

                task.status = TaskStatusEnum.COMPLETED
                task.result = "Задача успешно выполнена"
                task.completed_at = datetime.datetime.now(datetime.timezone.utc)
                await session.commit()

                await message.ack()
                logger.info(f"Задача {task_id} завершена")

            except Exception as e:
                task.status = TaskStatusEnum.FAILED
                task.error = str(e)
                await session.commit()
                await message.nack(requeue=False)
                logger.exception("Ошибка обработки задачи")

    except Exception:
        logger.exception("Ошибка на этапе получения задачи")
        await message.nack(requeue=False)


async def consume() -> None:
    connection = await aio_pika.connect_robust(
        host=settings.rabbit.host,
        login=settings.rabbit.login,
        password=settings.rabbit.password,
    )

    async with connection:
        channel = await connection.channel()
        tasks_queue = await channel.declare_queue(TASKS_QUEUE, durable=True)
        await tasks_queue.consume(process_task, no_ack=False)
        await asyncio.Future()


if __name__ == "__main__":
    logger.info("Запуск воркера сервиса задач...")
    asyncio.run(consume())
