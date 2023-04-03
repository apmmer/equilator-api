from openapi.modules.designations.repositories.designations import \
    DesignationsRepo


async def get_designations_repo() -> DesignationsRepo:
    return DesignationsRepo()
