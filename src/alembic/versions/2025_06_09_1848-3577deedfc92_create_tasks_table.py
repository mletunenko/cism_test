"""create tasks table

Revision ID: 3577deedfc92
Revises:
Create Date: 2025-06-09 18:48:15.059334

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3577deedfc92"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("priority", sa.Enum("LOW", "MEDIUM", "HIGH", name="task_priority"), nullable=False),
        sa.Column(
            "status",
            sa.Enum("NEW", "PENDING", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED", name="task_status"),
            nullable=False,
        ),
        sa.Column("started_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("completed_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("result", sa.String(), nullable=False),
        sa.Column("error", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tasks")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tasks")
    status = sa.Enum(name="task_status")
    priority = sa.Enum(name="task_priority")

    status.drop(op.get_bind())
    priority.drop(op.get_bind())
