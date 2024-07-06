from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class UpdateTeamRequestActiveFlag(Enum):
    """An enumeration representing different categories.

    :cvar _0: 0
    :vartype _0: str
    :cvar _1: 1
    :vartype _1: str
    """

    _0 = 0
    _1 = 1

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, UpdateTeamRequestActiveFlag._member_map_.values())
        )


class UpdateTeamRequestDeletedFlag(Enum):
    """An enumeration representing different categories.

    :cvar _0: 0
    :vartype _0: str
    :cvar _1: 1
    :vartype _1: str
    """

    _0 = 0
    _1 = 1

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, UpdateTeamRequestDeletedFlag._member_map_.values())
        )


@JsonMap({})
class UpdateTeamRequest(BaseModel):
    """UpdateTeamRequest

    :param name: The team name, defaults to None
    :type name: str, optional
    :param description: The team description, defaults to None
    :type description: str, optional
    :param manager_id: The team manager ID, defaults to None
    :type manager_id: int, optional
    :param users: The list of user IDs, defaults to None
    :type users: List[int], optional
    :param active_flag: active_flag, defaults to None
    :type active_flag: UpdateTeamRequestActiveFlag, optional
    :param deleted_flag: deleted_flag, defaults to None
    :type deleted_flag: UpdateTeamRequestDeletedFlag, optional
    """

    def __init__(
        self,
        name: str = None,
        description: str = None,
        manager_id: int = None,
        users: List[int] = None,
        active_flag: UpdateTeamRequestActiveFlag = None,
        deleted_flag: UpdateTeamRequestDeletedFlag = None,
    ):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if manager_id is not None:
            self.manager_id = manager_id
        if users is not None:
            self.users = users
        if active_flag is not None:
            self.active_flag = self._enum_matching(
                active_flag, UpdateTeamRequestActiveFlag.list(), "active_flag"
            )
        if deleted_flag is not None:
            self.deleted_flag = self._enum_matching(
                deleted_flag, UpdateTeamRequestDeletedFlag.list(), "deleted_flag"
            )
