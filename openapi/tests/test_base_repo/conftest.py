from openapi.core.db.models import DesignationModel, WeightedRangeModel
from pytest import fixture
from typing import Dict, List
from sqlalchemy import select
from openapi.core.db.db_session import db_session
from sqlalchemy.orm.decl_api import DeclarativeMeta


items_cases = [
    {
        # model of an item
        "model": DesignationModel,
        # data for item creation
        "data": {
            "id": "test",
            "range_length": 6,
            "range_definition": "AA+"
        },
        # data to filter item by uniq field
        "filter_field": "id",
        # data to update some fields with new values
        "update_fields": {
            "range_definition": "KK+",
            "range_length": 12
        }
    },
    {
        "model": DesignationModel,
        "data": {
            "id": "test2",
            "range_length": 12,
            "range_definition": "KK+"
        },
        "filter_field": "id",
        "update_fields": {
            "range_definition": "QQ+",
            "range_length": 18
        }
    },
    {
        "model": WeightedRangeModel,
        "data": {
            "name": "test",
            "hash": "test",
            "definition": {"AhAd": 0.5}
        },
        "filter_field": "hash",
        "update_fields": {
            "definition": {"AhAd": 0.1}
        }
    },
    {
        "model": WeightedRangeModel,
        "data": {
            "name": "test2",
            "hash": "test2",
            "definition": {"AhAd": 0.5, "KcKs": 0.1}
        },
        "filter_field": "hash",
        "update_fields": {
            "definition": {"AhAd": 0.9, "KcKs": 0.6}
        }
    }
]


class BaseRepoTestsMixin:
    @fixture(params=items_cases)
    async def item_case_fixt(self, request) -> Dict:
        return request.param

    @fixture(params=[
        [items_cases[0], items_cases[1]],
        [items_cases[2], items_cases[3]],
    ])
    async def get_items_case_fixt(self, request) -> Dict:
        return request.param

    async def prepare_item_in_db(self, model, data, session):
        new_model: DeclarativeMeta = model(**data)
        async with db_session(existing_session=session) as session:
            session.add(new_model)
            await session.commit()

    async def fetch_one_item(self, model, filters, session) -> DeclarativeMeta:
        query = select(model).filter_by(**filters)
        async with db_session(existing_session=session) as session:
            result: List[DeclarativeMeta] = (
                await session.execute(query)
            ).scalars().unique().all()
            await session.commit()
        return result[0]
