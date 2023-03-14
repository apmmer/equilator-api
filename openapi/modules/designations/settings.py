"""
Specific module settings are located here.
"""


class DesignationsSettings:
    """
    Designations module settings.
    """

    router_prefix: str = "/designations"
    router_tag: str = "Designations"
    max_range_definition_length: int = 5000
    min_range_definition_length: int = 2
