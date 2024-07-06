from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class LinkFileToItemRequestItemType(Enum):
    """An enumeration representing different categories.

    :cvar DEAL: "deal"
    :vartype DEAL: str
    :cvar ORGANIZATION: "organization"
    :vartype ORGANIZATION: str
    :cvar PERSON: "person"
    :vartype PERSON: str
    """

    DEAL = "deal"
    ORGANIZATION = "organization"
    PERSON = "person"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, LinkFileToItemRequestItemType._member_map_.values())
        )


class LinkFileToItemRequestRemoteLocation(Enum):
    """An enumeration representing different categories.

    :cvar GOOGLEDRIVE: "googledrive"
    :vartype GOOGLEDRIVE: str
    """

    GOOGLEDRIVE = "googledrive"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(
                lambda x: x.value,
                LinkFileToItemRequestRemoteLocation._member_map_.values(),
            )
        )


@JsonMap({})
class LinkFileToItemRequest(BaseModel):
    """LinkFileToItemRequest

    :param item_type: The item type
    :type item_type: LinkFileToItemRequestItemType
    :param item_id: The ID of the item to associate the file with
    :type item_id: int
    :param remote_id: The remote item ID
    :type remote_id: str
    :param remote_location: The location type to send the file to. Only `googledrive` is supported at the moment.
    :type remote_location: LinkFileToItemRequestRemoteLocation
    """

    def __init__(
        self,
        item_type: LinkFileToItemRequestItemType,
        item_id: int,
        remote_id: str,
        remote_location: LinkFileToItemRequestRemoteLocation,
    ):
        self.item_type = self._enum_matching(
            item_type, LinkFileToItemRequestItemType.list(), "item_type"
        )
        self.item_id = item_id
        self.remote_id = remote_id
        self.remote_location = self._enum_matching(
            remote_location,
            LinkFileToItemRequestRemoteLocation.list(),
            "remote_location",
        )
