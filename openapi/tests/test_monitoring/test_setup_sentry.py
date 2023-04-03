from openapi.modules.monitoring.setup import setup_sentry
from openapi.tests.test_monitoring.conftest import FakeSentrySDK, MonitoringTest


class Testsuite_setup_sentry(MonitoringTest):
    def test_setup_sentry_called_sdk_init_once(
        self, fake_sentry_sdk_fixt: FakeSentrySDK
    ):
        _ = setup_sentry(
            sentry_sdk=fake_sentry_sdk_fixt
        )
        assert fake_sentry_sdk_fixt.init_called_times == 1

    def test_dsn_in_called_init_args(
        self, fake_sentry_sdk_fixt: FakeSentrySDK
    ):
        _ = setup_sentry(
            sentry_sdk=fake_sentry_sdk_fixt
        )
        assert "dsn" in fake_sentry_sdk_fixt.kwargs

    def test_integrations_in_called_init_args(
        self, fake_sentry_sdk_fixt: FakeSentrySDK
    ):
        _ = setup_sentry(
            sentry_sdk=fake_sentry_sdk_fixt
        )
        assert "integrations" in fake_sentry_sdk_fixt.kwargs

    def test_traces_sample_rate_in_called_init_args(
        self, fake_sentry_sdk_fixt: FakeSentrySDK
    ):
        _ = setup_sentry(
            sentry_sdk=fake_sentry_sdk_fixt
        )
        assert "traces_sample_rate" in fake_sentry_sdk_fixt.kwargs

    def test_no_args_in_called_init_method(
        self, fake_sentry_sdk_fixt: FakeSentrySDK
    ):
        _ = setup_sentry(
            sentry_sdk=fake_sentry_sdk_fixt
        )
        assert not fake_sentry_sdk_fixt.args
