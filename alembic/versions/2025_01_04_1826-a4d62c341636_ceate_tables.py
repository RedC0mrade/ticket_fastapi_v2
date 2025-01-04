"""ceate tables

Revision ID: a4d62c341636
Revises: 
Create Date: 2025-01-04 18:26:40.775209

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a4d62c341636"
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_profiles")),
    )
    op.create_table(
        "tags",
        sa.Column("tag_name", sa.String(length=30), nullable=False),
        sa.Column("tag_color", sa.String(length=7), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tags")),
        sa.UniqueConstraint("tag_name", "tag_color", name="unique_tag"),
    )
    op.create_table(
        "users",
        sa.Column("username", sa.String(length=30), nullable=False),
        sa.Column("password", sa.LargeBinary(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
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
    op.drop_table("users")
    op.drop_table("tags")
    op.drop_table("profiles")
