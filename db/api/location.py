from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db.database import connection
from db.models import City, Country, State

@connection
async def get_country_id(name: str, session: AsyncSession) -> int | None:
    return (await session.scalar(select(Country.id).where(Country.name == name)))

@connection
async def get_city_id(name: str, session: AsyncSession) -> int | None:
    return (await session.scalar(select(City.id).where(City.name == name)))

@connection
async def get_state_id(name: str, session: AsyncSession) -> int | None:
    return (await session.scalar(select(State.id).where(State.name == name)))
