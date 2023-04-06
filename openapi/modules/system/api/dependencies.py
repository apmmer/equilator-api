from openapi.modules.system.repositories.system import SystemRepo


async def get_system_repo() -> SystemRepo:
    return SystemRepo(model=None)
