from enum import Enum


class Folder(Enum):
    """An enumeration representing different categories.

    :cvar INBOX: "inbox"
    :vartype INBOX: str
    :cvar DRAFTS: "drafts"
    :vartype DRAFTS: str
    :cvar SENT: "sent"
    :vartype SENT: str
    :cvar ARCHIVE: "archive"
    :vartype ARCHIVE: str
    """

    INBOX = "inbox"
    DRAFTS = "drafts"
    SENT = "sent"
    ARCHIVE = "archive"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Folder._member_map_.values()))
