"""
Module for storing models mixins
"""


class DBBaseMixin:
    """
    Default DB mixin with basic useful methods
    """

    def custom_representation(self, **repr_fields) -> str:
        """
        Prepares custom representation for a model.
        Based on class name and fields send.
        """

        result = " , ".join([f"{k}={v}" for k, v in repr_fields.items()])
        return f"{self.__class__.__name__}({result})"

    async def update(self, **new_values) -> None:
        """
        Updates DB model with new values
        """

        for key, value in new_values.items():
            if hasattr(self, key):
                setattr(self, key, value)
