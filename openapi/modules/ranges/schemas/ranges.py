from typing import Dict, List, Optional
from pydantic import Field, confloat, constr, validator
from openapi.core.exceptions import PydanticValidationError
from openapi.core.schemas import ImprovedBaseModel
from openapi.modules.ranges.docs.ranges import (
    range_scheme_docs as r_docs
)


class WeightedRangeBase(ImprovedBaseModel):
    """
    The basic scheme for creating a range definition.
    """

    name: constr(
        min_length=1,
        max_length=500
    ) = Field(
        title=r_docs["name"]["title"],
        description=r_docs["name"]["description"],
        example=r_docs["name"]["example"],
    )

    definition: Dict[
        constr(min_length=4, max_length=4),
        confloat(gt=0, le=1)
    ] = Field(
        title=r_docs["definition"]["title"],
        description=r_docs["definition"]["description"],
        example=r_docs["definition"]["example"],
    )

    @validator("definition")
    def validate_definition_exists(cls, value):
        if value == {}:
            raise PydanticValidationError(
                "Definition can not be empty."
            )
        errors: List[str] = []
        for hand in value.keys():
            if hand[:2] == hand[2:]:
                errors.append(f"Hand ({hand}) contains two same cards.")
            if hand[0] not in "23456789TJQKA":
                errors.append(f"Hand ({hand}), first rank is not valid.")
            if hand[2] not in "23456789TJQKA":
                errors.append(f"Hand ({hand}), secord rank is not valid.")
            if hand[1] not in "hdcs":
                errors.append(f"Hand ({hand}), first suit is not valid.")
            if hand[3] not in "hdcs":
                errors.append(f"Hand ({hand}), second suit is not valid.")

        if errors:
            raise PydanticValidationError(
                detail=f"During validation next errors found: {errors}"
            )
        return value


class WeightedRange(WeightedRangeBase):
    id: int = Field(
        title=r_docs["id"]["title"],
        description=r_docs["id"]["description"],
        example=r_docs["id"]["example"],
    )
    hash: str = Field(
        title=r_docs["hash"]["title"],
        description=r_docs["hash"]["description"],
        example=r_docs["hash"]["example"],
    )

    class Config:
        """
        This class adds more flexibility for basic pydantic model.
        """

        orm_mode = True
        allow_population_by_field_name = True


class WeightedRangePatch(WeightedRangeBase):
    name: Optional[
        constr(
            min_length=1,
            max_length=500
        )
    ] = None

    definition: Optional[
        Dict[
            constr(min_length=4, max_length=4),
            confloat(gt=0, le=1)
        ]
    ] = None
