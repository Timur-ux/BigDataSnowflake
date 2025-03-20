from typing import List
from sqlalchemy.ext.asyncio.session import AsyncSession
from db.database import connection
from db.models import RawData

@connection
async def addRawData(data: List[RawData], session: AsyncSession) -> None:
    for row in data:
        session.add(row)
    await session.commit()

