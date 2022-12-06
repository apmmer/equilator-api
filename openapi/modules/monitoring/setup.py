from types import ModuleType
from typing import List

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from openapi.core.settings import OpenapiSettings
from openapi.modules.monitoring.settings import SentrySettings


def setup_sentry(
    sentry_sdk: ModuleType = sentry_sdk,
    dsn: str = SentrySettings.sentry_dsn,
    integrations: List = [
        StarletteIntegration(
            transaction_style=SentrySettings.sentry_transaction_style),
        FastApiIntegration(
            transaction_style=SentrySettings.sentry_transaction_style),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate: float = SentrySettings.sentry_traces_sample_rate,
    server_type: str = SentrySettings.server_type,
    version: str = OpenapiSettings.version,
    title: str = OpenapiSettings.title,
    is_send_default_pii: bool = True,
):
    """
    Calls sentry_sdk's init method, which will include Sentry
    wrapping for fastapi.
    This function should be called in main app before declaring FastAPI()
    """

    sentry_sdk.init(
        dsn=dsn,
        integrations=integrations,
        traces_sample_rate=traces_sample_rate,
        release=f"{title}@{version}",
        environment=server_type,
        send_default_pii=is_send_default_pii,
    )
