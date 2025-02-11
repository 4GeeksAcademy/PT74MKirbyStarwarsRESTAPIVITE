"""empty message

Revision ID: c01f2ac59d78
Revises: 
Create Date: 2025-02-11 00:31:49.917993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c01f2ac59d78'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('terrain', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('username', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id_favorites', sa.Integer(), nullable=True),
    sa.Column('favorite_planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['favorite_planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id_favorites'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('home_planet', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['home_planet'], ['planet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id_favorites', sa.Integer(), nullable=True),
    sa.Column('favorite_person_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['favorite_person_id'], ['person.id'], ),
    sa.ForeignKeyConstraint(['user_id_favorites'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_people')
    op.drop_table('person')
    op.drop_table('favorite_planets')
    op.drop_table('users')
    op.drop_table('planet')
    # ### end Alembic commands ###
