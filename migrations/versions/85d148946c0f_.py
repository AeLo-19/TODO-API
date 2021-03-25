"""empty message

Revision ID: 85d148946c0f
Revises: ecf6617875ab
Create Date: 2020-01-29 23:40:32.871181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85d148946c0f'
down_revision = 'ecf6617875ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('id', table_name='user')
    op.create_unique_constraint(None, 'user', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.create_index('id', 'user', ['id'], unique=True)
    # ### end Alembic commands ###