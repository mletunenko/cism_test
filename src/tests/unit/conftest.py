from typing import Optional
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from models import TaskModel
from models.base import Base
from schemas.base import PaginationParams
from schemas.task import TaskIn, TaskListParams


@pytest_asyncio.fixture
def mock_session() -> MagicMock:
    return MagicMock(spec=AsyncSession)


@pytest_asyncio.fixture
def task_data() -> TaskIn:
    return TaskIn(title="Test Task", description="This is a test task.", priority="MEDIUM")


@pytest_asyncio.fixture
def task_list_params() -> TaskListParams:
    return TaskListParams(pagination=PaginationParams(page_number=1, page_size=10))


@pytest_asyncio.fixture
def task_model() -> TaskModel:
    return TaskModel(
        id="123e4567-e89b-12d3-a456-426655440000",
        title="Test Task",
        description="This is a test task.",
        priority="MEDIUM",
    )


@pytest.fixture
def empty_mock_session() -> AsyncMock:
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = []
    mock_scalars.first.return_value = None

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.return_value = mock_result
    return mock_session


def make_mock_session(
    *,
    scalars_all: list[Base] = None,
    scalars_first: Optional[Base] = None,
) -> MagicMock:
    """
    Создает мок AsyncSession с гибким заданием результатов.
    Аргументы:
        scalars_all: список, который должен вернуть scalars().all()
        scalars_first: значение, которое должен вернуть scalars().first()
    Возвращает:
        мок AsyncSession с настроенными методами
    """

    mock_scalars = MagicMock()

    if scalars_all is not None:
        mock_scalars.all.return_value = scalars_all
    if scalars_first is not None:
        mock_scalars.first.return_value = scalars_first

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    mock_session = MagicMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=mock_result)
    return mock_session
