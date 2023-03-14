"""
All current module endpoints will be added to the router here.
"""

from fastapi import APIRouter, Depends, status
from loguru import logger

from openapi.core.schemas import HTTPExceptionModel
from openapi.modules.auth.dependencies import verify_api_key

from openapi.modules.reports.api.dependencies import get_reports_handler
from openapi.modules.reports.report_handler import EquityReportsHandler
from openapi.modules.reports.schemas.reports import (EquityReport,
                                                     ReportsPostBody)

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
