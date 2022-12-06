from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession


class SystemRepo:
    """
    A class where additional logic of operations with DB is presented.
    """

    def __init__(self, db_sess: AsyncSession):
        """
        Init DB session.

        :param db_sess: Created DB session
        """
        self.db_sess = db_sess

    async def get_now(self) -> str:
        """
        Method get current DB time
        :return: Current DB datetime
        """
        data = (await self.db_sess.execute(select(text("NOW()")))).scalar()
        return data
