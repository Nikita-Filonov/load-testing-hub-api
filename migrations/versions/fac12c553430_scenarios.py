"""scenarios

Revision ID: fac12c553430
Revises: 86a4c71a7f31
Create Date: 2024-08-02 22:20:29.480600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fac12c553430'
down_revision: Union[str, None] = '86a4c71a7f31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scenarios', sa.Column('service', sa.String(), nullable=False))
    op.create_foreign_key(None, 'scenarios', 'services', ['service'], ['name'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'scenarios', type_='foreignkey')
    op.drop_column('scenarios', 'service')
    # ### end Alembic commands ###