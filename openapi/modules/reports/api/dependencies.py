from openapi.modules.reports.report_handler import EquityReportsHandler
from openapi.modules.ranges.repositories.ranges import RangesRepo
from openapi.modules.ranges.repo_manager import RepositoriesManager


async def get_reports_handler() -> EquityReportsHandler:
    return EquityReportsHandler()
