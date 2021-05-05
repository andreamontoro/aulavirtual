"""empty message

Revision ID: 4075b3fa54fe
Revises: 2fa8de1662e1
Create Date: 2021-05-05 09:05:37.724396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4075b3fa54fe'
down_revision = '2fa8de1662e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('participation_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=50), nullable=True),
    sa.Column('code_description', sa.String(length=120), nullable=True),
    sa.Column('code_type', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('course_name', sa.String(length=50), nullable=True),
    sa.Column('institution_name', sa.String(length=50), nullable=True),
    sa.Column('date_expire', sa.DateTime(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participation_redeem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('participation_code', sa.String(length=50), nullable=True),
    sa.Column('code_description', sa.String(length=120), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('course_name', sa.String(length=50), nullable=True),
    sa.Column('institution_name', sa.String(length=50), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('participation_redeem')
    op.drop_table('participation_code')
    # ### end Alembic commands ###
