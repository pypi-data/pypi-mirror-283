from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class FileType(Enum):
    """An enumeration representing different categories.

    :cvar GDOC: "gdoc"
    :vartype GDOC: str
    :cvar GSLIDES: "gslides"
    :vartype GSLIDES: str
    :cvar GSHEET: "gsheet"
    :vartype GSHEET: str
    :cvar GFORM: "gform"
    :vartype GFORM: str
    :cvar GDRAW: "gdraw"
    :vartype GDRAW: str
    """

    GDOC = "gdoc"
    GSLIDES = "gslides"
    GSHEET = "gsheet"
    GFORM = "gform"
    GDRAW = "gdraw"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, FileType._member_map_.values()))


class AddFileAndLinkItRequestItemType(Enum):
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
            map(
                lambda x: x.value, AddFileAndLinkItRequestItemType._member_map_.values()
            )
        )


class AddFileAndLinkItRequestRemoteLocation(Enum):
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
                AddFileAndLinkItRequestRemoteLocation._member_map_.values(),
            )
        )


@JsonMap({})
class AddFileAndLinkItRequest(BaseModel):
    """AddFileAndLinkItRequest

    :param file_type: The file type
    :type file_type: FileType
    :param title: The title of the file
    :type title: str
    :param item_type: The item type
    :type item_type: AddFileAndLinkItRequestItemType
    :param item_id: The ID of the item to associate the file with
    :type item_id: int
    :param remote_location: The location type to send the file to. Only `googledrive` is supported at the moment.
    :type remote_location: AddFileAndLinkItRequestRemoteLocation
    """

    def __init__(
        self,
        file_type: FileType,
        title: str,
        item_type: AddFileAndLinkItRequestItemType,
        item_id: int,
        remote_location: AddFileAndLinkItRequestRemoteLocation,
    ):
        self.file_type = self._enum_matching(file_type, FileType.list(), "file_type")
        self.title = title
        self.item_type = self._enum_matching(
            item_type, AddFileAndLinkItRequestItemType.list(), "item_type"
        )
        self.item_id = item_id
        self.remote_location = self._enum_matching(
            remote_location,
            AddFileAndLinkItRequestRemoteLocation.list(),
            "remote_location",
        )
