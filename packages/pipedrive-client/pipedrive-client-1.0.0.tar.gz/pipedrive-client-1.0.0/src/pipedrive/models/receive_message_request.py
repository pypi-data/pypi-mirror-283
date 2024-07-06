from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class ReceiveMessageRequestStatus(Enum):
    """An enumeration representing different categories.

    :cvar SENT: "sent"
    :vartype SENT: str
    :cvar DELIVERED: "delivered"
    :vartype DELIVERED: str
    :cvar READ: "read"
    :vartype READ: str
    :cvar FAILED: "failed"
    :vartype FAILED: str
    """

    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, ReceiveMessageRequestStatus._member_map_.values())
        )


@JsonMap({"id_": "id", "type_": "type"})
class ReceiveMessageRequestAttachments(BaseModel):
    """ReceiveMessageRequestAttachments

    :param id_: The ID of the attachment
    :type id_: str
    :param type_: The mime-type of the attachment
    :type type_: str
    :param name: The name of the attachment, defaults to None
    :type name: str, optional
    :param size: The size of the attachment, defaults to None
    :type size: float, optional
    :param url: A URL to the file
    :type url: str
    :param preview_url: A URL to a preview picture of the file, defaults to None
    :type preview_url: str, optional
    :param link_expires: If true, it will use the getMessageById endpoint for fetching updated attachment's urls. Find out more [here](https://pipedrive.readme.io/docs/implementing-messaging-app-extension), defaults to None
    :type link_expires: bool, optional
    """

    def __init__(
        self,
        id_: str,
        type_: str,
        url: str,
        name: str = None,
        size: float = None,
        preview_url: str = None,
        link_expires: bool = None,
    ):
        self.id_ = id_
        self.type_ = type_
        if name is not None:
            self.name = name
        if size is not None:
            self.size = size
        self.url = url
        if preview_url is not None:
            self.preview_url = preview_url
        if link_expires is not None:
            self.link_expires = link_expires


@JsonMap({"id_": "id"})
class ReceiveMessageRequest(BaseModel):
    """ReceiveMessageRequest

    :param id_: The ID of the message
    :type id_: str
    :param channel_id: The channel ID as in the provider
    :type channel_id: str
    :param sender_id: The ID of the provider's user that sent the message
    :type sender_id: str
    :param conversation_id: The ID of the conversation
    :type conversation_id: str
    :param message: The body of the message
    :type message: str
    :param status: The status of the message
    :type status: ReceiveMessageRequestStatus
    :param created_at: The date and time when the message was created in the provider, in UTC. Format: YYYY-MM-DD HH:MM
    :type created_at: str
    :param reply_by: The date and time when the message can no longer receive a reply, in UTC. Format: YYYY-MM-DD HH:MM, defaults to None
    :type reply_by: str, optional
    :param conversation_link: A URL that can open the conversation in the provider's side, defaults to None
    :type conversation_link: str, optional
    :param attachments: The list of attachments available in the message, defaults to None
    :type attachments: List[ReceiveMessageRequestAttachments], optional
    """

    def __init__(
        self,
        id_: str,
        channel_id: str,
        sender_id: str,
        conversation_id: str,
        message: str,
        status: ReceiveMessageRequestStatus,
        created_at: str,
        reply_by: str = None,
        conversation_link: str = None,
        attachments: List[ReceiveMessageRequestAttachments] = None,
    ):
        self.id_ = id_
        self.channel_id = channel_id
        self.sender_id = sender_id
        self.conversation_id = conversation_id
        self.message = message
        self.status = self._enum_matching(
            status, ReceiveMessageRequestStatus.list(), "status"
        )
        self.created_at = created_at
        if reply_by is not None:
            self.reply_by = reply_by
        if conversation_link is not None:
            self.conversation_link = conversation_link
        if attachments is not None:
            self.attachments = self._define_list(
                attachments, ReceiveMessageRequestAttachments
            )
