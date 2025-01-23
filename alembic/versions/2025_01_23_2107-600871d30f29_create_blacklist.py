"""create blacklist

Revision ID: 600871d30f29
Revises: 26aeeb5256eb
Create Date: 2025-01-23 21:07:44.273904

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "600871d30f29"
down_revision: Union[str, None] = "26aeeb5256eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "black",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("black_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["black_id"], ["users.id"], name=op.f("fk_black_black_id_users")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_black_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_black")),
        sa.UniqueConstraint("user_id", "black_id", name="black_list"),
    )


def downgrade() -> None:
    op.drop_table("black")
