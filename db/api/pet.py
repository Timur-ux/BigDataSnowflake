from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db.database import connection
from db.models import Breed, CustomerPet, PetCategory, PetType

@connection
async def get_pet_type_id(name: str, session: AsyncSession) -> int | None:
    return (await session.scalar(select(PetType.id).where(PetType.name == name)))

@connection
async def get_pet_category_id(name: str, session: AsyncSession) -> int | None:
    return (await session.scalar(select(PetCategory.id).where(PetCategory.name == name)))

@connection
async def get_pet_breed_id(name: str, session: AsyncSession) -> int | None:
    return (await session.scalar(select(Breed.id).where(Breed.name == name)))

@connection
async def add_pet(scalar: CustomerPet, session: AsyncSession, checkOnExisting=False):
    state = scalar.__getstate__().copy()
    del state["_sa_instance_state"]
    if checkOnExisting:
        if (await session.scalar(select(CustomerPet.id).filter_by(**state))) is not None:
            return

    await session.commit()


