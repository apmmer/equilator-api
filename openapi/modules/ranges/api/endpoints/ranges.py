"""
All current app endpoints will be added to the router here.
"""

from typing import Dict, List
from fastapi import APIRouter, Depends, status, Path, Query
from openapi.core.schemas import HTTPExceptionModel, Pagination
from openapi.modules.auth.dependencies import verify_api_key
from openapi.modules.ranges.api.dependencies import (
    get_ranges_repo,
    get_repo_manager
)
from openapi.modules.ranges.repo_manager import RepositoriesManager
from openapi.modules.ranges.repositories.ranges import (
    RangesRepo)
from openapi.modules.ranges.schemas.ranges import (
    WeightedRange, WeightedRangeBase)
from openapi.modules.ranges.docs.ranges import (
    range_scheme_docs as r_docs
)
from openapi.modules.designations.docs.designations import (
    designation_scheme_docs as ds_docs
)
from pydantic import confloat, PositiveInt
from loguru import logger

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
    response_model=WeightedRange,
    status_code=status.HTTP_201_CREATED,
    openapi_extra=WeightedRangeBase.get_request_body_docs(
        docs=r_docs
    )
)
async def add_weighted_range(
    body: Dict,
    repo: RangesRepo = Depends(get_ranges_repo)
):
    """
    Saves the user's weighted hands range to the database.\n
    Returns successfully created object
    or error-response 400+ with detailed description.\n
    Authentication is required.\n
    """

    logger.info(
        "Got request add_weighted_range using api-key. "
        f"{body=}"
    )

    item = await repo.add_an_item(data=body)
    return item


@router.post(
    '/from_designation',
    responses={
        401: {"model": HTTPExceptionModel},
        403: {"model": HTTPExceptionModel},
        404: {"model": HTTPExceptionModel},
        409: {"model": HTTPExceptionModel},
        422: {"model": HTTPExceptionModel},
        500: {"model": HTTPExceptionModel},
    },
    response_model=WeightedRange,
    status_code=status.HTTP_201_CREATED
)
async def add_weighted_range_using_designation(
    name: str = Query(
        ...,
        title=r_docs["name"]["title"],
        description=r_docs["name"]["description"],
        example=r_docs["name"]["example"],
    ),
    designation_id: str = Query(
        ...,
        title=ds_docs["id"]["title"],
        description=ds_docs["id"]["description"],
        example=ds_docs["id"]["example"],
    ),
    default_weight: confloat(ge=0, le=1) = Query(
        ...,
        title="Default weight",
        description=(
            "This weight will be applied for all "
            "hands in given range designation."
        ),
        example=0.5,
    ),
    repo_manager: RepositoriesManager = Depends(get_repo_manager)
):
    """
    Saves the user's weighted hands range to the database.\n
    Returns successfully created object
    or error-response 400+ with detailed description.\n
    Authentication is required.\n
    """

    logger.info(
        "Got request add_weighted_range using api-key. "
        f"{designation_id=} {default_weight=}"
    )

    item = await repo_manager.add_range_using_designation(
        name=name,
        designation_id=designation_id,
        default_weight=default_weight
    )
    return item


@router.get(
    '',
    responses={
        401: {"model": HTTPExceptionModel},
        403: {"model": HTTPExceptionModel},
        422: {"model": HTTPExceptionModel},
        500: {"model": HTTPExceptionModel},
    },
    response_model=List[WeightedRange],
    status_code=status.HTTP_200_OK,
)
async def get_weighted_ranges_collection(
    pagination: Pagination = Depends(),
    repo: RangesRepo = Depends(get_ranges_repo)
):
    """
    Returns a list of weighted ranges.\n
    Authentication is required.
    """

    logger.info(
        "Got request get_ranges_collection using api-key. "
        f"{pagination=}"
    )

    items = await repo.get_collection(pagination=pagination)
    return items


@router.delete(
    '/{weighted_range_id}',
    responses={
        401: {"model": HTTPExceptionModel},
        403: {"model": HTTPExceptionModel},
        422: {"model": HTTPExceptionModel},
        500: {"model": HTTPExceptionModel},
    },
    response_model=Dict,
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_weighted_range_by_id(
    weighted_range_id: PositiveInt = Path(
        title=r_docs["id"]["title"],
        description=r_docs["id"]["description"],
        example=r_docs["id"]["example"],
    ),
    repo: RangesRepo = Depends(get_ranges_repo)
):
    """
    Deletes weighted range object with given ID.\n
    Authentication is required.
    """

    logger.info(
        "Got request delete_weighted_range_by_id using api-key. "
        f"{weighted_range_id=}"
    )

    await repo.delete_an_item(item_id=weighted_range_id)
    return {"accepted deletion of object with id": weighted_range_id}


@router.get(
    '/{weighted_range_id}',
    responses={
        401: {"model": HTTPExceptionModel},
        403: {"model": HTTPExceptionModel},
        422: {"model": HTTPExceptionModel},
        500: {"model": HTTPExceptionModel},
    },
    response_model=WeightedRange,
    status_code=status.HTTP_200_OK,
)
async def get_weighted_range_by_id(
    weighted_range_id: PositiveInt = Path(
        title=r_docs["id"]["title"],
        description=r_docs["id"]["description"],
        example=r_docs["id"]["example"],
    ),
    repo: RangesRepo = Depends(get_ranges_repo)
):
    """
    Returns a player's range with given id if exists.\n
    Authentication is required.
    """

    logger.info(
        "Got request get_weighted_range_by_id using api-key. "
        f"{weighted_range_id=}"
    )

    result = await repo.get_an_item(item_id=weighted_range_id)
    return result


@router.patch(
    '/{weighted_range_id}',
    responses={
        401: {"model": HTTPExceptionModel},
        403: {"model": HTTPExceptionModel},
        422: {"model": HTTPExceptionModel},
        500: {"model": HTTPExceptionModel},
    },
    response_model=WeightedRange,
    status_code=status.HTTP_200_OK,
    openapi_extra=WeightedRangeBase.get_request_body_docs(
        docs=r_docs
    )
)
async def update_weighted_range_by_id(
    body: Dict,
    weighted_range_id: PositiveInt = Path(
        title=r_docs["id"]["title"],
        description=r_docs["id"]["description"],
        example=r_docs["id"]["example"],
    ),
    repo: RangesRepo = Depends(get_ranges_repo)
):
    """
    Returns a player's range with given name is exists.\n
    Authentication is required.
    """

    logger.info(
        "Got request update_weighted_range_by_id using api-key. "
        f"{weighted_range_id=}"
    )

    result = await repo.update_an_item(
        item_id=weighted_range_id,
        data=body
    )
    return result
