from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DeleteTeamUserOkResponse(BaseModel):
    """DeleteTeamUserOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The list of user IDs, defaults to None
    :type data: List[int], optional
    """

    def __init__(self, success: bool = None, data: List[int] = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = data
