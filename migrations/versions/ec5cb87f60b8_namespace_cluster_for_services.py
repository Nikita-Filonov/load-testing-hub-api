"""namespace_cluster_for_services

Revision ID: ec5cb87f60b8
Revises: 545e00abc28c
Create Date: 2024-07-31 22:38:40.716083

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ec5cb87f60b8'
down_revision: Union[str, None] = '545e00abc28c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('services', sa.Column('namespace', sa.String(length=250), nullable=True))
    op.add_column('services', sa.Column('cluster', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('services', 'cluster')
    op.drop_column('services', 'namespace')
    # ### end Alembic commands ###