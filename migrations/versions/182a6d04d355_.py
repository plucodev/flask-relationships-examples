"""empty message

Revision ID: 182a6d04d355
Revises: 79c9c9eca21e
Create Date: 2019-11-18 19:04:24.961623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '182a6d04d355'
down_revision = '79c9c9eca21e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'image', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'image', type_='foreignkey')
    op.drop_column('image', 'user_id')
    # ### end Alembic commands ###
