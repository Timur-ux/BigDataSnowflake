from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db.database import connection
from db.models import Sale


@connection
async def add_sale(scalar: Sale, session: AsyncSession, checkOnExisting=False):
    state = scalar.__getstate__().copy()
    del state["_sa_instance_state"]
    if checkOnExisting:
        if (await session.scalar(select(Sale.id).filter_by(date = scalar.date, customer_id = scalar.customer_id, seller_id = scalar.seller_id, product_id = scalar.seller_id))) is not None:
            return
    session.add(scalar)
    await session.commit()

