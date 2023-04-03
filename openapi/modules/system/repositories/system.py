from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession


class SystemRepo:
    """
    A class where additional logic of operations with DB is presented.
    """

    def __init__(self, db_sess: AsyncSession):
        """
        Inits DB session.
        """

        self.db_sess = db_sess

    async def test_get_now(self) -> str:
        """
        Makes request to DB to get just time now.
        Helps to check DB connection.
        """

        res = (
            await self.db_sess.execute(select(text("NOW()")))
        ).scalar()
        return res
