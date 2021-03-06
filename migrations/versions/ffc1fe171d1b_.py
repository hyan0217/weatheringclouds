"""empty message

Revision ID: ffc1fe171d1b
Revises: b97c4729a355
Create Date: 2022-04-12 13:09:43.410090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffc1fe171d1b'
down_revision = 'b97c4729a355'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.String(length=30), nullable=False))
    op.add_column('user', sa.Column('last_name', sa.String(length=30), nullable=False))
    op.add_column('user', sa.Column('image_file', sa.String(length=20), nullable=False))
    op.drop_column('user', 'name')
    op.drop_column('user', 'imageFile')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('imageFile', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('name', sa.VARCHAR(length=30), autoincrement=False, nullable=False))
    op.drop_column('user', 'image_file')
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###
