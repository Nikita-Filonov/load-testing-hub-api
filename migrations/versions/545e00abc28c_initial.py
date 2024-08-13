"""initial

Revision ID: 545e00abc28c
Revises: 
Create Date: 2024-07-30 06:58:12.881737

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '545e00abc28c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('services',
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('url', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('load_test_results',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('trigger_ci_pipeline_url', sa.String(), nullable=True),
    sa.Column('trigger_ci_project_title', sa.String(), nullable=True),
    sa.Column('trigger_ci_project_version', sa.String(), nullable=True),
    sa.Column('load_tests_ci_pipeline_url', sa.String(), nullable=True),
    sa.Column('number_of_users', sa.Integer(), nullable=False),
    sa.Column('total_requests', sa.Integer(), nullable=False),
    sa.Column('total_failures', sa.Integer(), nullable=False),
    sa.Column('max_response_time', sa.Float(), nullable=False),
    sa.Column('min_response_time', sa.Float(), nullable=False),
    sa.Column('average_response_time', sa.Float(), nullable=False),
    sa.Column('total_requests_per_second', sa.Float(), nullable=False),
    sa.Column('total_failures_per_second', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('finished_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('service', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['service'], ['services.name'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('history_results',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('datetime', sa.DateTime(timezone=True), nullable=False),
    sa.Column('number_of_users', sa.Integer(), nullable=False),
    sa.Column('requests_per_second', sa.Float(), nullable=False),
    sa.Column('failures_per_second', sa.Float(), nullable=False),
    sa.Column('average_response_time', sa.Float(), nullable=False),
    sa.Column('response_time_percentile_95', sa.Float(), nullable=False),
    sa.Column('load_test_results_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['load_test_results_id'], ['load_test_results.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('method_results',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('method', sa.String(length=200), nullable=False),
    sa.Column('protocol', sa.String(length=20), nullable=False),
    sa.Column('number_of_requests', sa.Integer(), nullable=False),
    sa.Column('number_of_failures', sa.Integer(), nullable=False),
    sa.Column('max_response_time', sa.Float(), nullable=False),
    sa.Column('min_response_time', sa.Float(), nullable=False),
    sa.Column('total_response_time', sa.Float(), nullable=False),
    sa.Column('requests_per_second', sa.Float(), nullable=False),
    sa.Column('failures_per_second', sa.Float(), nullable=False),
    sa.Column('average_response_time', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('service', sa.String(), nullable=False),
    sa.Column('load_test_results_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['load_test_results_id'], ['load_test_results.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['service'], ['services.name'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ratio_results',
    sa.Column('ratio_total', sa.JSON(), nullable=False),
    sa.Column('ratio_per_class', sa.JSON(), nullable=False),
    sa.Column('load_test_results_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['load_test_results_id'], ['load_test_results.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('load_test_results_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ratio_results')
    op.drop_table('method_results')
    op.drop_table('history_results')
    op.drop_table('load_test_results')
    op.drop_table('services')
    # ### end Alembic commands ###
