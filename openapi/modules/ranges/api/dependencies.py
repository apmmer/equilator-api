from openapi.modules.ranges.repositories.ranges import RangesRepo
from openapi.modules.ranges.repo_manager import RepositoriesManager


async def get_ranges_repo() -> RangesRepo:
    return RangesRepo()


async def get_repo_manager() -> RepositoriesManager:
    return RepositoriesManager()
