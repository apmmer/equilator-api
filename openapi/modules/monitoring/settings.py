"""
Specific module settings are located here.
"""

from os import getenv


class SentrySettings:
    server_type: str = getenv("SERVER_TYPE", "local")
    router_prefix: str = "/monitoring"
    router_tag: str = "Monitoring"

    # Sentry client settings
    sentry_transaction_style: str = "url"
    sentry_dsn: str = getenv("SENTRY_DSN", "https://<key>@sentry.io/<project>")

    # Set traces_sample_rate to 1.0 to capture
    # 100% of transactions for performance monitoring.
    sentry_traces_sample_rate: float = float(
        getenv("SENTRY_TRACES_SAMPLE_RATE", 0.1)
    )
