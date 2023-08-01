"""add SET NULL for tasks

Revision ID: ea9d2a95d127
Revises: d91173e73cf7
Create Date: 2023-07-30 05:30:30.432275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea9d2a95d127'
down_revision = 'd91173e73cf7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'assignee_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_constraint('tasks_assignee_id_fkey', 'tasks', type_='foreignkey')
    op.create_foreign_key(None, 'tasks', 'users', ['assignee_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.create_foreign_key('tasks_assignee_id_fkey', 'tasks', 'users', ['assignee_id'], ['id'], ondelete='CASCADE')
    op.alter_column('tasks', 'assignee_id',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###