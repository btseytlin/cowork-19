"""non-nullable

Revision ID: 5868e2e008c6
Revises: dbc43e7336ef
Create Date: 2020-04-01 16:25:05.242321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5868e2e008c6'
down_revision = 'dbc43e7336ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posting', 'cv_url',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('posting', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('posting', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('posting', 'oneliner',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posting', 'oneliner',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('posting', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('posting', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('posting', 'cv_url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
