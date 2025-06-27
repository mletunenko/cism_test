from datetime import datetime

from fastapi import Depends
from pydantic import UUID4, BaseModel

from models import TaskModel
from schemas.base import PaginationParams
from utils.enums import TaskPriorityEnum, TaskStatusEnum


class TaskIn(BaseModel):
    title: str
    description: str = ""
    priority: TaskPriorityEnum = TaskPriorityEnum.MEDIUM


class TaskOut(BaseModel):
    id: UUID4
    title: str
    description: str = ""
    priority: TaskPriorityEnum
    status: TaskStatusEnum
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: str = ""
    error: str = ""


class TaskListParams(BaseModel):
    title: str | None = None
    priority: TaskPriorityEnum | None = None
    status: TaskStatusEnum | None = None
    started_after: datetime | None = None
    started_before: datetime | None = None
    completed_after: datetime | None = None
    completed_before: datetime | None = None
    pagination: PaginationParams = Depends()

    def build_filters(self) -> list:
        filters = []

        if self.title:
            filters.append(TaskModel.title.ilike(f"%{self.title}%"))
        if self.priority:
            filters.append(TaskModel.priority == self.priority)
        if self.status:
            filters.append(TaskModel.status == self.status)
        if self.started_after:
            filters.append(TaskModel.started_at >= self.started_after)
        if self.started_before:
            filters.append(TaskModel.started_at <= self.started_before)
        if self.completed_after:
            filters.append(TaskModel.completed_at >= self.completed_after)
        if self.completed_before:
            filters.append(TaskModel.completed_at <= self.completed_before)

        return filters


class TaskStatusResponse(BaseModel):
    id: UUID4
    status: TaskStatusEnum


class TaskCancelResponse(BaseModel):
    id: UUID4
    new_status: TaskStatusEnum
