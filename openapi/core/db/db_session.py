"""
Contains functions to operate with database sessions.
"""

from contextlib import asynccontextmanager
from typing import Optional

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from openapi.core.db.main import engine
from openapi.core.exceptions import DefaultException


@asynccontextmanager
async def db_session(
    existing_session: Optional[AsyncSession] = None
) -> AsyncSession:
    """
    Connects to DB and returns session
    if there is no existing_session
    """

    logger.info(f"Calling db_session, existing_session = {existing_session}")
    if existing_session:
        yield existing_session
        # no make commit here, just pass through

    else:
        new_session = None
        async_session = sessionmaker(
            bind=engine,
            future=True,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        try:
            new_session = async_session()
            yield new_session
            await new_session.commit()

        except Exception as ex:
            await _handle_session_exception(exception=ex, session=new_session)
        finally:
            if new_session:
                await new_session.close()


async def _handle_session_exception(
    exception: Exception,
    session: Optional[AsyncSession]
):
    """
    Log unknown exception in details if encountered.
    """

    if session:
        await session.rollback()
    if not isinstance(exception, DefaultException):
        # getting detailed traceback for unknown exception
        logger.exception(exception)
    raise exception
