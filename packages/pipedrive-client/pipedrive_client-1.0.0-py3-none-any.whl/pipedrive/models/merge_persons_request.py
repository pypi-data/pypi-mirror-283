from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class MergePersonsRequest(BaseModel):
    """MergePersonsRequest

    :param merge_with_id: The ID of the person that will not be overwritten. This person’s data will be prioritized in case of conflict with the other person.
    :type merge_with_id: int
    """

    def __init__(self, merge_with_id: int):
        self.merge_with_id = merge_with_id
