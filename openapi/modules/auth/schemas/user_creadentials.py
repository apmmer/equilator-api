from pydantic import BaseModel


class UserCredentials(BaseModel):
    """
        Schema for the request parameters for obtaining the token.
    """

    username: str
    password: str
