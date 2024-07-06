from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class MergeOrganizationsRequest(BaseModel):
    """MergeOrganizationsRequest

    :param merge_with_id: The ID of the organization that the organization will be merged with
    :type merge_with_id: int
    """

    def __init__(self, merge_with_id: int):
        self.merge_with_id = merge_with_id
