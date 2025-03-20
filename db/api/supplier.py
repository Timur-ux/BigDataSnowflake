from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db.database import connection
from db.models import Supplier


@connection
async def add_supplier(scalar: Supplier, session: AsyncSession, checkOnExisting=False):
    state = scalar.__getstate__().copy()
    del state["_sa_instance_state"]
    if checkOnExisting:
        if (await session.scalar(select(Supplier.id).filter_by(**state))) is not None:
            return
    session.add(scalar)
    await session.commit()
