"""empty message

Revision ID: dbcef579cabf
Revises: 6ae97d704bd0
Create Date: 2023-12-12 21:52:06.864510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbcef579cabf'
down_revision = '6ae97d704bd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('adminfirstname', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('adminusername', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('adminemail', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('adminpassword', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('adminprofile', sa.VARCHAR(length=180), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('adminemail', name='users_adminemail_key'),
    sa.UniqueConstraint('adminusername', name='users_adminusername_key')
    )
    # ### end Alembic commands ###