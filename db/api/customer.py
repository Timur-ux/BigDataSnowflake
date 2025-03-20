from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db.database import connection
from db.models import Customer


@connection
async def get_customer_by_id(id: int, session: AsyncSession) -> Customer | None:
    return (await session.scalar(select(Customer).where(Customer.id == id)))

@connection
async def add_customer(scalar: Customer, session: AsyncSession, checkOnExisting=False):
    state = scalar.__getstate__().copy()
    del state["_sa_instance_state"]
    res = (await session.scalar(select(Customer).filter_by(**state)))
    if checkOnExisting:
        if res  is not None:
            return  res
    session.add(scalar)
    await session.commit()
    await session.refresh(scalar)
    return scalar
