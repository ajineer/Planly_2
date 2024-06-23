"""making tables maybe.

Revision ID: 45152bfdd3c8
Revises: 
Create Date: 2024-06-23 10:56:03.916373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45152bfdd3c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('_password_hash', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('calendars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_calendars_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('calendar_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('start', sa.String(), nullable=False),
    sa.Column('end', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['calendar_id'], ['calendars.id'], name=op.f('fk_events_calendar_id_calendars'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.Column('calendar_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('sent_at', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['calendar_id'], ['calendars.id'], name=op.f('fk_invites_calendar_id_calendars'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], name=op.f('fk_invites_receiver_id_users'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], name=op.f('fk_invites_sender_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participants',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('calendar_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['calendar_id'], ['calendars.id'], name=op.f('fk_participants_calendar_id_calendars')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_participants_user_id_users'))
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('calendar_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['calendar_id'], ['calendars.id'], name=op.f('fk_tasks_calendar_id_calendars'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    op.drop_table('participants')
    op.drop_table('invites')
    op.drop_table('events')
    op.drop_table('calendars')
    op.drop_table('users')
    # ### end Alembic commands ###
