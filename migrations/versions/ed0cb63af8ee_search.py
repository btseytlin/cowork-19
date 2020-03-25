"""search

Revision ID: ed0cb63af8ee
Revises: 582229d25623
Create Date: 2020-03-25 11:24:49.704668

"""
import os.path as path
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy_searchable import sync_trigger

# revision identifiers, used by Alembic.
revision = 'ed0cb63af8ee'
down_revision = '582229d25623'
branch_labels = None
depends_on = None


def run_sqlalchemy_searchable_sql(conn):
    """
    With alembic and sqlalchemy_searchable we run SQL statements before table creation. These statements enable searching
    See:
    - https://conorliv.com/alembic-migration-execute-raw-sql.html
    - https://github.com/kvesteri/sqlalchemy-searchable/issues/67
    """
    with open(path.join('migrations', 'searchable_expressions.sql')) as f:
        sql_expressions = f.read()
    conn.execute(sql_expressions)


def upgrade():
    conn = op.get_bind()
    run_sqlalchemy_searchable_sql(conn)
    op.add_column('candidate', sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType('name', 'search_vector'), nullable=True))
    sync_trigger(conn, 'candidate', 'search_vector', ['name', 'description'])
    op.create_index('ix_candidate_search_vector', 'candidate', ['search_vector'], unique=False, postgresql_using='gin')


def downgrade():
    conn = op.get_bind()
    op.drop_index('ix_candidate_search_vector', table_name='candidate')
    op.drop_column('candidate', 'search_vector')
    sync_trigger(conn, 'candidate', 'search_vector', ['name', 'description'])
