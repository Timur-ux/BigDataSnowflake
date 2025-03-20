from functools import wraps
from sqlalchemy import BigInteger
from sqlalchemy.ext.asyncio.session import AsyncAttrs, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine
from db.config import settings

DATABASE_URL = settings.get_db_url()

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)


engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def connection(method):
    """
    Decorator to automatically create async session and call method
    Rollback on exception
    Commit at end

    * method must have `session` argument with type `AsyncSession`
    """
    @wraps(method)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            try:
                return await method(*args, session = session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.commit()

    return wrapper
