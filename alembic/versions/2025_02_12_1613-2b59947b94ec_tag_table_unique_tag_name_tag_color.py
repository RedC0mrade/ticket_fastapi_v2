"""tag table unique tag_name, tag_color

Revision ID: 2b59947b94ec
Revises: e4fdfb44f425
Create Date: 2025-02-12 16:13:45.658875

"""

from typing import Sequence, Union

from alembic import op


revision: str = "2b59947b94ec"
down_revision: Union[str, None] = "e4fdfb44f425"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        op.f("uq_tags_tag_color"), "tags", ["tag_color"]
    )
    op.create_unique_constraint(op.f("uq_tags_tag_name"), "tags", ["tag_name"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_tags_tag_name"), "tags", type_="unique")
    op.drop_constraint(op.f("uq_tags_tag_color"), "tags", type_="unique")
