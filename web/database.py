import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.engine import URL

from dotenv import load_dotenv

load_dotenv()


def construct_sqlalchemy_url() -> URL:
    return URL.create(
        drivername='postgresql+asyncpg',
        username=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        port=os.getenv('DP_PORT')
    )


engine = create_async_engine(construct_sqlalchemy_url(), echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    """Подключение к сессии бд."""
    async with async_session() as session:
        async with session.begin():
            yield session
