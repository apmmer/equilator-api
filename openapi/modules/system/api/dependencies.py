from sqlalchemy.ext.asyncio import AsyncSession

from openapi.core.db.db_session import db_session


async def get_system_session() -> AsyncSession:
    async with db_session() as sess:
        yield sess
