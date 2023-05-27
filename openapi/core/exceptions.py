from typing import List, Optional

from fastapi import HTTPException, status
from pydantic.error_wrappers import ValidationError as pd_ValidationError


class DefaultException(HTTPException):
    """
    A basic exception that will turn into a response
    from the server with the specified status code and detail.
    This class is usually used for inheritance,
    but it can also be used by itself
    """

    detail: str = "Server cannot process your request."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        detail: Optional[str] = None,
        status_code: Optional[int] = None
    ):
        if not detail:
            self.detail = self.__class__.detail
        else:
            self.detail = detail
        if not status_code:
            self.status_code = self.__class__.status_code
        else:
            self.status_code = status_code


class ObjectNotFoundError(DefaultException):
    detail: str = "Object not found."
    status_code: int = status.HTTP_404_NOT_FOUND

    def __init__(
        self,
        fields_names: Optional[List[str]] = None,
        fields_values: Optional[List[str]] = None,
        *args, **kwargs
    ):

        if fields_names and fields_values:
            detail = (
                f"Object with attributes {fields_names}"
                f" and values ({fields_values}) was not found.")
            kwargs["detail"] = detail
        super().__init__(*args, **kwargs)


class UniqueFieldError(DefaultException):
    detail: str = "UniqueFieldError."
    status_code: int = status.HTTP_409_CONFLICT

    # we don't want to respond raw details from postgre.
    # so, parse postgre details.
    def __init__(
        self,
        detail: Optional[str] = None,
        status_code: Optional[int] = None
    ):
        if detail:
            detail = self.parse_detail(detail)
        super().__init__(detail=detail, status_code=status_code)

    def parse_detail(self, detail: str) -> str:
        try:
            index = detail.index("Key (")
            detail = f"Object with {detail[index + 4:]}"
        except ValueError:
            pass
        return detail


class ForeignKeyError(DefaultException):
    detail: str = "ForeignKeyError."
    status_code: int = status.HTTP_409_CONFLICT

    def __init__(
        self,
        detail: Optional[str] = None,
        status_code: Optional[int] = None
    ):
        if detail:
            detail = self._parse_detail(detail)
        super().__init__(detail=detail, status_code=status_code)

    def _parse_detail(self, detail: str) -> str:
        """
        Replaces asyncpg detail's message with custom variant.
        """

        try:
            index = detail.index("Key (")
            detail = f"Object with {detail[index + 4:]}"
            index = detail.index("present in table")
            detail = f"{detail[:index]}presented."

        except ValueError:
            detail = self.detail
        return detail


class PydanticValidationError(DefaultException):
    status_code: int = 422

    def __init__(
        self,
        detail: Optional[str] = None,
        status_code: Optional[int] = None,
        ex: Optional[pd_ValidationError] = None
    ):
        """
        When ex (pydantic.error_wrappers ValidationError) is provided ->
        then erorr detail will be taken from it
        """

        if status_code:
            self.status_code = status_code
        if ex and isinstance(ex, pd_ValidationError):
            self.detail = ex.errors()
        elif detail:
            self.detail = detail
        super().__init__(
            detail=self.detail,
            status_code=self.status_code
        )


class SQLException(DefaultException):
    detail: str = "Exception during database request."
    status_code: int = status.HTTP_409_CONFLICT


class WrongFiltersError(DefaultException):
    """
    This exception is usually raised when input filters were incorrect.
    """

    detail: str = "Input filters contain wrong fields."
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, wrong_fields: Optional[List[str]] = None):
        if wrong_fields:
            self.detail = f"Input filters contain wrong fields: {wrong_fields}"


class GotMultipleObjectsError(DefaultException):
    """
    This exception is usually raised when many objects were received
    from the database, but only one was expected.
    """

    detail: str = "Got multiple objects with provided filters."
    status_code: int = status.HTTP_406_NOT_ACCEPTABLE
