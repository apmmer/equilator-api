from openapi.modules.ranges.repo_manager import RepositoriesManager
from openapi.modules.ranges.repositories.ranges import RangesRepo


async def get_ranges_repo() -> RangesRepo:
    return RangesRepo()


async def get_repo_manager() -> RepositoriesManager:
    return RepositoriesManager()
