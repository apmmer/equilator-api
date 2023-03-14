"""
All current module endpoints will be added to the router here.
"""

from typing import Dict, List

from fastapi import APIRouter, Depends, Path, status
from loguru import logger

from openapi.core.schemas import HTTPExceptionModel, Pagination
from openapi.modules.auth.dependencies import verify_api_key
from openapi.modules.designations.api.dependencies import get_designations_repo
from openapi.modules.designations.docs.designations import \
    designation_scheme_docs as ds_docs
from openapi.modules.designations.repositories.designations import \
    DesignationsRepo
from openapi.modules.designations.schemas.designations import (Designation,
                                                               DesignationBase)

router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)


@router.post(
    '',
    responses={
        401: {"model": HTTPExceptionModel},
        403: {"model": HTTPExceptionModel},
        409: {"model": HTTPExceptionModel},
        422: {"model": HTTPExceptionModel},
        500: {"model": HTTPExceptionModel},
    },
    response_model=Designation,
    status_code=status.HTTP_201_CREATED,
    openapi_extra=DesignationBase.get_request_body_docs(
        docs=ds_docs
    )
)
async def add_designation(
    body: Dict,
    repo: DesignationsRepo = Depends(get_designations_repo)
):
    """
    Saves the user's hands range to the database.\n
    Returns successfully created object
    or error-response 400+ with detailed description.\n
    Authentication is required.\n
    Cards ranking in Texas Holdem:\n
        A > K > Q > J > T > 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2\n
    Input syntax for range_definition:\n
        "2h2d" - single combo of a pocket pair (1 combo)
        "22" - single pocket pair (including all suits:  6 combos)
            Correct inputs: "33", "JJ", "AA"
        "22+" - all pocket pairs combos from AA to 22 (78 combos)
        "88-22" - all pocket pairs between 88 and 22 (42 combos)
            Note: higher pocket should be first, "22-88" - is wrong input
        "AhJd" - Single ofsuited combo. (1 combo)
            Note: the highest rank can be written second, "JdAh" is valid,
                but it will be replaced to AhJd automatically.
        "AJo" - All combos of offsuited AJ (AhJd, AhJc...AsJc: 12 combos)
            Note: higher rank should be first, "QAo" - is wrong input
        "AJo+" - all offsuited Ace-high hands with kickers from J to K,
            (AJo, AQo, AKo: 36 combos)
            Note: higher rank should be first, "QAo+" - is wrong input
            Correct inputs: "A2o+" (144 combos), "K3o+" (120 combos),
                "75o+" (24 combos), "87o+" (12 combos)
        "A5o-A2o" - all offsuited Ace-high hands with kickers from 5 to 2,
            (A2o, A3o, A4o, A5o: 48 combos)
            Note: higher kicker rank should be first, "A2o-A5o" - is wrong
            Correct inputs: "A7o-A5o" (36 combos), "KJo-KTo" (24 combos)
        "AhTh" - Single suited combo. (1 combo)
            Note: the highest rank can be written second, "ThAh" is valid,
                but it will be replaced to AhTh automatically.
        "ATs+" - all suited Ace-high hands with kickers from T to K,
            (ATs, AJs, AQs, AKs: 16 combos)
            Note: higher rank should be first, "TAs+" - is wrong input
            Correct inputs: "A3s+" (44 combos), "K4s+" (36 combos)
        "A5s-A2s" - all suited Ace-high hands with kickers from 5 to 2,
            (A2s, A3s, A4s, A5s: 16 combos)
            Note: higher kicker rank should be first, "A2s-A5s" - is wrong
            Correct inputs: "A7s-A5s" (12 combos), "KJs-KTs" (8 combos)
        "all" - all 1326 combos. Also valid: "any2", "any two", "anytwo"
        "suited" - all suited hands (312 combos)
        "offsuited" - all offsuited hands (936 combos)
        "pockets" - all pocket pairs (the same as 22+)

    Correct examples:\n
        "QQ+,AKs" - 16 combos.
        "TT+,AQs+,AKo" - 50 combos.
        "88+,ATs+,AQo+,KQs,QJs" - 90 combos.
        "55+,AKo" - 72 combos
        "8h8d,7d7s,2h2d,AJo+,55-44,AA-KK" - 63 combos.
    """

    logger.info(
        "Got request add_designation using api-key. "
        f"{body=}"
    )

    item = await repo.add_an_item(data=body)
    return item


@router.get(
    '',
    responses={
        401: {"model": HTTPExceptionModel},
        403: {"model": HTTPExceptionModel},
        422: {"model": HTTPExceptionModel},
        500: {"model": HTTPExceptionModel},
    },
    response_model=List[Designation],
    status_code=status.HTTP_200_OK,
)
async def get_designations_collection(
    pagination: Pagination = Depends(),
    repo: DesignationsRepo = Depends(get_designations_repo)
):
    """
    Returns a list of unique designations.\n
    Authentication is required.
    """

    logger.info(
        "Got request get_designations_collection using api-key. "
        f"{pagination=}"
    )

    items = await repo.get_collection(pagination=pagination)
    return items


@router.delete(
    '/{designation_id}',
    responses={
        401: {"model": HTTPExceptionModel},
        403: {"model": HTTPExceptionModel},
        422: {"model": HTTPExceptionModel},
        500: {"model": HTTPExceptionModel},
    },
    response_model=Dict,
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_designation_by_id(
    designation_id: str = Path(
        title=ds_docs["id"]["title"],
        description=ds_docs["id"]["description"],
        example=ds_docs["id"]["example"],
    ),
    repo: DesignationsRepo = Depends(get_designations_repo)
):
    """
    Deletes designation object with given ID.\n
    Authentication is required.
    """

    logger.info(
        "Got request delete_designation_by_id using api-key. "
        f"{designation_id=}"
    )

    await repo.delete_an_item(id=designation_id)
    return {"accepted deletion of id": designation_id}


@router.get(
    '/{designation_id}',
    responses={
        401: {"model": HTTPExceptionModel},
        403: {"model": HTTPExceptionModel},
        422: {"model": HTTPExceptionModel},
        500: {"model": HTTPExceptionModel},
    },
    response_model=Designation,
    status_code=status.HTTP_200_OK,
)
async def get_designation_by_id(
    designation_id: str = Path(
        title=ds_docs["id"]["title"],
        description=ds_docs["id"]["description"],
        example=ds_docs["id"]["example"],
    ),
    repo: DesignationsRepo = Depends(get_designations_repo)
):
    """
    Returns a designation with given ID is exists.\n
    Authentication is required.
    """

    logger.info(
        "Got request get_designation_by_id using api-key. "
        f"{designation_id=}"
    )

    result = await repo.get_an_item(id=designation_id)
    return result
