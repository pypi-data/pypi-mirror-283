from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class UpdateMailThreadDetailsRequestSharedFlag(Enum):
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
            map(
                lambda x: x.value,
                UpdateMailThreadDetailsRequestSharedFlag._member_map_.values(),
            )
        )


class UpdateMailThreadDetailsRequestReadFlag(Enum):
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
            map(
                lambda x: x.value,
                UpdateMailThreadDetailsRequestReadFlag._member_map_.values(),
            )
        )


class UpdateMailThreadDetailsRequestArchivedFlag(Enum):
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
            map(
                lambda x: x.value,
                UpdateMailThreadDetailsRequestArchivedFlag._member_map_.values(),
            )
        )


@JsonMap({})
class UpdateMailThreadDetailsRequest(BaseModel):
    """UpdateMailThreadDetailsRequest

    :param deal_id: The ID of the deal this thread is associated with, defaults to None
    :type deal_id: int, optional
    :param lead_id: The ID of the lead this thread is associated with, defaults to None
    :type lead_id: str, optional
    :param shared_flag: shared_flag, defaults to None
    :type shared_flag: UpdateMailThreadDetailsRequestSharedFlag, optional
    :param read_flag: read_flag, defaults to None
    :type read_flag: UpdateMailThreadDetailsRequestReadFlag, optional
    :param archived_flag: archived_flag, defaults to None
    :type archived_flag: UpdateMailThreadDetailsRequestArchivedFlag, optional
    """

    def __init__(
        self,
        deal_id: int = None,
        lead_id: str = None,
        shared_flag: UpdateMailThreadDetailsRequestSharedFlag = None,
        read_flag: UpdateMailThreadDetailsRequestReadFlag = None,
        archived_flag: UpdateMailThreadDetailsRequestArchivedFlag = None,
    ):
        if deal_id is not None:
            self.deal_id = deal_id
        if lead_id is not None:
            self.lead_id = lead_id
        if shared_flag is not None:
            self.shared_flag = self._enum_matching(
                shared_flag,
                UpdateMailThreadDetailsRequestSharedFlag.list(),
                "shared_flag",
            )
        if read_flag is not None:
            self.read_flag = self._enum_matching(
                read_flag, UpdateMailThreadDetailsRequestReadFlag.list(), "read_flag"
            )
        if archived_flag is not None:
            self.archived_flag = self._enum_matching(
                archived_flag,
                UpdateMailThreadDetailsRequestArchivedFlag.list(),
                "archived_flag",
            )
