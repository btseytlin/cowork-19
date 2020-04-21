"""oneliner

Revision ID: dbc43e7336ef
Revises: c1aa18e4a68f
Create Date: 2020-04-01 16:24:09.155732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbc43e7336ef'
down_revision = 'c1aa18e4a68f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posting', sa.Column('oneliner', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posting', 'oneliner')
    # ### end Alembic commands ###
