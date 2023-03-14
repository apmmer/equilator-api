from openapi.modules.ranges.repo_manager import RepositoriesManager
from openapi.modules.ranges.repositories.ranges import RangesRepo
from openapi.modules.reports.report_handler import EquityReportsHandler


async def get_reports_handler() -> EquityReportsHandler:
    return EquityReportsHandler()
