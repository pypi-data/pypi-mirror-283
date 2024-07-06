from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GetPersonUsersOkResponse(BaseModel):
    """GetPersonUsersOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The list of permitted user IDs, defaults to None
    :type data: List[float], optional
    """

    def __init__(self, success: bool = None, data: List[float] = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = data
