from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from models import TaskModel
from schemas.task import TaskIn, TaskListParams
from utils.enums import ClientErrorMessage


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


#     @staticmethod
#     async def get_profile_by_email(email: EmailStr, session: AsyncSession) -> ProfileModel | None:
#         stmt = select(ProfileModel).where(ProfileModel.email == email)
#         result = await session.execute(stmt)
#         profile = result.scalars().first()
#         return profile
#
#     @staticmethod
#     async def get_profile_by_phone(phone: str, session: AsyncSession) -> ProfileModel | None:
#         stmt = select(ProfileModel).where(ProfileModel.phone == phone)
#         result = await session.execute(stmt)
#         profile = result.scalars().first()
#         return profile
#

#

#
#     @staticmethod
#     async def delete_profile(profile_id: UUID4, session: AsyncSession) -> None:
#         profile = await ProfileService.get_profile_by_id(profile_id, session)
#         await session.delete(profile)
#         await session.commit()
#
#     @staticmethod
#     async def update_profile(profile_id: UUID4, data: ProfilePatch, session: AsyncSession) -> ProfileModel:
#         profile = await ProfileService.get_profile_by_id(profile_id, session)
#         update_data = data.model_dump(exclude_unset=True)
#         for field, value in update_data.items():
#             setattr(profile, field, value)
#         await session.commit()
#         return profile
#
#     @staticmethod
#     async def get_profile_list(session: AsyncSession, query_params: ProfileListParams) -> list[ProfileModel]:
#         stmt = select(ProfileModel)
#         if query_params.birth_day:
#             stmt = stmt.filter(extract("day", ProfileModel.birth_date) == query_params.birth_day)
#         if query_params.birth_month:
#             stmt = stmt.filter(extract("month", ProfileModel.birth_date) == query_params.birth_month)
#         if query_params.email:
#             stmt = stmt.filter(ProfileModel.email == query_params.email)
#         stmt = stmt.offset((query_params.pagination.page_number - 1) * query_params.pagination.page_size).limit(
#             query_params.pagination.page_size
#         )
#
#         result = await session.execute(stmt)
#         profile_list = list(result.scalars().all())
#         return profile_list
#
#     @staticmethod
#     async def is_phone_unique(
#         new_phone: str,
#         profile_id: UUID4,
#         session: AsyncSession,
#     ) -> bool:
#         stmt = select(ProfileModel).where(ProfileModel.id != profile_id).where(ProfileModel.phone == new_phone)
#         result = await session.execute(stmt)
#         existent_profile = result.scalars().first()
#         if existent_profile:
#             return False
#         return True
#
#     @staticmethod
#     async def update_email(
#         data: UpdateEmailRequest,
#         session: AsyncSession,
#     ) -> None:
#         profile = await ProfileService.get_profile_by_email(data.old_email, session)
#         if not profile:
#             raise HTTPException(
#                 status_code=HTTP_404_NOT_FOUND,
#                 detail=ClientErrorMessage.NOT_FOUND_PROFILE_ERROR.value,
#             )
#         profile.email = data.new_email
#         await session.commit()
