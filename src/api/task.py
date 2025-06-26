from fastapi import APIRouter, HTTPException, Depends
from pydantic import UUID4

from db.postgres import SessionDep
from models import TaskModel
from schemas.task import TaskIn, TaskOut, TaskStatusResponse, TaskListParams
from services.task import TaskService
from utils.enums import ClientErrorMessage, TaskStatusEnum

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", summary="Создать новую задачу", response_model=TaskOut)
async def create_task(data: TaskIn, session: SessionDep) -> TaskModel:
    task = await TaskService.create_task(data, session)
    return task


@router.get("", summary="Получить список задач", response_model=list[TaskOut])
async def list_task(session: SessionDep, query_params: TaskListParams = Depends()) -> list[TaskModel]:
    task_list = await TaskService.get_task_list(session, query_params)
    return task_list


@router.get("/{task_id}", summary="Получить задачу по id", response_model=TaskOut)
async def task_by_id(task_id: UUID4, session: SessionDep) -> TaskModel:
    task = await TaskService.get_task_by_id(task_id, session)
    return task


@router.get("/{task_id}/status", summary="Получить статус задачи", response_model=TaskStatusResponse)
async def task_status(task_id: UUID4, session: SessionDep) -> TaskStatusResponse:
    task = await TaskService.get_task_by_id(task_id, session)
    return task


# @router.delete("/{task_id}", summary="Отменить задачу")
# async def cancel_task(task_id: UUID4, session: SessionDep):
#     task = TaskService.get_task_by_id(task_id, session)
#
#     if task.status in [
#         TaskStatusEnum.COMPLETED,
#         TaskStatusEnum.FAILED,
#         TaskStatusEnum.CANCELLED,
#         TaskStatusEnum.IN_PROGRESS,
#     ]:
#         raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=ClientErrorMessage.CANNOT_CANCEL_TASK_ERROR)
