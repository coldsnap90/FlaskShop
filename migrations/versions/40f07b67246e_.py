"""empty message

Revision ID: 40f07b67246e
Revises: d9162ca84603
Create Date: 2023-12-13 20:13:00.873966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40f07b67246e'
down_revision = 'd9162ca84603'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('admins')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('firstname', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('profile', sa.VARCHAR(length=180), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='admins_pkey'),
    sa.UniqueConstraint('email', name='admins_email_key'),
    sa.UniqueConstraint('username', name='admins_username_key')
    )
    # ### end Alembic commands ###
