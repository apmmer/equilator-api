from typing import Any, Dict, List, Optional

from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.sql.selectable import Select

from openapi.core.db.db_session import db_session
from openapi.core.exceptions import (DefaultException, GotMultipleObjectsError,
                                     ObjectNotFoundError, SQLException)
from openapi.core.schemas import Pagination


class BaseRepository:
    """
    Provides async operations for any abstract
    item (model) using SQLAlchemy syntax.
    To keep the order in the code: еach "public" method should
    include only basic python types in the parameters,
    otherwise - it should be a "private" method.
    """

    # This is a limitation for querying db
    max_page_size = 5000

    def __init__(
        self,
        model: DeclarativeMeta
    ):
        self.model = model

    async def add_one(
        self,
        data: Dict[str, Any],
        existing_session: Optional[AsyncSession] = None
    ) -> DeclarativeMeta:
        """
        Inserts new record in DB. No checking if object exists:
        "try and rollback" instead of double request.

        Args:
            data (Dict[str, Any]): validated data for record creation.
            make_commit (bool, optional): Parameter to force or
                avoid making session's commit. If make_commit == False:
                session.flush() will be applied instead.
                Defaults to True.
            existing_session (Optional[AsyncSession]) - SqlAlchemy
                AsyncSession, created by sqlalchemy.orm.sessionmaker.
                Defaults to None.

        Raises:
            SQLException: An exception with a description of the details,
            suitable for the FastAPI server response

        Notes:
            All fields validations should be maden on higher level.

        Returns:
            DeclarativeMeta: an instance of SqlAlchemy model
        """

        new_model: DeclarativeMeta = self.model(**data)
        async with db_session(existing_session=existing_session) as session:
            session.add(new_model)
            try:
                if not existing_session:
                    await session.commit()
                else:
                    # if there is an existing session, its possible to
                    # make decision about commit outside of this function
                    await session.flush()
            except IntegrityError as ex:
                self._handle_integrity_error(ex)

        return new_model

    def _handle_integrity_error(self, exception: IntegrityError):
        """
        Encapsulates logic of IntegrityError exception handling.

        Args:
            exception (IntegrityError): exception, raised inside
                sqlalchemy, during db querying

        Raises:
            SQLException: its known exception, share details
            DefaultException: unknown IntegrityError
        """

        detail = exception.orig.__context__.detail
        logger.error(f"Catched IntegrityError, msg: {exception}")
        if "already exists" in detail:
            raise SQLException(detail=detail)
        # unknown IntegrityError, getting full traceback
        logger.exception(exception)
        raise DefaultException()

    async def _execute_get_many(
        self,
        query: Select,
        session: AsyncSession,
    ) -> List[DeclarativeMeta]:
        """
        Makes request to DB with given query.

        Args:
            query (Select) - select sqlalchemy query
            session (AsyncSession) - opened sqlalchemy session.

        Returns:
            List[DeclarativeMeta] - result of query execution (a list)
            with not serialized objects.
        """

        result: List[DeclarativeMeta] = (
            await session.execute(query)
        ).scalars().unique().all()
        return result

    async def _get_many_limited_pagination(
        self,
        filters: Dict[str, Any],
        pagination: Pagination,
        in_filters: Dict[str, List] = {},
        existing_session: Optional[AsyncSession] = None,
    ) -> List[DeclarativeMeta]:
        """
        Makes request to DB, avoiding huge results, using pagination.

        Args:
            filters (Dict[str, Any]) - filters for query compiling.
            pagination (Pagination) - pagination info.
            in_filters (Dict[str, List]) - more complex, "IN" filters.
            existing_session (Optional[AsyncSession]) - sqlalchemy DB session,
                if None - new session will be opened.

        Returns:
            List[DeclarativeMeta] - not serialized list of objects.
        """

        query: Select = select(self.model)
        if filters:
            query = query.filter_by(**filters)
        if in_filters:
            for field_name, list_of_items in in_filters.items():
                model_attr = getattr(self.model, field_name)
                query = query.filter(model_attr.in_(list_of_items))
        if pagination.limit is not None:
            query = query.limit(pagination.limit)
        if pagination.offset:
            query = query.offset(pagination.offset)

        # query is compiled, next making request with opened session
        async with db_session(existing_session=existing_session) as session:
            result = await self._execute_get_many(
                query=query, session=session
            )
            if not existing_session:
                # not commit existing session.
                await session.commit()

        return result

    async def get_many(
        self,
        filters: Dict[str, Any] = {},
        in_filters: Dict[str, List] = {},
        pagination: Pagination = Pagination(),
        existing_session: Optional[AsyncSession] = None,
    ) -> List[DeclarativeMeta]:
        """
        Filters database entries to fetch collection.
        Base repository keeps its own paginations while querying db.
        Example: if repo user asked for 20000 items, but we dont want
        to fetch that many from db at a time, repo will do it with
        smaller batches and respond 20000 items (if exist).

        Args:
            filters: Standard filters like {some_field: some_Value}
            pagination: Store pagination params, like offset/limit
            existing_session: Can be used for some external transaction.

        Examples:
            >>> await self.get_many(
                filters={"name": "abc"},
                pagination=Pagination(offset=0, limit=5000)
            )
            [ < Model (some_data) >, ..., < Model (some_data) >]

        Returns:
            type List[DeclarativeMeta] - collection of elements.
        """

        resulting_list: List[DeclarativeMeta] = []
        offset = pagination.offset
        limit = (
            pagination.limit
            if pagination.limit and pagination.limit < self.max_page_size
            else self.max_page_size
        )

        if not pagination.limit or limit < pagination.limit:
            logger.info(
                "Additional pagination to query db will be applied. "
                f"Given {pagination.limit=}, max limit = {self.max_page_size}"
            )

        while True:
            result = await self._get_many_limited_pagination(
                filters=filters,
                pagination=Pagination(offset=offset, limit=limit),
                in_filters=in_filters,
                existing_session=existing_session
            )
            resulting_list.extend(result)

            if len(result) < limit:
                break

            elif (
                pagination.limit and
                limit + offset >= pagination.offset + pagination.limit
            ):
                break
            offset += limit

        return resulting_list

    async def get_one(
        self,
        filters: Dict[str, Any],
        existing_session: Optional[AsyncSession] = None,
    ) -> DeclarativeMeta:
        """
        Fetches single record from DB.
        Ensures if filters are valid for fetching only 1 record.

        Args:
            filters (Dict[str, Any]): simple filters for query compiling.
            existing_session (Optional[AsyncSession], optional): opened
                sqlalchemy session. Defaults to None.

        Raises:
            GotMultipleObjectsError: got many records according given filters.
            ObjectNotFoundError: object not found.

        Returns:
            DeclarativeMeta: single not serialized object.
        """

        many_items = await self.get_many(
            filters=filters,
            existing_session=existing_session,
            pagination=Pagination(limit=2)
        )
        if len(many_items) > 1:
            raise GotMultipleObjectsError()
        elif len(many_items) == 0:
            raise ObjectNotFoundError(
                fields_names=list(filters.keys()),
                fields_values=list(filters.values())
            )
        return many_items[0]

    async def _execute_delete_one(
        self,
        filters: Dict[str, Any],
        session: AsyncSession
    ):
        """
        Fetches 1 object from db according filters and deletes it.
        """

        obj_in_db = await self.get_one(
            filters=filters, existing_session=session
        )
        await session.delete(obj_in_db)

    async def delete_one(
        self,
        filters: Dict[str, Any],
        existing_session: Optional[AsyncSession] = None,
    ) -> None:
        """
        Deletes one object from db, ensures object exists,
        optionally uses existing session.

        Args:
            filters (Dict[str, Any]): simple filters for query compiling.
            existing_session (Optional[AsyncSession], optional): opened
                sqlalchemy session. Defaults to None.
        """

        query = delete(self.model)
        if filters:
            query = query.filter_by(**filters)

        async with db_session(existing_session=existing_session) as session:
            await self._execute_delete_one(
                filters=filters, session=session
            )
            if not existing_session:
                await session.commit()

    async def update_one(
        self,
        filters: Dict[str, Any],
        data_to_update: Dict[str, Any],
        existing_session: Optional[AsyncSession] = None,
    ) -> DeclarativeMeta:
        """
        Updates filtered record with given data.
        Filters using existing method <filter_one>.
        Just does a job, no validation,
        so make validation before calling this method.
        Returns updated model.

        Args:
            filters (Dict[str, Any]): simple filters for query compiling.
            data_to_update (Dict[str, Any]): data (fields) to replace.
            existing_session (Optional[AsyncSession], optional): opened
                sqlalchemy session. Defaults to None.

        Returns:
            DeclarativeMeta: updated object.
        """

        model_to_update = await self.get_one(
            existing_session=existing_session,
            filters=filters
        )
        async with db_session(existing_session=existing_session) as session:
            for key, val in data_to_update.items():
                setattr(model_to_update, key, val)
            session.add(model_to_update)
            await session.commit()

        return model_to_update
