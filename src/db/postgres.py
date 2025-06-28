from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import settings

engine = create_async_engine(
    url=settings.db.url,
    pool_size=5,
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with new_session() as session:
        yield session


async def get_session_context() -> AsyncSession:
    return new_session()


SessionDep = Annotated[AsyncSession, Depends(get_session)]
