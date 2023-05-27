from openapi.modules.designations.repositories.designations import \
    DesignationsRepo
from openapi.modules.equilator.range_converter import convert_from_string
from openapi.modules.ranges.repositories.ranges import RangesRepo
from openapi.modules.ranges.schemas.ranges import WeightedRange


class RepositoriesManager:
    """
    This class is used to manipulate multiple repositories
    to avoid the appearance of dirt in each of the private repositories.
    """

    def __init__(self):
        self.ranges_repo = RangesRepo()
        self.designation_repo = DesignationsRepo()

    async def add_range_using_designation(
        self,
        name: str,
        designation_id: str,
        default_weight: float
    ) -> WeightedRange:
        """
        Converts range designation into weighted range using both repositories

        Args:
            name (str): name of a weighted range
            designation_id (str): link to a designation
            default_weight (float): this weight will be applied to all hands in range

        Returns:
            WeightedRange: created weight range object
        """

        designation = await self.designation_repo.get_an_item(
            id=designation_id
        )

        range_list = convert_from_string(
            user_input=designation.range_definition
        )
        definition = {}
        for hand_name in range_list:
            definition[hand_name] = default_weight

        weighted_range = await self.ranges_repo.add_an_item(
            data={
                "name": name,
                "definition": definition
            }
        )
        return weighted_range
