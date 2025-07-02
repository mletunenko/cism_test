import httpx
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from db.postgres import get_session
from models.base import Base
from web_server import app

TEST_DATABASE_URL = "postgresql+asyncpg://user:password@127.0.0.1:5433/test_tasks"


@pytest_asyncio.fixture(scope="session")
async def test_engine() -> AsyncEngine:
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=pool.NullPool,
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database(test_engine: AsyncEngine) -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session(test_engine: AsyncEngine) -> AsyncSession:
    async_session = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def clean_tables(session: AsyncSession) -> None:
    for table in reversed(Base.metadata.sorted_tables):
        await session.execute(table.delete())
    await session.commit()


@pytest_asyncio.fixture(autouse=True)
def override_get_session(session: AsyncSession) -> None:
    async def _override() -> AsyncSession:
        yield session

    app.dependency_overrides[get_session] = _override
    yield
    app.dependency_overrides.pop(get_session, None)


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    async with httpx.AsyncClient(
        base_url="http://test",
        transport=ASGITransport(app=app),
    ) as client:
        yield client


@pytest.fixture
def task_data() -> dict:
    return {
        "title": "Test Task",
        "description": "This is a test task.",
        "priority": "LOW",
    }
