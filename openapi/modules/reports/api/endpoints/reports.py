"""
    All current app endpoints will be added to the router here.
"""
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, status, Path, Query
from openapi.core.exceptions_handlers import ReplaceExceptions
from openapi.core.schemas import HTTPExceptionModel, Pagination
from openapi.modules.auth.api.dependencies import verify_api_key
from openapi.modules.reports.api.dependencies import (
    get_reports_handler
)
from openapi.modules.ranges.repo_manager import RepositoriesManager
from openapi.modules.ranges.repositories.ranges import (
    RangesRepo)
from openapi.modules.ranges.schemas.ranges import (
    WeightedRange, WeightedRangeBase)
# from openapi.modules.ranges.settings import rangesSettings
from openapi.modules.ranges.docs.ranges import (
    range_scheme_docs as r_docs
)
from openapi.modules.designations.docs.designations import (
    designation_scheme_docs as ds_docs
)
from pydantic import confloat, PositiveInt
from loguru import logger
from pydantic.error_wrappers import ValidationError as PydValidationError
from openapi.modules.reports.report_handler import EquityReportsHandler

from openapi.modules.reports.schemas.reports import EquityReport, ReportsPostBody


router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)


@router.post(
    '/equity_report',
    responses={
        401: {"model": HTTPExceptionModel},
        403: {"model": HTTPExceptionModel},
        406: {"model": HTTPExceptionModel},
        422: {"model": HTTPExceptionModel},
        500: {"model": HTTPExceptionModel},
    },
    response_model=EquityReport,
    status_code=status.HTTP_200_OK
)
async def create_equity_report(
    data: ReportsPostBody,
    handler: EquityReportsHandler = Depends(get_reports_handler)
):
    """
    This endpoint used to calculate equity of a hero's
    range against opponent's range.
    """

    logger.info(
        "Got request create_equity_report using api-key. "
        f"{data=}"
    )

    return await handler.create_equity_report(data=data)
