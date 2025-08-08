"""create_tables"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = 'create_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Таблица buildings
    op.create_table('buildings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=False, unique=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('activities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=255), nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('level', sa.Integer(), server_default='1'),
        sa.ForeignKeyConstraint(['parent_id'], ['activities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('organizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('building_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['building_id'], ['buildings.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('phones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('number', sa.String(length=50), nullable=False, unique=True),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('organization_activity',
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('activity_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('organization_id', 'activity_id')
    )


def downgrade():
    op.drop_table('organization_activity')
    op.drop_table('phones')
    op.drop_table('organizations')
    op.drop_table('activities')
    op.drop_table('buildings')
