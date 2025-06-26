from datetime import datetime

from sqlalchemy import TIMESTAMP, Enum
from sqlalchemy.orm import Mapped, mapped_column

from utils.enums import TaskPriorityEnum, TaskStatusEnum

from .base import Base


class TaskModel(Base):
    __tablename__ = "tasks"
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    priority: Mapped[TaskPriorityEnum] = mapped_column(
        Enum(TaskPriorityEnum, name="task_priority"), default=TaskPriorityEnum.MEDIUM
    )
    status: Mapped[TaskStatusEnum] = mapped_column(Enum(TaskStatusEnum, name="task_status"), default=TaskStatusEnum.NEW)
    started_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    completed_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    result: Mapped[str] = mapped_column(default="")
    error: Mapped[str] = mapped_column(default="")
