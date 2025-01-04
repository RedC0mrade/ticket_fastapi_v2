"""ceate tables

Revision ID: 3976e7c78329
Revises: 
Create Date: 2025-01-04 15:55:09.661413

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3976e7c78329"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("lastname", sa.String(length=30), nullable=False),
        sa.Column("birthday", sa.Date(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tags",
        sa.Column("tag_name", sa.String(length=30), nullable=False),
        sa.Column("tag_color", sa.String(length=7), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tag_name", "tag_color", name="unique_tag"),
    )
    op.create_table(
        "users",
        sa.Column("username", sa.String(length=30), nullable=False),
        sa.Column("password", sa.LargeBinary(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
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
        ),
        sa.ForeignKeyConstraint(
            ["executor_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
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
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "ticket_tag",
        sa.Column("ticket_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tags.id"],
        ),
        sa.ForeignKeyConstraint(
            ["ticket_id"],
            ["tickets.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ticket_id", "tag_id", name="unique_tag_ticket"),
    )


def downgrade() -> None:
    op.drop_table("ticket_tag")
    op.drop_table("messages")
    op.drop_table("tickets")
    op.drop_table("users")
    op.drop_table("tags")
    op.drop_table("profiles")
