from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db.database import connection
from db.models import Brand, Color, Material, Product, ProductCategory

@connection
async def get_product_cat_id(name: str, session: AsyncSession) -> int | None:
    return (await session.scalar(select(ProductCategory.id).where(ProductCategory.name == name)))

@connection
async def get_color_id(name: str, session: AsyncSession) -> int | None:
    return (await session.scalar(select(Color.id).where(Color.name == name)))

@connection
async def get_brand_id(name: str, session: AsyncSession) -> int | None:
    return (await session.scalar(select(Brand.id).where(Brand.name == name)))

@connection
async def get_material_id(name: str, session: AsyncSession) -> int | None:
    return (await session.scalar(select(Material.id).where(Material.name == name)))


@connection
async def add_product(scalar: Product, session: AsyncSession, checkOnExisting=False):
    state = scalar.__getstate__().copy()
    del state["_sa_instance_state"]
    if checkOnExisting:
        if (await session.scalar(select(Product.id).filter_by(**state))) is not None:
            return
    session.add(scalar)
    await session.commit()
