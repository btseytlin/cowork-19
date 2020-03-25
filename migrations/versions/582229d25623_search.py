"""search

Revision ID: 582229d25623
Revises: 0d91f8d3abda
Create Date: 2020-03-25 10:43:14.179450

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_searchable import sync_trigger

# revision identifiers, used by Alembic.
revision = '582229d25623'
down_revision = '0d91f8d3abda'
branch_labels = None
depends_on = None


def upgrade():
    pass
    # conn = op.get_bind()
    # sync_trigger(conn, 'Candidate', 'search_vector', ['name', 'description'])


def downgrade():
    pass
    # conn = op.get_bind()
    # sync_trigger(conn, 'Candidate', 'search_vector', ['name', 'description'])
