from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class DataActiveFlag4(Enum):
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
        return list(map(lambda x: x.value, DataActiveFlag4._member_map_.values()))


class DataDeletedFlag5(Enum):
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
        return list(map(lambda x: x.value, DataDeletedFlag5._member_map_.values()))


@JsonMap({"id_": "id"})
class UpdateTeamOkResponseData(BaseModel):
    """UpdateTeamOkResponseData

    :param id_: The team ID, defaults to None
    :type id_: int, optional
    :param name: The team name, defaults to None
    :type name: str, optional
    :param description: The team description, defaults to None
    :type description: str, optional
    :param manager_id: The team manager ID, defaults to None
    :type manager_id: int, optional
    :param users: The list of user IDs, defaults to None
    :type users: List[int], optional
    :param active_flag: active_flag, defaults to None
    :type active_flag: DataActiveFlag4, optional
    :param deleted_flag: deleted_flag, defaults to None
    :type deleted_flag: DataDeletedFlag5, optional
    :param add_time: The team creation time. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    :param created_by_user_id: The ID of the user who created the team, defaults to None
    :type created_by_user_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        description: str = None,
        manager_id: int = None,
        users: List[int] = None,
        active_flag: DataActiveFlag4 = None,
        deleted_flag: DataDeletedFlag5 = None,
        add_time: str = None,
        created_by_user_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
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
                active_flag, DataActiveFlag4.list(), "active_flag"
            )
        if deleted_flag is not None:
            self.deleted_flag = self._enum_matching(
                deleted_flag, DataDeletedFlag5.list(), "deleted_flag"
            )
        if add_time is not None:
            self.add_time = add_time
        if created_by_user_id is not None:
            self.created_by_user_id = created_by_user_id


@JsonMap({})
class UpdateTeamOkResponse(BaseModel):
    """UpdateTeamOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: UpdateTeamOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: UpdateTeamOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, UpdateTeamOkResponseData)
