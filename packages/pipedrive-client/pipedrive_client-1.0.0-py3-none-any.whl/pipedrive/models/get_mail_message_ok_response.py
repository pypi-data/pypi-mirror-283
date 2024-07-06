from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DataFrom2(BaseModel):
    """DataFrom2

    :param id_: ID of the mail participant, defaults to None
    :type id_: int, optional
    :param email_address: Mail address of the mail participant, defaults to None
    :type email_address: str, optional
    :param name: Name of the mail participant, defaults to None
    :type name: str, optional
    :param linked_person_id: ID of the linked person to the mail message, defaults to None
    :type linked_person_id: int, optional
    :param linked_person_name: Name of the linked person to the mail message, defaults to None
    :type linked_person_name: str, optional
    :param mail_message_party_id: ID of the mail message participant, defaults to None
    :type mail_message_party_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        email_address: str = None,
        name: str = None,
        linked_person_id: int = None,
        linked_person_name: str = None,
        mail_message_party_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if email_address is not None:
            self.email_address = email_address
        if name is not None:
            self.name = name
        if linked_person_id is not None:
            self.linked_person_id = linked_person_id
        if linked_person_name is not None:
            self.linked_person_name = linked_person_name
        if mail_message_party_id is not None:
            self.mail_message_party_id = mail_message_party_id


@JsonMap({"id_": "id"})
class DataTo2(BaseModel):
    """DataTo2

    :param id_: ID of the mail participant, defaults to None
    :type id_: int, optional
    :param email_address: Mail address of the mail participant, defaults to None
    :type email_address: str, optional
    :param name: Name of the mail participant, defaults to None
    :type name: str, optional
    :param linked_person_id: ID of the linked person to the mail message, defaults to None
    :type linked_person_id: int, optional
    :param linked_person_name: Name of the linked person to the mail message, defaults to None
    :type linked_person_name: str, optional
    :param mail_message_party_id: ID of the mail message participant, defaults to None
    :type mail_message_party_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        email_address: str = None,
        name: str = None,
        linked_person_id: int = None,
        linked_person_name: str = None,
        mail_message_party_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if email_address is not None:
            self.email_address = email_address
        if name is not None:
            self.name = name
        if linked_person_id is not None:
            self.linked_person_id = linked_person_id
        if linked_person_name is not None:
            self.linked_person_name = linked_person_name
        if mail_message_party_id is not None:
            self.mail_message_party_id = mail_message_party_id


@JsonMap({"id_": "id"})
class DataCc2(BaseModel):
    """DataCc2

    :param id_: ID of the mail participant, defaults to None
    :type id_: int, optional
    :param email_address: Mail address of the mail participant, defaults to None
    :type email_address: str, optional
    :param name: Name of the mail participant, defaults to None
    :type name: str, optional
    :param linked_person_id: ID of the linked person to the mail message, defaults to None
    :type linked_person_id: int, optional
    :param linked_person_name: Name of the linked person to the mail message, defaults to None
    :type linked_person_name: str, optional
    :param mail_message_party_id: ID of the mail message participant, defaults to None
    :type mail_message_party_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        email_address: str = None,
        name: str = None,
        linked_person_id: int = None,
        linked_person_name: str = None,
        mail_message_party_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if email_address is not None:
            self.email_address = email_address
        if name is not None:
            self.name = name
        if linked_person_id is not None:
            self.linked_person_id = linked_person_id
        if linked_person_name is not None:
            self.linked_person_name = linked_person_name
        if mail_message_party_id is not None:
            self.mail_message_party_id = mail_message_party_id


@JsonMap({"id_": "id"})
class DataBcc2(BaseModel):
    """DataBcc2

    :param id_: ID of the mail participant, defaults to None
    :type id_: int, optional
    :param email_address: Mail address of the mail participant, defaults to None
    :type email_address: str, optional
    :param name: Name of the mail participant, defaults to None
    :type name: str, optional
    :param linked_person_id: ID of the linked person to the mail message, defaults to None
    :type linked_person_id: int, optional
    :param linked_person_name: Name of the linked person to the mail message, defaults to None
    :type linked_person_name: str, optional
    :param mail_message_party_id: ID of the mail message participant, defaults to None
    :type mail_message_party_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        email_address: str = None,
        name: str = None,
        linked_person_id: int = None,
        linked_person_name: str = None,
        mail_message_party_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if email_address is not None:
            self.email_address = email_address
        if name is not None:
            self.name = name
        if linked_person_id is not None:
            self.linked_person_id = linked_person_id
        if linked_person_name is not None:
            self.linked_person_name = linked_person_name
        if mail_message_party_id is not None:
            self.mail_message_party_id = mail_message_party_id


class DataMailTrackingStatus2(Enum):
    """An enumeration representing different categories.

    :cvar OPENED: "opened"
    :vartype OPENED: str
    :cvar NOT_OPENED: "not opened"
    :vartype NOT_OPENED: str
    """

    OPENED = "opened"
    NOT_OPENED = "not opened"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, DataMailTrackingStatus2._member_map_.values())
        )


class DataMailLinkTrackingEnabledFlag2(Enum):
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
                DataMailLinkTrackingEnabledFlag2._member_map_.values(),
            )
        )


class DataReadFlag2(Enum):
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
        return list(map(lambda x: x.value, DataReadFlag2._member_map_.values()))


class DataDraftFlag2(Enum):
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
        return list(map(lambda x: x.value, DataDraftFlag2._member_map_.values()))


class DataSyncedFlag2(Enum):
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
        return list(map(lambda x: x.value, DataSyncedFlag2._member_map_.values()))


class DataDeletedFlag7(Enum):
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
        return list(map(lambda x: x.value, DataDeletedFlag7._member_map_.values()))


class DataHasBodyFlag2(Enum):
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
        return list(map(lambda x: x.value, DataHasBodyFlag2._member_map_.values()))


class DataSentFlag2(Enum):
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
        return list(map(lambda x: x.value, DataSentFlag2._member_map_.values()))


class DataSentFromPipedriveFlag2(Enum):
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
            map(lambda x: x.value, DataSentFromPipedriveFlag2._member_map_.values())
        )


class DataSmartBccFlag2(Enum):
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
        return list(map(lambda x: x.value, DataSmartBccFlag2._member_map_.values()))


class DataHasAttachmentsFlag2(Enum):
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
            map(lambda x: x.value, DataHasAttachmentsFlag2._member_map_.values())
        )


class DataHasInlineAttachmentsFlag2(Enum):
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
            map(lambda x: x.value, DataHasInlineAttachmentsFlag2._member_map_.values())
        )


class DataHasRealAttachmentsFlag2(Enum):
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
            map(lambda x: x.value, DataHasRealAttachmentsFlag2._member_map_.values())
        )


@JsonMap({"id_": "id", "from_": "from"})
class GetMailMessageOkResponseData(BaseModel):
    """GetMailMessageOkResponseData

    :param id_: ID of the mail message., defaults to None
    :type id_: int, optional
    :param from_: The array of mail message sender (object), defaults to None
    :type from_: List[DataFrom2], optional
    :param to: The array of mail message receiver (object), defaults to None
    :type to: List[DataTo2], optional
    :param cc: The array of mail message copies (object), defaults to None
    :type cc: List[DataCc2], optional
    :param bcc: The array of mail message blind copies (object), defaults to None
    :type bcc: List[DataBcc2], optional
    :param body_url: The mail message body URL, defaults to None
    :type body_url: str, optional
    :param account_id: The connection account ID, defaults to None
    :type account_id: str, optional
    :param user_id: ID of the user whom mail message will be assigned to, defaults to None
    :type user_id: int, optional
    :param mail_thread_id: ID of the mail message thread, defaults to None
    :type mail_thread_id: int, optional
    :param subject: The subject of mail message, defaults to None
    :type subject: str, optional
    :param snippet: The snippet of mail message. Snippet length is up to 225 characters., defaults to None
    :type snippet: str, optional
    :param mail_tracking_status: The status of tracking mail message. Value is `null` if tracking is not enabled., defaults to None
    :type mail_tracking_status: DataMailTrackingStatus2, optional
    :param mail_link_tracking_enabled_flag: mail_link_tracking_enabled_flag, defaults to None
    :type mail_link_tracking_enabled_flag: DataMailLinkTrackingEnabledFlag2, optional
    :param read_flag: read_flag, defaults to None
    :type read_flag: DataReadFlag2, optional
    :param draft: If the mail message has a draft status then the value is the mail message object as JSON formatted string, otherwise `null`., defaults to None
    :type draft: str, optional
    :param draft_flag: draft_flag, defaults to None
    :type draft_flag: DataDraftFlag2, optional
    :param synced_flag: synced_flag, defaults to None
    :type synced_flag: DataSyncedFlag2, optional
    :param deleted_flag: deleted_flag, defaults to None
    :type deleted_flag: DataDeletedFlag7, optional
    :param has_body_flag: has_body_flag, defaults to None
    :type has_body_flag: DataHasBodyFlag2, optional
    :param sent_flag: sent_flag, defaults to None
    :type sent_flag: DataSentFlag2, optional
    :param sent_from_pipedrive_flag: sent_from_pipedrive_flag, defaults to None
    :type sent_from_pipedrive_flag: DataSentFromPipedriveFlag2, optional
    :param smart_bcc_flag: smart_bcc_flag, defaults to None
    :type smart_bcc_flag: DataSmartBccFlag2, optional
    :param message_time: Creation or receival time of the mail message, defaults to None
    :type message_time: str, optional
    :param add_time: The insertion into the database time of the mail message, defaults to None
    :type add_time: str, optional
    :param update_time: The updating time in the database of the mail message, defaults to None
    :type update_time: str, optional
    :param has_attachments_flag: has_attachments_flag, defaults to None
    :type has_attachments_flag: DataHasAttachmentsFlag2, optional
    :param has_inline_attachments_flag: has_inline_attachments_flag, defaults to None
    :type has_inline_attachments_flag: DataHasInlineAttachmentsFlag2, optional
    :param has_real_attachments_flag: has_real_attachments_flag, defaults to None
    :type has_real_attachments_flag: DataHasRealAttachmentsFlag2, optional
    """

    def __init__(
        self,
        id_: int = None,
        from_: List[DataFrom2] = None,
        to: List[DataTo2] = None,
        cc: List[DataCc2] = None,
        bcc: List[DataBcc2] = None,
        body_url: str = None,
        account_id: str = None,
        user_id: int = None,
        mail_thread_id: int = None,
        subject: str = None,
        snippet: str = None,
        mail_tracking_status: DataMailTrackingStatus2 = None,
        mail_link_tracking_enabled_flag: DataMailLinkTrackingEnabledFlag2 = None,
        read_flag: DataReadFlag2 = None,
        draft: str = None,
        draft_flag: DataDraftFlag2 = None,
        synced_flag: DataSyncedFlag2 = None,
        deleted_flag: DataDeletedFlag7 = None,
        has_body_flag: DataHasBodyFlag2 = None,
        sent_flag: DataSentFlag2 = None,
        sent_from_pipedrive_flag: DataSentFromPipedriveFlag2 = None,
        smart_bcc_flag: DataSmartBccFlag2 = None,
        message_time: str = None,
        add_time: str = None,
        update_time: str = None,
        has_attachments_flag: DataHasAttachmentsFlag2 = None,
        has_inline_attachments_flag: DataHasInlineAttachmentsFlag2 = None,
        has_real_attachments_flag: DataHasRealAttachmentsFlag2 = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if from_ is not None:
            self.from_ = self._define_list(from_, DataFrom2)
        if to is not None:
            self.to = self._define_list(to, DataTo2)
        if cc is not None:
            self.cc = self._define_list(cc, DataCc2)
        if bcc is not None:
            self.bcc = self._define_list(bcc, DataBcc2)
        if body_url is not None:
            self.body_url = body_url
        if account_id is not None:
            self.account_id = account_id
        if user_id is not None:
            self.user_id = user_id
        if mail_thread_id is not None:
            self.mail_thread_id = mail_thread_id
        if subject is not None:
            self.subject = subject
        if snippet is not None:
            self.snippet = snippet
        if mail_tracking_status is not None:
            self.mail_tracking_status = self._enum_matching(
                mail_tracking_status,
                DataMailTrackingStatus2.list(),
                "mail_tracking_status",
            )
        if mail_link_tracking_enabled_flag is not None:
            self.mail_link_tracking_enabled_flag = self._enum_matching(
                mail_link_tracking_enabled_flag,
                DataMailLinkTrackingEnabledFlag2.list(),
                "mail_link_tracking_enabled_flag",
            )
        if read_flag is not None:
            self.read_flag = self._enum_matching(
                read_flag, DataReadFlag2.list(), "read_flag"
            )
        if draft is not None:
            self.draft = draft
        if draft_flag is not None:
            self.draft_flag = self._enum_matching(
                draft_flag, DataDraftFlag2.list(), "draft_flag"
            )
        if synced_flag is not None:
            self.synced_flag = self._enum_matching(
                synced_flag, DataSyncedFlag2.list(), "synced_flag"
            )
        if deleted_flag is not None:
            self.deleted_flag = self._enum_matching(
                deleted_flag, DataDeletedFlag7.list(), "deleted_flag"
            )
        if has_body_flag is not None:
            self.has_body_flag = self._enum_matching(
                has_body_flag, DataHasBodyFlag2.list(), "has_body_flag"
            )
        if sent_flag is not None:
            self.sent_flag = self._enum_matching(
                sent_flag, DataSentFlag2.list(), "sent_flag"
            )
        if sent_from_pipedrive_flag is not None:
            self.sent_from_pipedrive_flag = self._enum_matching(
                sent_from_pipedrive_flag,
                DataSentFromPipedriveFlag2.list(),
                "sent_from_pipedrive_flag",
            )
        if smart_bcc_flag is not None:
            self.smart_bcc_flag = self._enum_matching(
                smart_bcc_flag, DataSmartBccFlag2.list(), "smart_bcc_flag"
            )
        if message_time is not None:
            self.message_time = message_time
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if has_attachments_flag is not None:
            self.has_attachments_flag = self._enum_matching(
                has_attachments_flag,
                DataHasAttachmentsFlag2.list(),
                "has_attachments_flag",
            )
        if has_inline_attachments_flag is not None:
            self.has_inline_attachments_flag = self._enum_matching(
                has_inline_attachments_flag,
                DataHasInlineAttachmentsFlag2.list(),
                "has_inline_attachments_flag",
            )
        if has_real_attachments_flag is not None:
            self.has_real_attachments_flag = self._enum_matching(
                has_real_attachments_flag,
                DataHasRealAttachmentsFlag2.list(),
                "has_real_attachments_flag",
            )


@JsonMap({"status_code": "statusCode", "status_text": "statusText"})
class GetMailMessageOkResponse(BaseModel):
    """GetMailMessageOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param status_code: The email service specific status code and it is returned through the response body., defaults to None
    :type status_code: int, optional
    :param status_text: The status text of the response., defaults to None
    :type status_text: str, optional
    :param service: The service name of the response., defaults to None
    :type service: str, optional
    :param data: data, defaults to None
    :type data: GetMailMessageOkResponseData, optional
    """

    def __init__(
        self,
        success: bool = None,
        status_code: int = None,
        status_text: str = None,
        service: str = None,
        data: GetMailMessageOkResponseData = None,
    ):
        if success is not None:
            self.success = success
        if status_code is not None:
            self.status_code = status_code
        if status_text is not None:
            self.status_text = status_text
        if service is not None:
            self.service = service
        if data is not None:
            self.data = self._define_object(data, GetMailMessageOkResponseData)
