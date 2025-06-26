import datetime
import uuid
from functools import partial

from pydantic import UUID4
from sqlalchemy import TIMESTAMP, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    naming_conventions: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
    metadata = MetaData(naming_convention=naming_conventions)
    id: Mapped[UUID4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=partial(datetime.datetime.now, datetime.timezone.utc),
    )
