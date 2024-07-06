from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AddTeamRequest(BaseModel):
    """AddTeamRequest

    :param name: The team name
    :type name: str
    :param description: The team description, defaults to None
    :type description: str, optional
    :param manager_id: The team manager ID
    :type manager_id: int
    :param users: The list of user IDs, defaults to None
    :type users: List[int], optional
    """

    def __init__(
        self,
        name: str,
        manager_id: int,
        description: str = None,
        users: List[int] = None,
    ):
        self.name = name
        if description is not None:
            self.description = description
        self.manager_id = manager_id
        if users is not None:
            self.users = users
