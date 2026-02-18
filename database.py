import os
from typing import Annotated
from dotenv import load_dotenv

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

load_dotenv()

engine = create_async_engine(os.getenv("DATABASE_URL"))

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase, MappedAsDataclass):
    pass


async def get_db():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]