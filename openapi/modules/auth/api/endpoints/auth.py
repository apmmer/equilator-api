from typing import Dict

from fastapi import APIRouter, Depends, status
from keycloak import KeycloakOpenID
from loguru import logger

from openapi.core.exceptions import DefaultException
from openapi.core.schemas import HTTPExceptionModel
from openapi.modules.auth.api.dependencies import verify_api_key
from openapi.modules.auth.schemas.user_creadentials import UserCredentials
from openapi.modules.auth.settings import AuthSettings

router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)


# @router.post(
#     '/access_token',
#     responses={
#         401: {"model": HTTPExceptionModel},
#         403: {"model": HTTPExceptionModel},
#         422: {"model": HTTPExceptionModel},
#         500: {"model": HTTPExceptionModel},
#     },
#     response_model=Dict,
#     status_code=status.HTTP_200_OK)
# async def get_token(
#     body: UserCredentials,
# ):
#     """
#         Endpoint for developers, to get token using api.
#         This endpoint (and whole application) should be removed
#         before production stage.
#     """

#     logger.info(
#         'Got request to retrieve keycloak access token.'
#     )

#     try:
#         keycloak_openid = KeycloakOpenID(
#             server_url=AuthSettings.server_url,
#             client_id=AuthSettings.client_id,
#             realm_name=AuthSettings.realm_name,
#             client_secret_key=AuthSettings.client_secret_key,
#         )
#         token = keycloak_openid.token(
#             body.username, body.password)
#     except Exception as ex:
#         logger.error(f'Msg: {ex}')
#         raise DefaultException()
#     return token
