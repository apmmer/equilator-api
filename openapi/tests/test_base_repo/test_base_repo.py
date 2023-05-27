import inspect
from typing import Dict, List

import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from openapi.core.base_repository import BaseRepository
from openapi.core.exceptions import (DefaultException, GotMultipleObjectsError,
                                     ObjectNotFoundError, SQLException)
from openapi.tests.conftest import BaseTest
from openapi.tests.test_base_repo.conftest import BaseRepoTests


class TestCaseBaseRepository(BaseRepoTests):
    # test base repository with different models

    # BaseRepository.add_one(...) tests
    def test_add_one_method_exists(self):
        assert BaseRepository.__dict__.get("add_one", None)

    def test_add_one_is_coroutine(self):
        method = BaseRepository.__dict__.get("add_one", None)
        assert inspect.iscoroutinefunction(method)

    async def test_add_one_adds_an_item(
        self,
        db_session: AsyncSession,
        item_case_fixt: Dict
    ):
        repo = BaseRepository(model=item_case_fixt["model"])
        data = item_case_fixt["data"]
        filters_field_name = item_case_fixt["filter_field"]
        filters_value = data[filters_field_name]
        filters = {filters_field_name: filters_value}

        repo_res = await repo.add_one(
            data=data,
            existing_session=db_session
        )
        await db_session.commit()
        assert True

        db_res = await self.fetch_one_item(
            model=item_case_fixt["model"],
            filters=filters,
            session=db_session
        )
        assert db_res.id == repo_res.id
        await db_session.commit()

    # BaseRepository.get_many(...) tests
    def test_get_many_method_exists(self):
        assert BaseRepository.__dict__.get("get_many", None)

    def test_get_many_is_coroutine(self):
        method = BaseRepository.__dict__.get("get_many", None)
        assert inspect.iscoroutinefunction(method)

    async def test_get_many_returns_list_of_items(
        self,
        db_session: AsyncSession,
        get_items_case_fixt: List[Dict]
    ):
        for item in get_items_case_fixt:
            await self.prepare_item_in_db(
                model=item["model"],
                session=db_session,
                data=item["data"]
            )
        assert type(get_items_case_fixt) == list
        assert len(get_items_case_fixt) == 2
        repo = BaseRepository(model=get_items_case_fixt[0]["model"])
        res = await repo.get_many(existing_session=db_session)
        await db_session.commit()
        assert isinstance(res, list)
        assert len(res) == len(get_items_case_fixt)

    async def test_get_many_returns_correct_items(
        self,
        db_session: AsyncSession,
        get_items_case_fixt: List[Dict]
    ):
        for item in get_items_case_fixt:
            await self.prepare_item_in_db(
                model=item["model"],
                session=db_session,
                data=item["data"]
            )
        repo = BaseRepository(model=get_items_case_fixt[0]["model"])
        res = await repo.get_many(existing_session=db_session)
        await db_session.commit()
        for i, item in enumerate(get_items_case_fixt):
            db_res_fieldvalue = getattr(res[i], item["filter_field"])
            test_fieldvalue = item["data"][item["filter_field"]]
            assert db_res_fieldvalue == test_fieldvalue

    async def test_get_many_returns_empty_list_if_no_items(
        self,
        db_session: AsyncSession,
        item_case_fixt: Dict
    ):
        repo = BaseRepository(model=item_case_fixt["model"])
        res = await repo.get_many(
            existing_session=db_session,
            filters={item_case_fixt["filter_field"]: "invalid_filter"}
        )
        await db_session.commit()
        assert res == []

    # BaseRepository.get_one(...) tests
    def test_get_one_method_exists(self):
        assert BaseRepository.__dict__.get("get_one", None)

    def test_get_one_is_coroutine(self):
        method = BaseRepository.__dict__.get("get_one", None)
        assert inspect.iscoroutinefunction(method)

    async def test_get_one_returns_correct_item(
        self,
        db_session: AsyncSession,
        item_case_fixt: Dict
    ):
        data = item_case_fixt["data"]
        filters_field_name = item_case_fixt["filter_field"]
        filters_value = data[filters_field_name]
        filters = {filters_field_name: filters_value}

        await self.prepare_item_in_db(
            model=item_case_fixt["model"],
            session=db_session,
            data=data
        )
        repo = BaseRepository(model=item_case_fixt["model"])
        res = await repo.get_one(filters=filters)
        assert res

    async def test_get_one_raises_correct_exception_if_not_found(
        self,
        item_case_fixt: Dict
    ):
        async def fake_get_many(*args, **kwargs):
            return []

        repo = BaseRepository(model=item_case_fixt["model"])
        repo.get_many = fake_get_many

        with pytest.raises(ObjectNotFoundError):
            await repo.get_one(filters={})

    async def test_get_one_raises_correct_exception_if_found_many(
        self,
        item_case_fixt: Dict
    ):
        async def fake_get_many(*args, **kwargs):
            return [1, 2, 3]

        repo = BaseRepository(model=item_case_fixt["model"])
        repo.get_many = fake_get_many

        with pytest.raises(GotMultipleObjectsError):
            await repo.get_one(filters={})

    # BaseRepository.delete_one(...) tests
    def test_delete_one_method_exists(self):
        assert BaseRepository.__dict__.get("delete_one", None)

    def test_delete_one_is_coroutine(self):
        method = BaseRepository.__dict__.get("get_one", None)
        assert inspect.iscoroutinefunction(method)

    async def test_delete_one_really_deletes_an_item(
        self,
        db_session: AsyncSession,
        item_case_fixt: Dict
    ):
        # ensure item is in db
        data = item_case_fixt["data"]
        filters_field_name = item_case_fixt["filter_field"]
        filters_value = data[filters_field_name]
        filters = {filters_field_name: filters_value}
        await self.prepare_item_in_db(
            model=item_case_fixt["model"],
            session=db_session,
            data=data
        )

        # make repo and call delete method
        repo = BaseRepository(model=item_case_fixt["model"])
        res = await repo.delete_one(
            existing_session=db_session,
            filters=filters
        )
        await db_session.commit()
        assert res is None

        # ensure item is not in db
        with pytest.raises(IndexError):
            await self.fetch_one_item(
                model=item_case_fixt["model"],
                filters=filters,
                session=db_session
            )

    # BaseRepository.update_one(...) tests
    def test_update_one_method_exists(self):
        assert BaseRepository.__dict__.get("update_one", None)

    def test_update_one_is_coroutine(self):
        method = BaseRepository.__dict__.get("update_one", None)
        assert inspect.iscoroutinefunction(method)

    async def test_update_one_returns_correct_results(
        self,
        db_session: AsyncSession,
        item_case_fixt: Dict
    ):
        data = item_case_fixt["data"]
        filters_field_name = item_case_fixt["filter_field"]
        filters_value = data[filters_field_name]
        filters = {filters_field_name: filters_value}
        await self.prepare_item_in_db(
            model=item_case_fixt["model"],
            session=db_session,
            data=data
        )

        repo = BaseRepository(model=item_case_fixt["model"])
        data_to_update = item_case_fixt["update_fields"]
        res = await repo.update_one(
            existing_session=db_session,
            filters=filters,
            data_to_update=data_to_update
        )
        await db_session.commit()
        for field_name in data_to_update.keys():
            assert getattr(res, field_name) == data_to_update[field_name]

    async def test_update_one_really_updates_an_item(
        self,
        db_session: AsyncSession,
        item_case_fixt: Dict
    ):
        data = item_case_fixt["data"]
        filters_field_name = item_case_fixt["filter_field"]
        filters_value = data[filters_field_name]
        filters = {filters_field_name: filters_value}
        await self.prepare_item_in_db(
            model=item_case_fixt["model"],
            session=db_session,
            data=data
        )

        repo = BaseRepository(model=item_case_fixt["model"])
        data_to_update = item_case_fixt["update_fields"]
        await repo.update_one(
            existing_session=db_session,
            filters=filters,
            data_to_update=data_to_update
        )
        await db_session.commit()

        db_res = await self.fetch_one_item(
            model=item_case_fixt["model"],
            filters=filters,
            session=db_session
        )
        for field_name in data_to_update.keys():
            assert getattr(db_res, field_name) == data_to_update[field_name]

    # BaseRepository._handle_integrity_error(...) tests
    def test__handle_integrity_error_raises_fastapi_exception(
        self,
        item_case_fixt: Dict
    ):
        # just for tests as mock, do not repeat in prod :)
        class FakeIntegrityError:
            class orig:
                class __context__:
                    detail = "test"

        repo = BaseRepository(model=item_case_fixt["model"])
        with pytest.raises(DefaultException):
            repo._handle_integrity_error(
                exception=FakeIntegrityError()
            )

    def test__handle_integrity_error_raises_error_with_detail(
        self,
        item_case_fixt: Dict
    ):
        # just for tests as mock, do not repeat in prod :)
        class FakeIntegrityError:
            class orig:
                class __context__:
                    # there is a condition inside a code
                    detail = "test 'already exists'"

        repo = BaseRepository(model=item_case_fixt["model"])
        with pytest.raises(SQLException):
            repo._handle_integrity_error(
                exception=FakeIntegrityError()
            )
