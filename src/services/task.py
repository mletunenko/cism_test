from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from models import TaskModel
from schemas.task import TaskIn, TaskListParams
from utils.enums import ClientErrorMessage, TaskStatusEnum


class TaskService:
    @staticmethod
    async def create_task(data: TaskIn, session: AsyncSession) -> TaskModel:
        task = TaskModel(
            title=data.title,
            description=data.description,
            priority=data.priority,
        )
        session.add(task)
        await session.commit()
        return task

    @staticmethod
    async def get_task_list(session: AsyncSession, query_params: TaskListParams) -> list[TaskModel]:
        stmt = select(TaskModel).where(*query_params.build_filters())
        stmt = stmt.offset((query_params.pagination.page_number - 1) * query_params.pagination.page_size).limit(
            query_params.pagination.page_size
        )

        result = await session.execute(stmt)
        task_list = list(result.scalars().all())
        return task_list

    @staticmethod
    async def get_task_by_id(task_id: UUID4, session: AsyncSession) -> TaskModel:
        stmt = select(TaskModel).where(TaskModel.id == task_id)
        result = await session.execute(stmt)
        task = result.scalars().first()
        if not task:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=ClientErrorMessage.NOT_FOUND_TASK_ERROR.value,
            )
        return task

    @staticmethod
    async def update_task_status(task_id: UUID4, session: AsyncSession, status: TaskStatusEnum) -> TaskModel:
        task = TaskService.get_task_by_id(task_id, session)
        task.status = status
        await session.commit()
