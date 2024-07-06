from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class DataReadFlag6(Enum):
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
        return list(map(lambda x: x.value, DataReadFlag6._member_map_.values()))


class DataHasAttachmentsFlag6(Enum):
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
            map(lambda x: x.value, DataHasAttachmentsFlag6._member_map_.values())
        )


class DataHasInlineAttachmentsFlag6(Enum):
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
            map(lambda x: x.value, DataHasInlineAttachmentsFlag6._member_map_.values())
        )


class DataHasRealAttachmentsFlag6(Enum):
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
            map(lambda x: x.value, DataHasRealAttachmentsFlag6._member_map_.values())
        )


class DataDeletedFlag11(Enum):
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
        return list(map(lambda x: x.value, DataDeletedFlag11._member_map_.values()))


class DataSyncedFlag6(Enum):
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
        return list(map(lambda x: x.value, DataSyncedFlag6._member_map_.values()))


class DataSmartBccFlag6(Enum):
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
        return list(map(lambda x: x.value, DataSmartBccFlag6._member_map_.values()))


class DataMailLinkTrackingEnabledFlag6(Enum):
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
                DataMailLinkTrackingEnabledFlag6._member_map_.values(),
            )
        )


@JsonMap({"id_": "id"})
class DataFrom3(BaseModel):
    """Member of a thread

    :param id_: ID of the mail thread participant, defaults to None
    :type id_: int, optional
    :param name: Name of the mail thread participant, defaults to None
    :type name: str, optional
    :param latest_sent: Whether the mail thread participant was last to send an email, defaults to None
    :type latest_sent: bool, optional
    :param email_address: Email address of the mail thread participant, defaults to None
    :type email_address: str, optional
    :param message_time: Message time, defaults to None
    :type message_time: float, optional
    :param linked_person_id: ID of the linked person, defaults to None
    :type linked_person_id: int, optional
    :param linked_person_name: Email of the linked person, defaults to None
    :type linked_person_name: str, optional
    :param mail_message_party_id: ID of the mail message party, defaults to None
    :type mail_message_party_id: int, optional
    :param linked_organization_id: Linked Organization ID, defaults to None
    :type linked_organization_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        latest_sent: bool = None,
        email_address: str = None,
        message_time: float = None,
        linked_person_id: int = None,
        linked_person_name: str = None,
        mail_message_party_id: int = None,
        linked_organization_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if latest_sent is not None:
            self.latest_sent = latest_sent
        if email_address is not None:
            self.email_address = email_address
        if message_time is not None:
            self.message_time = message_time
        if linked_person_id is not None:
            self.linked_person_id = linked_person_id
        if linked_person_name is not None:
            self.linked_person_name = linked_person_name
        if mail_message_party_id is not None:
            self.mail_message_party_id = mail_message_party_id
        if linked_organization_id is not None:
            self.linked_organization_id = linked_organization_id


@JsonMap({"id_": "id"})
class DataTo3(BaseModel):
    """Member of a thread

    :param id_: ID of the mail thread participant, defaults to None
    :type id_: int, optional
    :param name: Name of the mail thread participant, defaults to None
    :type name: str, optional
    :param latest_sent: Whether the mail thread participant was last to send an email, defaults to None
    :type latest_sent: bool, optional
    :param email_address: Email address of the mail thread participant, defaults to None
    :type email_address: str, optional
    :param message_time: Message time, defaults to None
    :type message_time: float, optional
    :param linked_person_id: ID of the linked person, defaults to None
    :type linked_person_id: int, optional
    :param linked_person_name: Email of the linked person, defaults to None
    :type linked_person_name: str, optional
    :param mail_message_party_id: ID of the mail message party, defaults to None
    :type mail_message_party_id: int, optional
    :param linked_organization_id: Linked Organization ID, defaults to None
    :type linked_organization_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        latest_sent: bool = None,
        email_address: str = None,
        message_time: float = None,
        linked_person_id: int = None,
        linked_person_name: str = None,
        mail_message_party_id: int = None,
        linked_organization_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if latest_sent is not None:
            self.latest_sent = latest_sent
        if email_address is not None:
            self.email_address = email_address
        if message_time is not None:
            self.message_time = message_time
        if linked_person_id is not None:
            self.linked_person_id = linked_person_id
        if linked_person_name is not None:
            self.linked_person_name = linked_person_name
        if mail_message_party_id is not None:
            self.mail_message_party_id = mail_message_party_id
        if linked_organization_id is not None:
            self.linked_organization_id = linked_organization_id


@JsonMap({"id_": "id"})
class DataCc3(BaseModel):
    """Member of a thread

    :param id_: ID of the mail thread participant, defaults to None
    :type id_: int, optional
    :param name: Name of the mail thread participant, defaults to None
    :type name: str, optional
    :param latest_sent: Whether the mail thread participant was last to send an email, defaults to None
    :type latest_sent: bool, optional
    :param email_address: Email address of the mail thread participant, defaults to None
    :type email_address: str, optional
    :param message_time: Message time, defaults to None
    :type message_time: float, optional
    :param linked_person_id: ID of the linked person, defaults to None
    :type linked_person_id: int, optional
    :param linked_person_name: Email of the linked person, defaults to None
    :type linked_person_name: str, optional
    :param mail_message_party_id: ID of the mail message party, defaults to None
    :type mail_message_party_id: int, optional
    :param linked_organization_id: Linked Organization ID, defaults to None
    :type linked_organization_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        latest_sent: bool = None,
        email_address: str = None,
        message_time: float = None,
        linked_person_id: int = None,
        linked_person_name: str = None,
        mail_message_party_id: int = None,
        linked_organization_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if latest_sent is not None:
            self.latest_sent = latest_sent
        if email_address is not None:
            self.email_address = email_address
        if message_time is not None:
            self.message_time = message_time
        if linked_person_id is not None:
            self.linked_person_id = linked_person_id
        if linked_person_name is not None:
            self.linked_person_name = linked_person_name
        if mail_message_party_id is not None:
            self.mail_message_party_id = mail_message_party_id
        if linked_organization_id is not None:
            self.linked_organization_id = linked_organization_id


@JsonMap({"id_": "id"})
class DataBcc3(BaseModel):
    """Member of a thread

    :param id_: ID of the mail thread participant, defaults to None
    :type id_: int, optional
    :param name: Name of the mail thread participant, defaults to None
    :type name: str, optional
    :param latest_sent: Whether the mail thread participant was last to send an email, defaults to None
    :type latest_sent: bool, optional
    :param email_address: Email address of the mail thread participant, defaults to None
    :type email_address: str, optional
    :param message_time: Message time, defaults to None
    :type message_time: float, optional
    :param linked_person_id: ID of the linked person, defaults to None
    :type linked_person_id: int, optional
    :param linked_person_name: Email of the linked person, defaults to None
    :type linked_person_name: str, optional
    :param mail_message_party_id: ID of the mail message party, defaults to None
    :type mail_message_party_id: int, optional
    :param linked_organization_id: Linked Organization ID, defaults to None
    :type linked_organization_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        latest_sent: bool = None,
        email_address: str = None,
        message_time: float = None,
        linked_person_id: int = None,
        linked_person_name: str = None,
        mail_message_party_id: int = None,
        linked_organization_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if latest_sent is not None:
            self.latest_sent = latest_sent
        if email_address is not None:
            self.email_address = email_address
        if message_time is not None:
            self.message_time = message_time
        if linked_person_id is not None:
            self.linked_person_id = linked_person_id
        if linked_person_name is not None:
            self.linked_person_name = linked_person_name
        if mail_message_party_id is not None:
            self.mail_message_party_id = mail_message_party_id
        if linked_organization_id is not None:
            self.linked_organization_id = linked_organization_id


class DataHasBodyFlag3(Enum):
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
        return list(map(lambda x: x.value, DataHasBodyFlag3._member_map_.values()))


class DataSentFlag3(Enum):
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
        return list(map(lambda x: x.value, DataSentFlag3._member_map_.values()))


class DataSentFromPipedriveFlag3(Enum):
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
            map(lambda x: x.value, DataSentFromPipedriveFlag3._member_map_.values())
        )


@JsonMap({"id_": "id", "from_": "from"})
class GetMailThreadMessagesOkResponseData(BaseModel):
    """GetMailThreadMessagesOkResponseData

    :param id_: ID of the mail thread, defaults to None
    :type id_: int, optional
    :param account_id: The connection account ID, defaults to None
    :type account_id: str, optional
    :param user_id: ID of the user whom mail message will be assigned to, defaults to None
    :type user_id: int, optional
    :param subject: The subject, defaults to None
    :type subject: str, optional
    :param snippet: A snippet, defaults to None
    :type snippet: str, optional
    :param read_flag: read_flag, defaults to None
    :type read_flag: DataReadFlag6, optional
    :param mail_tracking_status: Mail tracking status, defaults to None
    :type mail_tracking_status: str, optional
    :param has_attachments_flag: has_attachments_flag, defaults to None
    :type has_attachments_flag: DataHasAttachmentsFlag6, optional
    :param has_inline_attachments_flag: has_inline_attachments_flag, defaults to None
    :type has_inline_attachments_flag: DataHasInlineAttachmentsFlag6, optional
    :param has_real_attachments_flag: has_real_attachments_flag, defaults to None
    :type has_real_attachments_flag: DataHasRealAttachmentsFlag6, optional
    :param deleted_flag: deleted_flag, defaults to None
    :type deleted_flag: DataDeletedFlag11, optional
    :param synced_flag: synced_flag, defaults to None
    :type synced_flag: DataSyncedFlag6, optional
    :param smart_bcc_flag: smart_bcc_flag, defaults to None
    :type smart_bcc_flag: DataSmartBccFlag6, optional
    :param mail_link_tracking_enabled_flag: mail_link_tracking_enabled_flag, defaults to None
    :type mail_link_tracking_enabled_flag: DataMailLinkTrackingEnabledFlag6, optional
    :param from_: Senders of the mail thread, defaults to None
    :type from_: List[DataFrom3], optional
    :param to: Recipients of the mail thread, defaults to None
    :type to: List[DataTo3], optional
    :param cc: Participants of the Cc, defaults to None
    :type cc: List[DataCc3], optional
    :param bcc: Participants of the Bcc, defaults to None
    :type bcc: List[DataBcc3], optional
    :param body_url: A link to the mail thread message, defaults to None
    :type body_url: str, optional
    :param mail_thread_id: ID of the mail thread, defaults to None
    :type mail_thread_id: int, optional
    :param draft: If the mail message has a draft status then the value is the mail message object as JSON formatted string, otherwise `null`., defaults to None
    :type draft: str, optional
    :param has_body_flag: has_body_flag, defaults to None
    :type has_body_flag: DataHasBodyFlag3, optional
    :param sent_flag: sent_flag, defaults to None
    :type sent_flag: DataSentFlag3, optional
    :param sent_from_pipedrive_flag: sent_from_pipedrive_flag, defaults to None
    :type sent_from_pipedrive_flag: DataSentFromPipedriveFlag3, optional
    :param message_time: The time when the mail message was received or created, defaults to None
    :type message_time: str, optional
    :param add_time: The time when the mail message was inserted to database, defaults to None
    :type add_time: str, optional
    :param update_time: The time when the mail message was updated in database received, defaults to None
    :type update_time: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        account_id: str = None,
        user_id: int = None,
        subject: str = None,
        snippet: str = None,
        read_flag: DataReadFlag6 = None,
        mail_tracking_status: str = None,
        has_attachments_flag: DataHasAttachmentsFlag6 = None,
        has_inline_attachments_flag: DataHasInlineAttachmentsFlag6 = None,
        has_real_attachments_flag: DataHasRealAttachmentsFlag6 = None,
        deleted_flag: DataDeletedFlag11 = None,
        synced_flag: DataSyncedFlag6 = None,
        smart_bcc_flag: DataSmartBccFlag6 = None,
        mail_link_tracking_enabled_flag: DataMailLinkTrackingEnabledFlag6 = None,
        from_: List[DataFrom3] = None,
        to: List[DataTo3] = None,
        cc: List[DataCc3] = None,
        bcc: List[DataBcc3] = None,
        body_url: str = None,
        mail_thread_id: int = None,
        draft: str = None,
        has_body_flag: DataHasBodyFlag3 = None,
        sent_flag: DataSentFlag3 = None,
        sent_from_pipedrive_flag: DataSentFromPipedriveFlag3 = None,
        message_time: str = None,
        add_time: str = None,
        update_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if account_id is not None:
            self.account_id = account_id
        if user_id is not None:
            self.user_id = user_id
        if subject is not None:
            self.subject = subject
        if snippet is not None:
            self.snippet = snippet
        if read_flag is not None:
            self.read_flag = self._enum_matching(
                read_flag, DataReadFlag6.list(), "read_flag"
            )
        if mail_tracking_status is not None:
            self.mail_tracking_status = mail_tracking_status
        if has_attachments_flag is not None:
            self.has_attachments_flag = self._enum_matching(
                has_attachments_flag,
                DataHasAttachmentsFlag6.list(),
                "has_attachments_flag",
            )
        if has_inline_attachments_flag is not None:
            self.has_inline_attachments_flag = self._enum_matching(
                has_inline_attachments_flag,
                DataHasInlineAttachmentsFlag6.list(),
                "has_inline_attachments_flag",
            )
        if has_real_attachments_flag is not None:
            self.has_real_attachments_flag = self._enum_matching(
                has_real_attachments_flag,
                DataHasRealAttachmentsFlag6.list(),
                "has_real_attachments_flag",
            )
        if deleted_flag is not None:
            self.deleted_flag = self._enum_matching(
                deleted_flag, DataDeletedFlag11.list(), "deleted_flag"
            )
        if synced_flag is not None:
            self.synced_flag = self._enum_matching(
                synced_flag, DataSyncedFlag6.list(), "synced_flag"
            )
        if smart_bcc_flag is not None:
            self.smart_bcc_flag = self._enum_matching(
                smart_bcc_flag, DataSmartBccFlag6.list(), "smart_bcc_flag"
            )
        if mail_link_tracking_enabled_flag is not None:
            self.mail_link_tracking_enabled_flag = self._enum_matching(
                mail_link_tracking_enabled_flag,
                DataMailLinkTrackingEnabledFlag6.list(),
                "mail_link_tracking_enabled_flag",
            )
        if from_ is not None:
            self.from_ = self._define_list(from_, DataFrom3)
        if to is not None:
            self.to = self._define_list(to, DataTo3)
        if cc is not None:
            self.cc = self._define_list(cc, DataCc3)
        if bcc is not None:
            self.bcc = self._define_list(bcc, DataBcc3)
        if body_url is not None:
            self.body_url = body_url
        if mail_thread_id is not None:
            self.mail_thread_id = mail_thread_id
        if draft is not None:
            self.draft = draft
        if has_body_flag is not None:
            self.has_body_flag = self._enum_matching(
                has_body_flag, DataHasBodyFlag3.list(), "has_body_flag"
            )
        if sent_flag is not None:
            self.sent_flag = self._enum_matching(
                sent_flag, DataSentFlag3.list(), "sent_flag"
            )
        if sent_from_pipedrive_flag is not None:
            self.sent_from_pipedrive_flag = self._enum_matching(
                sent_from_pipedrive_flag,
                DataSentFromPipedriveFlag3.list(),
                "sent_from_pipedrive_flag",
            )
        if message_time is not None:
            self.message_time = message_time
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time


@JsonMap({})
class GetMailThreadMessagesOkResponse(BaseModel):
    """GetMailThreadMessagesOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of the mail messages of the mail thread, defaults to None
    :type data: List[GetMailThreadMessagesOkResponseData], optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetMailThreadMessagesOkResponseData] = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetMailThreadMessagesOkResponseData)
