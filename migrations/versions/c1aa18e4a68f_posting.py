"""posting

Revision ID: c1aa18e4a68f
Revises: ed0cb63af8ee
Create Date: 2020-03-27 09:48:32.763336

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql
from sqlalchemy_searchable import sync_trigger

# revision identifiers, used by Alembic.
revision = 'c1aa18e4a68f'
down_revision = 'ed0cb63af8ee'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    op.create_table('posting',
        sa.Column('id', postgresql.UUID(), nullable=False),
        sa.Column('user_id', postgresql.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('display', sa.Boolean(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cv_url', sa.String(), nullable=True),
        sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posting_id'), 'posting', ['id'], unique=False)

    op.create_index('ix_posting_search_vector', 'posting', ['search_vector'], unique=False, postgresql_using='gin')

    op.drop_index('ix_candidate_id', table_name='candidate')
    op.drop_index('ix_candidate_search_vector', table_name='candidate')
    op.drop_table('candidate')

    sync_trigger(conn, 'posting', 'search_vector', ['name', 'description'])


def downgrade():
    conn = op.get_bind()

    op.create_table('candidate',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('display', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cv_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('search_vector', postgresql.TSVECTOR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='candidate_pkey')
    )
    op.create_index('ix_candidate_search_vector', 'candidate', ['search_vector'], unique=False)
    op.create_index('ix_candidate_id', 'candidate', ['id'], unique=False)
    op.drop_index('ix_posting_search_vector', table_name='posting')
    op.drop_index(op.f('ix_posting_id'), table_name='posting')

    sync_trigger(conn, 'posting', 'search_vector', ['name', 'description'])
    op.drop_table('posting')

