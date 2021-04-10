"""empty message

Revision ID: c2e0b016b8a5
Revises: 8d473623f3ef
Create Date: 2021-04-10 00:32:18.060044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2e0b016b8a5'
down_revision = '8d473623f3ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('people', sa.Column('idx', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'people', ['id'])
    op.add_column('planet', sa.Column('idx', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'planet', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'planet', type_='unique')
    op.drop_column('planet', 'idx')
    op.drop_constraint(None, 'people', type_='unique')
    op.drop_column('people', 'idx')
    # ### end Alembic commands ###
