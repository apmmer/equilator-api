from openapi.modules.reports.report_handler import EquityReportsHandler


async def get_reports_handler() -> EquityReportsHandler:
    return EquityReportsHandler()
