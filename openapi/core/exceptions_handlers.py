from typing import Any, List, Optional
from pydantic.error_wrappers import ValidationError as PydValidationError
from openapi.core.exceptions import PydanticValidationError
from loguru import logger


class ReplaceExceptions:
    """
    Class-decorator,
    that allows to replace supported exceptions with correct fastapi variants.

    Args:
        exceptions (List[Exception]): List of exceptions to retry,
        other will be raised.
        repeat (int): how many times to retry (repeat a function call)
        delay(float | None): if delay is necessary between retries (seconds).

    Returns:
        decorated function
    """

    supported_exceptions = [PydValidationError]

    def __init__(
        self,
        exceptions: Optional[List[Exception]] = None
    ) -> None:
        if exceptions:
            for exc in exceptions:
                assert exc in self.supported_exceptions
            self.exceptions = exceptions
        else:
            self.exceptions = self.supported_exceptions

    def __call__(self, function: callable) -> Any:
        async def _wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await function(*args, **kwargs)
            except Exception as ex:
                if type(ex) not in self.exceptions:
                    logger.critical("Exception {type(ex)} IS NOT SUPPORTED.")
                    raise ex
                if type(ex) == PydValidationError:
                    raise PydanticValidationError(ex=ex)
        return _wrapper
