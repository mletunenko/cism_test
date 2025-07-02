import uuid

import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from utils.enums import ClientErrorMessage, TaskStatusEnum

TASKS_PATH = "/api/v1/tasks"


# create_task

@pytest.mark.asyncio
async def test_create_task(async_client: AsyncClient, task_data: dict[str, str]) -> None:
    response = await async_client.post(TASKS_PATH, json=task_data)

    assert response.status_code == HTTP_200_OK
    assert response.json()["title"] == task_data["title"]
    assert response.json()["priority"] == task_data["priority"]


@pytest.mark.asyncio
async def test_create_task_no_description(async_client: AsyncClient) -> None:
    task_data = {
        "title": "Test Task",
        "priority": "MEDIUM",
    }

    response = await async_client.post(TASKS_PATH, json=task_data)
    assert response.status_code == HTTP_200_OK
    assert response.json()["description"] == ""


@pytest.mark.asyncio
async def test_create_task_no_title(async_client: AsyncClient) -> None:
    task_data = {
        "description": "This is a test task.",
        "priority": "MEDIUM",
    }
    response = await async_client.post(TASKS_PATH, json=task_data)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_task_invalid_priority(async_client: AsyncClient) -> None:
    task_data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "priority": "INVALID_PRIORITY",
    }
    response = await async_client.post(TASKS_PATH, json=task_data)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


# list_task

@pytest.mark.asyncio
async def test_list_task(async_client: AsyncClient, task_data: dict[str, str]) -> None:
    await async_client.post(TASKS_PATH, json=task_data)
    await async_client.post(TASKS_PATH, json=task_data)

    response = await async_client.get(TASKS_PATH)
    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_filtered_by_title_list_task(async_client: AsyncClient, task_data: dict[str, str]) -> None:
    await async_client.post(TASKS_PATH, json=task_data)

    special_data = {"title": "Special Test Task"}
    await async_client.post(TASKS_PATH, json=special_data)

    response = await async_client.get(f"{TASKS_PATH}?title={special_data['title']}")
    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == special_data["title"]


# get_task_by_id

@pytest.mark.asyncio
async def test_task_by_id(async_client: AsyncClient, task_data: dict[str, str]) -> None:
    response = await async_client.post(TASKS_PATH, json=task_data)
    assert response.status_code == HTTP_200_OK
    task_id = response.json()["id"]

    response = await async_client.get(f"{TASKS_PATH}/{task_id}")
    assert response.status_code == HTTP_200_OK
    assert response.json()["id"] == task_id


@pytest.mark.asyncio
async def test_task_by_non_existent_id(async_client: AsyncClient) -> None:
    random_task_id = str(uuid.uuid4())
    response = await async_client.get(f"{TASKS_PATH}/{random_task_id}")

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ClientErrorMessage.NOT_FOUND_TASK_ERROR.value


@pytest.mark.asyncio
async def test_task_by_invalid_id(async_client: AsyncClient, task_data: dict[str, str]) -> None:
    random_task_id = "invalid"
    response = await async_client.get(f"{TASKS_PATH}/{random_task_id}")

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


# get_task_status

@pytest.mark.asyncio
async def test_get_task_status(async_client: AsyncClient, task_data: dict[str, str]) -> None:
    response = await async_client.post(TASKS_PATH, json=task_data)
    assert response.status_code == HTTP_200_OK
    task_id = response.json()["id"]

    response = await async_client.get(f"{TASKS_PATH}/{task_id}/status")
    assert response.status_code == HTTP_200_OK
    assert response.json()["id"] == task_id
    assert response.json()["status"] in TaskStatusEnum.__members__


@pytest.mark.asyncio
async def test_get_non_existent_task_status(async_client: AsyncClient) -> None:
    random_task_id = str(uuid.uuid4())
    response = await async_client.get(f"{TASKS_PATH}/{random_task_id}/status")

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ClientErrorMessage.NOT_FOUND_TASK_ERROR.value


@pytest.mark.asyncio
async def test_get_task_status_by_invalid_id(async_client: AsyncClient) -> None:
    random_task_id = "invalid"
    response = await async_client.get(f"{TASKS_PATH}/{random_task_id}/status")

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


# cancel_task

@pytest.mark.asyncio
async def test_cancel_task(async_client: AsyncClient, task_data: dict[str, str]) -> None:
    response = await async_client.post(TASKS_PATH, json=task_data)
    assert response.status_code == HTTP_200_OK
    task_id = response.json()["id"]

    response = await async_client.delete(f"{TASKS_PATH}/{task_id}")

    assert response.status_code == HTTP_200_OK
    assert response.json()["id"] == task_id
    assert response.json()["status"] == TaskStatusEnum.CANCELLED.value


@pytest.mark.asyncio
async def test_cancel_non_existent_task(async_client: AsyncClient) -> None:
    random_task_id = str(uuid.uuid4())
    response = await async_client.delete(f"{TASKS_PATH}/{random_task_id}")

    assert response.status_code == HTTP_404_NOT_FOUND
