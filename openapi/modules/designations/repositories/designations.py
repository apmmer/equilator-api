import hashlib
from typing import Dict, List, Optional

from pydantic import parse_obj_as
from sqlalchemy.orm.decl_api import DeclarativeMeta

from openapi.core.base_repository import BaseRepository
from openapi.core.db.models import DesignationModel
from openapi.core.exceptions import DefaultException
from openapi.core.exceptions_handlers import ReplaceExceptions
from openapi.core.schemas import Pagination
from openapi.modules.designations.schemas.designations import (Designation,
                                                               DesignationBase)
from openapi.modules.equilator.range_converter import convert_from_string


class DesignationsRepo(BaseRepository):
    """
    A class where logic of operations with designations is presented.
    This class can contain: business logic, validation, exceptions handling.
    """

    def __init__(
        self,
        model: Optional[DeclarativeMeta] = DesignationModel,
        *base_repo_args,
        **base_repo_kwargs
    ):
        super().__init__(model=model, *base_repo_args, **base_repo_kwargs)

    async def add_an_item(
        self,
        data: Dict,
        **base_repo_kwargs
    ) -> Designation:
        """
        Validates input data, compiles a new object,
        adds new record to db using BaseRepo method and
        finally validates returning value.

        Args:
            data (Dict): necessary data for designation creation

        Returns:
            Designation: validated pydantic model with necessary fields.
        """

        valid_data = DesignationBase.parse_obj(data).dict()
        resulting_range: list[str] = convert_from_string(
            user_input=valid_data["range_definition"]
        )

        hashed = hashlib.sha256(
            str(resulting_range).encode(encoding="UTF-8", errors="strict")
        ).hexdigest()

        valid_data["id"] = hashed
        valid_data["range_length"] = len(resulting_range)
        try:
            model = await self.add_one(
                data=valid_data,
                **base_repo_kwargs
            )
        except DefaultException as ex:
            if "already exists" in ex.detail:
                ex.detail = f"This range already exists, it's ID = ({hashed})"
            raise ex
        return Designation.from_orm(model)

    async def get_collection(
        self,
        pagination: Pagination = Pagination()
    ) -> List[Designation]:
        """
        Fetches multiple objects from db and returns a collection of
        pydantic models's instances.

        Args:
            pagination (Pagination, optional): pagination scheme instance.
                Defaults to Pagination().

        Returns:
            List[Designation]: a collection of items.
        """

        records = await self.get_many(
            filters={},
            pagination=pagination,
        )
        validated_result = parse_obj_as(List[Designation], records)
        return validated_result

    async def delete_an_item(self, id: str):
        """
        Deletes a single item from db, if exists.

        Args:
            id (str): unique identificator of an item,
                field "id" in model.
        """

        await self.delete_one(
            filters={"id": id}
        )

    @ReplaceExceptions()
    async def get_an_item(self, id: str) -> Designation:
        """
        Fetches an item with provided id.

        Args:
            id (str): unique identificator of an item,
                field "id" in model.

        Returns:
            Designation: single object, validated by pydantic.
        """

        db_item = await self.get_one(filters={"id": id})
        return Designation.from_orm(db_item)
