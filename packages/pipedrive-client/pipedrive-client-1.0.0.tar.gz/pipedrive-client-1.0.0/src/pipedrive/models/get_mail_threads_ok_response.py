from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class DataReadFlag3(Enum):
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
        return list(map(lambda x: x.value, DataReadFlag3._member_map_.values()))


class DataHasAttachmentsFlag3(Enum):
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
            map(lambda x: x.value, DataHasAttachmentsFlag3._member_map_.values())
        )


class DataHasInlineAttachmentsFlag3(Enum):
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
            map(lambda x: x.value, DataHasInlineAttachmentsFlag3._member_map_.values())
        )


class DataHasRealAttachmentsFlag3(Enum):
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
            map(lambda x: x.value, DataHasRealAttachmentsFlag3._member_map_.values())
        )


class DataDeletedFlag8(Enum):
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
        return list(map(lambda x: x.value, DataDeletedFlag8._member_map_.values()))


class DataSyncedFlag3(Enum):
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
        return list(map(lambda x: x.value, DataSyncedFlag3._member_map_.values()))


class DataSmartBccFlag3(Enum):
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
        return list(map(lambda x: x.value, DataSmartBccFlag3._member_map_.values()))


class DataMailLinkTrackingEnabledFlag3(Enum):
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
                DataMailLinkTrackingEnabledFlag3._member_map_.values(),
            )
        )


@JsonMap({"id_": "id"})
class PartiesTo1(BaseModel):
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
class PartiesFrom1(BaseModel):
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


@JsonMap({"from_": "from"})
class DataParties1(BaseModel):
    """Parties of the mail thread

    :param to: Recipients of the mail thread, defaults to None
    :type to: List[PartiesTo1], optional
    :param from_: Senders of the mail thread, defaults to None
    :type from_: List[PartiesFrom1], optional
    """

    def __init__(self, to: List[PartiesTo1] = None, from_: List[PartiesFrom1] = None):
        if to is not None:
            self.to = self._define_list(to, PartiesTo1)
        if from_ is not None:
            self.from_ = self._define_list(from_, PartiesFrom1)


class DataHasDraftFlag1(Enum):
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
        return list(map(lambda x: x.value, DataHasDraftFlag1._member_map_.values()))


class DataHasSentFlag1(Enum):
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
        return list(map(lambda x: x.value, DataHasSentFlag1._member_map_.values()))


class DataArchivedFlag1(Enum):
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
        return list(map(lambda x: x.value, DataArchivedFlag1._member_map_.values()))


class DataSharedFlag1(Enum):
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
        return list(map(lambda x: x.value, DataSharedFlag1._member_map_.values()))


class DataExternalDeletedFlag1(Enum):
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
            map(lambda x: x.value, DataExternalDeletedFlag1._member_map_.values())
        )


class DataFirstMessageToMeFlag1(Enum):
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
            map(lambda x: x.value, DataFirstMessageToMeFlag1._member_map_.values())
        )


class DataAllMessagesSentFlag1(Enum):
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
            map(lambda x: x.value, DataAllMessagesSentFlag1._member_map_.values())
        )


@JsonMap({"id_": "id"})
class GetMailThreadsOkResponseData(BaseModel):
    """GetMailThreadsOkResponseData

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
    :type read_flag: DataReadFlag3, optional
    :param mail_tracking_status: Mail tracking status, defaults to None
    :type mail_tracking_status: str, optional
    :param has_attachments_flag: has_attachments_flag, defaults to None
    :type has_attachments_flag: DataHasAttachmentsFlag3, optional
    :param has_inline_attachments_flag: has_inline_attachments_flag, defaults to None
    :type has_inline_attachments_flag: DataHasInlineAttachmentsFlag3, optional
    :param has_real_attachments_flag: has_real_attachments_flag, defaults to None
    :type has_real_attachments_flag: DataHasRealAttachmentsFlag3, optional
    :param deleted_flag: deleted_flag, defaults to None
    :type deleted_flag: DataDeletedFlag8, optional
    :param synced_flag: synced_flag, defaults to None
    :type synced_flag: DataSyncedFlag3, optional
    :param smart_bcc_flag: smart_bcc_flag, defaults to None
    :type smart_bcc_flag: DataSmartBccFlag3, optional
    :param mail_link_tracking_enabled_flag: mail_link_tracking_enabled_flag, defaults to None
    :type mail_link_tracking_enabled_flag: DataMailLinkTrackingEnabledFlag3, optional
    :param parties: Parties of the mail thread, defaults to None
    :type parties: DataParties1, optional
    :param drafts_parties: Parties of the drafted mail thread, defaults to None
    :type drafts_parties: List[dict], optional
    :param folders: Folders in which messages from thread are being stored, defaults to None
    :type folders: List[str], optional
    :param version: Version, defaults to None
    :type version: float, optional
    :param snippet_draft: A snippet from a draft, defaults to None
    :type snippet_draft: str, optional
    :param snippet_sent: A snippet from a message sent, defaults to None
    :type snippet_sent: str, optional
    :param message_count: An amount of messages, defaults to None
    :type message_count: int, optional
    :param has_draft_flag: has_draft_flag, defaults to None
    :type has_draft_flag: DataHasDraftFlag1, optional
    :param has_sent_flag: has_sent_flag, defaults to None
    :type has_sent_flag: DataHasSentFlag1, optional
    :param archived_flag: archived_flag, defaults to None
    :type archived_flag: DataArchivedFlag1, optional
    :param shared_flag: shared_flag, defaults to None
    :type shared_flag: DataSharedFlag1, optional
    :param external_deleted_flag: external_deleted_flag, defaults to None
    :type external_deleted_flag: DataExternalDeletedFlag1, optional
    :param first_message_to_me_flag: first_message_to_me_flag, defaults to None
    :type first_message_to_me_flag: DataFirstMessageToMeFlag1, optional
    :param last_message_timestamp: Last message timestamp, defaults to None
    :type last_message_timestamp: str, optional
    :param first_message_timestamp: The time when the mail thread has had the first message received or created, defaults to None
    :type first_message_timestamp: str, optional
    :param last_message_sent_timestamp: The last time when the mail thread has had a message sent, defaults to None
    :type last_message_sent_timestamp: str, optional
    :param last_message_received_timestamp: The last time when the mail thread has had a message received, defaults to None
    :type last_message_received_timestamp: str, optional
    :param add_time: The time when the mail thread was inserted to database, defaults to None
    :type add_time: str, optional
    :param update_time: The time when the mail thread was updated in database received, defaults to None
    :type update_time: str, optional
    :param deal_id: The ID of the deal, defaults to None
    :type deal_id: int, optional
    :param deal_status: Status of the deal, defaults to None
    :type deal_status: str, optional
    :param lead_id: The ID of the lead, defaults to None
    :type lead_id: str, optional
    :param all_messages_sent_flag: all_messages_sent_flag, defaults to None
    :type all_messages_sent_flag: DataAllMessagesSentFlag1, optional
    """

    def __init__(
        self,
        id_: int = None,
        account_id: str = None,
        user_id: int = None,
        subject: str = None,
        snippet: str = None,
        read_flag: DataReadFlag3 = None,
        mail_tracking_status: str = None,
        has_attachments_flag: DataHasAttachmentsFlag3 = None,
        has_inline_attachments_flag: DataHasInlineAttachmentsFlag3 = None,
        has_real_attachments_flag: DataHasRealAttachmentsFlag3 = None,
        deleted_flag: DataDeletedFlag8 = None,
        synced_flag: DataSyncedFlag3 = None,
        smart_bcc_flag: DataSmartBccFlag3 = None,
        mail_link_tracking_enabled_flag: DataMailLinkTrackingEnabledFlag3 = None,
        parties: DataParties1 = None,
        drafts_parties: List[dict] = None,
        folders: List[str] = None,
        version: float = None,
        snippet_draft: str = None,
        snippet_sent: str = None,
        message_count: int = None,
        has_draft_flag: DataHasDraftFlag1 = None,
        has_sent_flag: DataHasSentFlag1 = None,
        archived_flag: DataArchivedFlag1 = None,
        shared_flag: DataSharedFlag1 = None,
        external_deleted_flag: DataExternalDeletedFlag1 = None,
        first_message_to_me_flag: DataFirstMessageToMeFlag1 = None,
        last_message_timestamp: str = None,
        first_message_timestamp: str = None,
        last_message_sent_timestamp: str = None,
        last_message_received_timestamp: str = None,
        add_time: str = None,
        update_time: str = None,
        deal_id: int = None,
        deal_status: str = None,
        lead_id: str = None,
        all_messages_sent_flag: DataAllMessagesSentFlag1 = None,
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
                read_flag, DataReadFlag3.list(), "read_flag"
            )
        if mail_tracking_status is not None:
            self.mail_tracking_status = mail_tracking_status
        if has_attachments_flag is not None:
            self.has_attachments_flag = self._enum_matching(
                has_attachments_flag,
                DataHasAttachmentsFlag3.list(),
                "has_attachments_flag",
            )
        if has_inline_attachments_flag is not None:
            self.has_inline_attachments_flag = self._enum_matching(
                has_inline_attachments_flag,
                DataHasInlineAttachmentsFlag3.list(),
                "has_inline_attachments_flag",
            )
        if has_real_attachments_flag is not None:
            self.has_real_attachments_flag = self._enum_matching(
                has_real_attachments_flag,
                DataHasRealAttachmentsFlag3.list(),
                "has_real_attachments_flag",
            )
        if deleted_flag is not None:
            self.deleted_flag = self._enum_matching(
                deleted_flag, DataDeletedFlag8.list(), "deleted_flag"
            )
        if synced_flag is not None:
            self.synced_flag = self._enum_matching(
                synced_flag, DataSyncedFlag3.list(), "synced_flag"
            )
        if smart_bcc_flag is not None:
            self.smart_bcc_flag = self._enum_matching(
                smart_bcc_flag, DataSmartBccFlag3.list(), "smart_bcc_flag"
            )
        if mail_link_tracking_enabled_flag is not None:
            self.mail_link_tracking_enabled_flag = self._enum_matching(
                mail_link_tracking_enabled_flag,
                DataMailLinkTrackingEnabledFlag3.list(),
                "mail_link_tracking_enabled_flag",
            )
        if parties is not None:
            self.parties = self._define_object(parties, DataParties1)
        if drafts_parties is not None:
            self.drafts_parties = drafts_parties
        if folders is not None:
            self.folders = folders
        if version is not None:
            self.version = version
        if snippet_draft is not None:
            self.snippet_draft = snippet_draft
        if snippet_sent is not None:
            self.snippet_sent = snippet_sent
        if message_count is not None:
            self.message_count = message_count
        if has_draft_flag is not None:
            self.has_draft_flag = self._enum_matching(
                has_draft_flag, DataHasDraftFlag1.list(), "has_draft_flag"
            )
        if has_sent_flag is not None:
            self.has_sent_flag = self._enum_matching(
                has_sent_flag, DataHasSentFlag1.list(), "has_sent_flag"
            )
        if archived_flag is not None:
            self.archived_flag = self._enum_matching(
                archived_flag, DataArchivedFlag1.list(), "archived_flag"
            )
        if shared_flag is not None:
            self.shared_flag = self._enum_matching(
                shared_flag, DataSharedFlag1.list(), "shared_flag"
            )
        if external_deleted_flag is not None:
            self.external_deleted_flag = self._enum_matching(
                external_deleted_flag,
                DataExternalDeletedFlag1.list(),
                "external_deleted_flag",
            )
        if first_message_to_me_flag is not None:
            self.first_message_to_me_flag = self._enum_matching(
                first_message_to_me_flag,
                DataFirstMessageToMeFlag1.list(),
                "first_message_to_me_flag",
            )
        if last_message_timestamp is not None:
            self.last_message_timestamp = last_message_timestamp
        if first_message_timestamp is not None:
            self.first_message_timestamp = first_message_timestamp
        if last_message_sent_timestamp is not None:
            self.last_message_sent_timestamp = last_message_sent_timestamp
        if last_message_received_timestamp is not None:
            self.last_message_received_timestamp = last_message_received_timestamp
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if deal_id is not None:
            self.deal_id = deal_id
        if deal_status is not None:
            self.deal_status = deal_status
        if lead_id is not None:
            self.lead_id = lead_id
        if all_messages_sent_flag is not None:
            self.all_messages_sent_flag = self._enum_matching(
                all_messages_sent_flag,
                DataAllMessagesSentFlag1.list(),
                "all_messages_sent_flag",
            )


@JsonMap({})
class GetMailThreadsOkResponse(BaseModel):
    """GetMailThreadsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of mail threads, defaults to None
    :type data: List[GetMailThreadsOkResponseData], optional
    """

    def __init__(
        self, success: bool = None, data: List[GetMailThreadsOkResponseData] = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetMailThreadsOkResponseData)
