from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from starlette.status import HTTP_404_NOT_FOUND

from models import TaskModel
from schemas.task import TaskIn, TaskListParams
from services.task import TaskService
from tests.unit.conftest import make_mock_session
from utils.enums import ClientErrorMessage, TaskStatusEnum


@pytest.mark.asyncio
async def test_create_task(mock_session: MagicMock, task_data: TaskIn) -> None:
    task = await TaskService.create_task(task_data, mock_session)

    assert task.title == task_data.title
    assert task.description == task_data.description
    assert task.priority == task_data.priority

    mock_session.add.assert_called_once_with(task)
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_task_invalid_priority(mock_session: MagicMock) -> None:
    invalid_data = {"title": "", "description": "This is a test task.", "priority": "HARD"}

    with pytest.raises(ValidationError) as exc_info:
        await TaskService.create_task(TaskIn(**invalid_data), mock_session)

    assert "priority" in str(exc_info.value)


@pytest.mark.asyncio
async def test_create_task_no_title(mock_session: MagicMock) -> None:
    invalid_data = {"description": "This is a test task.", "priority": "MEDIUM"}

    with pytest.raises(ValidationError) as exc_info:
        await TaskService.create_task(TaskIn(**invalid_data), mock_session)

    assert "title" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_task_list(task_list_params: TaskListParams) -> None:
    task_list = [
        TaskModel(title="Test Task", description="This is a test task.", priority="MEDIUM"),
    ]
    mock_session = make_mock_session(scalars_all=task_list)
    result = await TaskService.get_task_list(mock_session, task_list_params)

    assert result == task_list
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_task_list_filtered(task_list_params: TaskListParams) -> None:
    task_2 = TaskModel(title="filtered", description="This is a test task.", priority="HIGH")
    task_list = [task_2]

    mock_session = make_mock_session(scalars_all=task_list)
    params = task_list_params.model_copy()
    params.title = "filtered"
    result = await TaskService.get_task_list(mock_session, params)

    assert len(result) == 1
    assert result[0].title == "filtered"
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_task_list_empty(task_list_params: TaskListParams) -> None:
    task_list = []
    mock_session = make_mock_session(scalars_all=task_list)

    result = await TaskService.get_task_list(mock_session, task_list_params)

    assert result == task_list
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_task_by_id(task_model: TaskModel) -> None:
    mock_session = make_mock_session(scalars_first=task_model)

    result = await TaskService.get_task_by_id(task_model.id, mock_session)

    assert result == task_model
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_task_by_id_not_found(empty_mock_session: AsyncMock) -> None:
    with pytest.raises(HTTPException) as exc_info:
        await TaskService.get_task_by_id("invalid_id", empty_mock_session)

    assert exc_info.value.status_code == HTTP_404_NOT_FOUND
    assert exc_info.value.detail == ClientErrorMessage.NOT_FOUND_TASK_ERROR.value
    empty_mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_task_status(task_model: TaskModel) -> None:
    mock_session = make_mock_session(scalars_first=task_model)

    updated_task = await TaskService.update_task_status(task_model.id, mock_session, TaskStatusEnum.COMPLETED.value)

    assert updated_task.status == TaskStatusEnum.COMPLETED
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()
