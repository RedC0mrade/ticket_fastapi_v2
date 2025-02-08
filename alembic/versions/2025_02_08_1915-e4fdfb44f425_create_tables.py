"""create tables

Revision ID: e4fdfb44f425
Revises: 
Create Date: 2025-02-08 19:15:40.499289

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.core.models.user import UserRoleType


revision: str = "e4fdfb44f425"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tags",
        sa.Column("tag_name", sa.String(length=30), nullable=False),
        sa.Column("tag_color", sa.String(length=7), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tags")),
    )
    op.create_table(
        "users",
        sa.Column("username", sa.String(length=30), nullable=False),
        sa.Column("password", sa.LargeBinary(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column(
            "user_role",
            UserRoleType(),
            server_default="user",
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )
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
    op.create_table(
        "profiles",
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("lastname", sa.String(length=30), nullable=False),
        sa.Column("birthday", sa.Date(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_profiles_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_profiles")),
    )
    op.create_table(
        "tickets",
        sa.Column("ticket_name", sa.String(length=100), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("executor_id", sa.Integer(), nullable=False),
        sa.Column("acceptor_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["acceptor_id"],
            ["users.id"],
            name=op.f("fk_tickets_acceptor_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["executor_id"],
            ["users.id"],
            name=op.f("fk_tickets_executor_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tickets")),
        sa.UniqueConstraint(
            "acceptor_id", "executor_id", "ticket_name", name="unique_ticket"
        ),
    )
    op.create_table(
        "messages",
        sa.Column("message", sa.String(length=250), nullable=True),
        sa.Column("ticket_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ticket_id"],
            ["tickets.id"],
            name=op.f("fk_messages_ticket_id_tickets"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_messages")),
    )
    op.create_table(
        "ticket_tag",
        sa.Column("ticket_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tag_id"], ["tags.id"], name=op.f("fk_ticket_tag_tag_id_tags")
        ),
        sa.ForeignKeyConstraint(
            ["ticket_id"],
            ["tickets.id"],
            name=op.f("fk_ticket_tag_ticket_id_tickets"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_ticket_tag")),
        sa.UniqueConstraint("ticket_id", "tag_id", name="unique_tag_ticket"),
    )


def downgrade() -> None:
    op.drop_table("ticket_tag")
    op.drop_table("messages")
    op.drop_table("tickets")
    op.drop_table("profiles")
    op.drop_table("friends")
    op.drop_table("followers")
    op.drop_table("black")
    op.drop_table("users")
    op.drop_table("tags")
