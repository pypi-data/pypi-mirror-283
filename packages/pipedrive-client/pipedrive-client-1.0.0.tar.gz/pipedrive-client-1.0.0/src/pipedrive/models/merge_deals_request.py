from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class MergeDealsRequest(BaseModel):
    """MergeDealsRequest

    :param merge_with_id: The ID of the deal that the deal will be merged with
    :type merge_with_id: int
    """

    def __init__(self, merge_with_id: int):
        self.merge_with_id = merge_with_id
