"""addemail1

Revision ID: c62324a53293
Revises: b8ff49dd15ea
Create Date: 2022-05-13 16:37:18.030503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c62324a53293'
down_revision = 'b8ff49dd15ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('email', sa.Column('email1', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('email', 'email1')
    # ### end Alembic commands ###
