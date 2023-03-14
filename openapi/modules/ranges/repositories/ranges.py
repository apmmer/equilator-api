import hashlib
from typing import Any, Dict, List, Optional

from pydantic import parse_obj_as
from sqlalchemy.orm.decl_api import DeclarativeMeta

from openapi.core.base_repository import BaseRepository
from openapi.core.db.models import WeightedRangeModel
from openapi.core.exceptions import DefaultException
from openapi.core.exceptions_handlers import ReplaceExceptions
from openapi.core.schemas import Pagination
from openapi.modules.ranges.schemas.ranges import (WeightedRange,
                                                   WeightedRangeBase,
                                                   WeightedRangePatch)


class RangesRepo(BaseRepository):
    """
    A class where logic of operations with weighted ranges is presented.
    This class can contain: business logic, validation, exceptions handling.
    """

    def __init__(
        self,
        model: Optional[DeclarativeMeta] = WeightedRangeModel,
        *base_repo_args,
        **base_repo_kwargs,
    ):
        super().__init__(model=model, *base_repo_args, **base_repo_kwargs)

    @ReplaceExceptions()
    async def add_an_item(
        self,
        data: Dict,
        **base_repo_kwargs
    ) -> WeightedRange:
        """
        Validates input data, compiles a new object,
        adds new record to db using BaseRepo method and
        finally validates returning value.

        Args:
            data (Dict): necessary data for designation creation

        Returns:
            Designation: validated pydantic model with necessary fields.
        """

        valid_data = WeightedRangeBase.parse_obj(data).dict()

        valid_data["hash"] = self._get_range_definition_hash(
            definition=valid_data["definition"]
        )
        try:
            model = await self.add_one(
                data=valid_data,
                **base_repo_kwargs
            )
        except DefaultException as ex:
            if "already exists" in ex.detail:
                ex.detail = (
                    "Player's range with name "
                    f"('{valid_data['name']}') already exists."
                )
            raise ex
        return WeightedRange.from_orm(model)

    @ReplaceExceptions()
    async def get_collection(
        self,
        pagination: Pagination = Pagination()
    ) -> List[WeightedRange]:

        records = await self.get_many(
            filters={},
            pagination=pagination,
        )
        validated_result = parse_obj_as(List[WeightedRange], records)
        return validated_result

    @ReplaceExceptions()
    async def delete_an_item(self, item_id: str):
        await self.delete_one(filters={"id": item_id})

    @ReplaceExceptions()
    async def get_an_item(self, item_id: int) -> WeightedRange:
        db_item = await self.get_one(filters={"id": item_id})
        valid_item = WeightedRange.from_orm(db_item)
        return valid_item

    def _prepare_hashable(self, definition: Dict[str, float]) -> str:
        # sort at first
        sorted_definition = sorted(definition.items())
        # return string
        return str(sorted_definition)

    def _get_range_definition_hash(self, definition: Dict[str, float]):
        sorted_range_str: str = self._prepare_hashable(
            definition=definition)
        hashed = hashlib.sha256(
            sorted_range_str.encode(encoding='UTF-8', errors='strict')
        ).hexdigest()
        return hashed

    @ReplaceExceptions()
    async def update_an_item(
        self,
        item_id: int,
        data: Dict[str, Any]
    ) -> WeightedRange:
        validated_data = WeightedRangePatch(**data).dict()
        data_to_update = {}
        for key, val in validated_data.items():
            if val is not None:
                data_to_update[key] = val
        data_to_update["hash"] = self._get_range_definition_hash(
            definition=validated_data["definition"]
        )
        updated_model = await self.update_one(
            filters={"id": item_id},
            data_to_update=data_to_update
        )
        return WeightedRange.from_orm(updated_model)
