"""add dimensional tables

Revision ID: ec00d2df8824
Revises: c945497f76ac
Create Date: 2025-03-19 16:27:40.656858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec00d2df8824'
down_revision: Union[str, None] = 'c945497f76ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('postal_code', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pet_types',
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sellers',
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('postal_code', sa.String(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer_pets',
    sa.Column('type_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('breed', sa.String(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['type_id'], ['pet_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customers_and_pets',
    sa.Column('customer_id', sa.BigInteger(), nullable=False),
    sa.Column('pet_id', sa.BigInteger(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['pet_id'], ['customer_pets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('customers_and_pets')
    op.drop_table('customer_pets')
    op.drop_table('sellers')
    op.drop_table('pet_types')
    op.drop_table('customers')
    # ### end Alembic commands ###
