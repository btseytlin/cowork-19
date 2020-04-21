"""Searchable NeedTeam, NeedWork

Revision ID: 9b4f28f462f6
Revises: 68bddc9b137d
Create Date: 2020-04-21 08:50:32.803903

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy_searchable import sync_trigger

# revision identifiers, used by Alembic.
revision = '9b4f28f462f6'
down_revision = '68bddc9b137d'
branch_labels = None
depends_on = None


def upgrade():

    op.add_column('posting_need_team', sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True))
    op.create_index('ix_posting_need_team_search_vector', 'posting_need_team', ['search_vector'], unique=False, postgresql_using='gin')
    op.add_column('posting_need_work', sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True))
    op.create_index('ix_posting_need_work_search_vector', 'posting_need_work', ['search_vector'], unique=False, postgresql_using='gin')

    conn = op.get_bind()
    sync_trigger(conn, 'posting', 'search_vector', ['name', 'oneliner', 'description'])
    sync_trigger(conn, 'posting_need_team', 'search_vector', ['name', 'oneliner', 'description'])
    sync_trigger(conn, 'posting_need_work', 'search_vector', ['name', 'oneliner', 'description'])


def downgrade():
    op.drop_index('ix_posting_need_work_search_vector', table_name='posting_need_work')
    op.drop_column('posting_need_work', 'search_vector')
    op.drop_index('ix_posting_need_team_search_vector', table_name='posting_need_team')
    op.drop_column('posting_need_team', 'search_vector')

    conn = op.get_bind()
    sync_trigger(conn, 'posting', 'search_vector',
                 ['name', 'oneliner', 'description'])
    sync_trigger(conn, 'posting_need_team', 'search_vector',
                 ['name', 'oneliner', 'description'])
    sync_trigger(conn, 'posting_need_work', 'search_vector',
                 ['name', 'oneliner', 'description'])
