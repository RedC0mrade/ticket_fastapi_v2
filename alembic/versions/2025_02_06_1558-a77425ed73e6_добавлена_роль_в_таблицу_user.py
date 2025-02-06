"""Добавлена роль в таблицу User

Revision ID: a77425ed73e6
Revises: 600871d30f29
Create Date: 2025-02-06 15:58:14.244461

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a77425ed73e6"
down_revision: Union[str, None] = "600871d30f29"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "user_role",
            sa.Enum("USER", "ADMIN", "SUPER_USER", name="userroleenum"),
            server_default="user",
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "user_role")
