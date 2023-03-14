from pydantic import Field, PositiveInt

from openapi.core.schemas import ImprovedBaseModel
from openapi.modules.designations.docs.designations import \
    designation_scheme_docs as ds_docs
from openapi.modules.designations.settings import DesignationsSettings


class DesignationBase(ImprovedBaseModel):
    """
    The basic scheme for creating a range definition.
    """

    range_definition: str = Field(
        title=ds_docs["range_definition"]["title"],
        description=ds_docs["range_definition"]["description"],
        example=ds_docs["range_definition"]["example"],
        max_length=DesignationsSettings.max_range_definition_length,
        min_length=DesignationsSettings.min_range_definition_length
    )


class Designation(DesignationBase):
    """
    Complete scheme for Designation object (player's range definition).
    Usually used as a server response for the object "designation".
    """

    id: str = Field(
        title=ds_docs["id"]["title"],
        description=ds_docs["id"]["description"],
        example=ds_docs["id"]["example"],
    )
    range_length: PositiveInt = Field(
        title=ds_docs["range_length"]["title"],
        description=ds_docs["range_length"]["description"],
        example=ds_docs["range_length"]["example"],
    )

    class Config:
        """
        This class adds more flexibility for basic pydantic model.
        """

        orm_mode = True
        allow_population_by_field_name = True
