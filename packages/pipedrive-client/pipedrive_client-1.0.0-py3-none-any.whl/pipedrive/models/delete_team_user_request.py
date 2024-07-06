from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DeleteTeamUserRequest(BaseModel):
    """DeleteTeamUserRequest

    :param users: The list of user IDs
    :type users: List[int]
    """

    def __init__(self, users: List[int]):
        self.users = users
