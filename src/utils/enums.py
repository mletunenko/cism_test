import enum


class TaskPriorityEnum(enum.StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskStatusEnum(enum.StrEnum):
    NEW = "NEW"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class ClientErrorMessage(enum.StrEnum):
    NOT_FOUND_TASK_ERROR = "Задача не найдена"
    CANNOT_CANCEL_TASK_ERROR = "Задача не может быть отменена"
