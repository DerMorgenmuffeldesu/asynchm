import os

from sqlalchemy import JSON, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "secret")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_DB = os.getenv("MYSQL_DB", "swapi")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

# Строка подключения для MySQL
MYSQL_DSN = f"mysql+asyncmy://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_async_engine(MYSQL_DSN, echo=True)
DbSession = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = "swapi_people"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    birth_year: Mapped[str] = mapped_column(String(20))
    eye_color: Mapped[str] = mapped_column(String(20))
    films: Mapped[str] = mapped_column(Text)  # Список фильмов как строка
    gender: Mapped[str] = mapped_column(String(10))
    hair_color: Mapped[str] = mapped_column(String(20))
    height: Mapped[str] = mapped_column(String(10))
    homeworld: Mapped[str] = mapped_column(String(100))
    mass: Mapped[str] = mapped_column(String(10))
    skin_color: Mapped[str] = mapped_column(String(20))
    species: Mapped[str] = mapped_column(Text)  # Список видов как строка
    starships: Mapped[str] = mapped_column(Text)  # Список кораблей как строка
    vehicles: Mapped[str] = mapped_column(Text)  # Список транспорта как строка
    url: Mapped[str] = mapped_column(String(100))
    created: Mapped[str] = mapped_column(String(50))
    edited: Mapped[str] = mapped_column(String(50))


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
