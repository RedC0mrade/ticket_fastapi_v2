"""create models

Revision ID: 26aeeb5256eb
Revises: d83c3a1e837a
Create Date: 2025-01-11 18:48:54.501690

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "26aeeb5256eb"
down_revision: Union[str, None] = "d83c3a1e837a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "followers",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("follower_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["follower_id"],
            ["users.id"],
            name=op.f("fk_followers_follower_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_followers_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_followers")),
        sa.UniqueConstraint("user_id", "follower_id", name="unique_follower"),
    )
    op.create_table(
        "friends",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("friend_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["friend_id"],
            ["users.id"],
            name=op.f("fk_friends_friend_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_friends_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_friends")),
        sa.UniqueConstraint("user_id", "friend_id", name="unique_friend"),
    )
    op.drop_constraint("unique_tag", "tags", type_="unique")


def downgrade() -> None:
    op.create_unique_constraint(
        "unique_tag", "tags", ["tag_name", "tag_color"]
    )
    op.drop_table("friends")
    op.drop_table("followers")
