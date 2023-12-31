"""update role

Revision ID: 646de2be88f7
Revises: 78172ce90787
Create Date: 2023-08-01 17:27:13.357620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '646de2be88f7'
down_revision = '78172ce90787'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_projects_title', table_name='projects')
    op.create_index(op.f('ix_projects_title'), 'projects', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_projects_title'), table_name='projects')
    op.create_index('ix_projects_title', 'projects', ['title'], unique=False)
    # ### end Alembic commands ###
