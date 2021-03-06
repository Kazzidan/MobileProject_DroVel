"""Add_isAdmin_users

Revision ID: b8ff49dd15ea
Revises: 9d6f2793b695
Create Date: 2022-05-11 22:12:37.012900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8ff49dd15ea'
down_revision = '9d6f2793b695'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('isAdmin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'isAdmin')
    # ### end Alembic commands ###
