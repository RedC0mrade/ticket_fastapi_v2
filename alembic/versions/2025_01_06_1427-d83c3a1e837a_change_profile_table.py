"""change profile table

Revision ID: d83c3a1e837a
Revises: a4d62c341636
Create Date: 2025-01-06 14:27:50.963114

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d83c3a1e837a"
down_revision: Union[str, None] = "a4d62c341636"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "profiles", sa.Column("user_id", sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        op.f("fk_profiles_user_id_users"),
        "profiles",
        "users",
        ["user_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_profiles_user_id_users"), "profiles", type_="foreignkey"
    )
    op.drop_column("profiles", "user_id")
