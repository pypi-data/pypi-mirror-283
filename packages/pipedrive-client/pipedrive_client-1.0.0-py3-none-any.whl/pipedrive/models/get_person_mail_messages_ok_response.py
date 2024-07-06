from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DataFrom5(BaseModel):
    """DataFrom5

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
class DataTo5(BaseModel):
    """DataTo5

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
class DataCc5(BaseModel):
    """DataCc5

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
class DataBcc5(BaseModel):
    """DataBcc5

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


class DataMailTrackingStatus4(Enum):
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
            map(lambda x: x.value, DataMailTrackingStatus4._member_map_.values())
        )


class DataMailLinkTrackingEnabledFlag8(Enum):
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
                DataMailLinkTrackingEnabledFlag8._member_map_.values(),
            )
        )


class DataReadFlag8(Enum):
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
        return list(map(lambda x: x.value, DataReadFlag8._member_map_.values()))


class DataDraftFlag4(Enum):
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
        return list(map(lambda x: x.value, DataDraftFlag4._member_map_.values()))


class DataSyncedFlag8(Enum):
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
        return list(map(lambda x: x.value, DataSyncedFlag8._member_map_.values()))


class DataDeletedFlag13(Enum):
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
        return list(map(lambda x: x.value, DataDeletedFlag13._member_map_.values()))


class DataHasBodyFlag5(Enum):
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
        return list(map(lambda x: x.value, DataHasBodyFlag5._member_map_.values()))


class DataSentFlag5(Enum):
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
        return list(map(lambda x: x.value, DataSentFlag5._member_map_.values()))


class DataSentFromPipedriveFlag5(Enum):
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
            map(lambda x: x.value, DataSentFromPipedriveFlag5._member_map_.values())
        )


class DataSmartBccFlag8(Enum):
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
        return list(map(lambda x: x.value, DataSmartBccFlag8._member_map_.values()))


class DataHasAttachmentsFlag8(Enum):
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
            map(lambda x: x.value, DataHasAttachmentsFlag8._member_map_.values())
        )


class DataHasInlineAttachmentsFlag8(Enum):
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
            map(lambda x: x.value, DataHasInlineAttachmentsFlag8._member_map_.values())
        )


class DataHasRealAttachmentsFlag8(Enum):
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
            map(lambda x: x.value, DataHasRealAttachmentsFlag8._member_map_.values())
        )


@JsonMap({"id_": "id", "from_": "from"})
class DataData3(BaseModel):
    """DataData3

    :param id_: ID of the mail message., defaults to None
    :type id_: int, optional
    :param from_: The array of mail message sender (object), defaults to None
    :type from_: List[DataFrom5], optional
    :param to: The array of mail message receiver (object), defaults to None
    :type to: List[DataTo5], optional
    :param cc: The array of mail message copies (object), defaults to None
    :type cc: List[DataCc5], optional
    :param bcc: The array of mail message blind copies (object), defaults to None
    :type bcc: List[DataBcc5], optional
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
    :type mail_tracking_status: DataMailTrackingStatus4, optional
    :param mail_link_tracking_enabled_flag: mail_link_tracking_enabled_flag, defaults to None
    :type mail_link_tracking_enabled_flag: DataMailLinkTrackingEnabledFlag8, optional
    :param read_flag: read_flag, defaults to None
    :type read_flag: DataReadFlag8, optional
    :param draft: If the mail message has a draft status then the value is the mail message object as JSON formatted string, otherwise `null`., defaults to None
    :type draft: str, optional
    :param draft_flag: draft_flag, defaults to None
    :type draft_flag: DataDraftFlag4, optional
    :param synced_flag: synced_flag, defaults to None
    :type synced_flag: DataSyncedFlag8, optional
    :param deleted_flag: deleted_flag, defaults to None
    :type deleted_flag: DataDeletedFlag13, optional
    :param has_body_flag: has_body_flag, defaults to None
    :type has_body_flag: DataHasBodyFlag5, optional
    :param sent_flag: sent_flag, defaults to None
    :type sent_flag: DataSentFlag5, optional
    :param sent_from_pipedrive_flag: sent_from_pipedrive_flag, defaults to None
    :type sent_from_pipedrive_flag: DataSentFromPipedriveFlag5, optional
    :param smart_bcc_flag: smart_bcc_flag, defaults to None
    :type smart_bcc_flag: DataSmartBccFlag8, optional
    :param message_time: Creation or receival time of the mail message, defaults to None
    :type message_time: str, optional
    :param add_time: The insertion into the database time of the mail message, defaults to None
    :type add_time: str, optional
    :param update_time: The updating time in the database of the mail message, defaults to None
    :type update_time: str, optional
    :param has_attachments_flag: has_attachments_flag, defaults to None
    :type has_attachments_flag: DataHasAttachmentsFlag8, optional
    :param has_inline_attachments_flag: has_inline_attachments_flag, defaults to None
    :type has_inline_attachments_flag: DataHasInlineAttachmentsFlag8, optional
    :param has_real_attachments_flag: has_real_attachments_flag, defaults to None
    :type has_real_attachments_flag: DataHasRealAttachmentsFlag8, optional
    :param nylas_id: The Mail Message ID assigned by the sync provider, defaults to None
    :type nylas_id: str, optional
    :param s3_bucket: The name of the S3 bucket, defaults to None
    :type s3_bucket: str, optional
    :param s3_bucket_path: The path of the S3 bucket, defaults to None
    :type s3_bucket_path: str, optional
    :param external_deleted_flag: If the Mail Message has been deleted on the provider side or not, defaults to None
    :type external_deleted_flag: bool, optional
    :param mua_message_id: The Mail Message ID assigned by the mail user agent, defaults to None
    :type mua_message_id: str, optional
    :param template_id: The ID of the mail template, defaults to None
    :type template_id: int, optional
    :param timestamp: The add date and time of the Mail Message, defaults to None
    :type timestamp: str, optional
    :param item_type: The type of the data item, defaults to None
    :type item_type: str, optional
    :param company_id: The ID of the company, defaults to None
    :type company_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        from_: List[DataFrom5] = None,
        to: List[DataTo5] = None,
        cc: List[DataCc5] = None,
        bcc: List[DataBcc5] = None,
        body_url: str = None,
        account_id: str = None,
        user_id: int = None,
        mail_thread_id: int = None,
        subject: str = None,
        snippet: str = None,
        mail_tracking_status: DataMailTrackingStatus4 = None,
        mail_link_tracking_enabled_flag: DataMailLinkTrackingEnabledFlag8 = None,
        read_flag: DataReadFlag8 = None,
        draft: str = None,
        draft_flag: DataDraftFlag4 = None,
        synced_flag: DataSyncedFlag8 = None,
        deleted_flag: DataDeletedFlag13 = None,
        has_body_flag: DataHasBodyFlag5 = None,
        sent_flag: DataSentFlag5 = None,
        sent_from_pipedrive_flag: DataSentFromPipedriveFlag5 = None,
        smart_bcc_flag: DataSmartBccFlag8 = None,
        message_time: str = None,
        add_time: str = None,
        update_time: str = None,
        has_attachments_flag: DataHasAttachmentsFlag8 = None,
        has_inline_attachments_flag: DataHasInlineAttachmentsFlag8 = None,
        has_real_attachments_flag: DataHasRealAttachmentsFlag8 = None,
        nylas_id: str = None,
        s3_bucket: str = None,
        s3_bucket_path: str = None,
        external_deleted_flag: bool = None,
        mua_message_id: str = None,
        template_id: int = None,
        timestamp: str = None,
        item_type: str = None,
        company_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if from_ is not None:
            self.from_ = self._define_list(from_, DataFrom5)
        if to is not None:
            self.to = self._define_list(to, DataTo5)
        if cc is not None:
            self.cc = self._define_list(cc, DataCc5)
        if bcc is not None:
            self.bcc = self._define_list(bcc, DataBcc5)
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
                DataMailTrackingStatus4.list(),
                "mail_tracking_status",
            )
        if mail_link_tracking_enabled_flag is not None:
            self.mail_link_tracking_enabled_flag = self._enum_matching(
                mail_link_tracking_enabled_flag,
                DataMailLinkTrackingEnabledFlag8.list(),
                "mail_link_tracking_enabled_flag",
            )
        if read_flag is not None:
            self.read_flag = self._enum_matching(
                read_flag, DataReadFlag8.list(), "read_flag"
            )
        if draft is not None:
            self.draft = draft
        if draft_flag is not None:
            self.draft_flag = self._enum_matching(
                draft_flag, DataDraftFlag4.list(), "draft_flag"
            )
        if synced_flag is not None:
            self.synced_flag = self._enum_matching(
                synced_flag, DataSyncedFlag8.list(), "synced_flag"
            )
        if deleted_flag is not None:
            self.deleted_flag = self._enum_matching(
                deleted_flag, DataDeletedFlag13.list(), "deleted_flag"
            )
        if has_body_flag is not None:
            self.has_body_flag = self._enum_matching(
                has_body_flag, DataHasBodyFlag5.list(), "has_body_flag"
            )
        if sent_flag is not None:
            self.sent_flag = self._enum_matching(
                sent_flag, DataSentFlag5.list(), "sent_flag"
            )
        if sent_from_pipedrive_flag is not None:
            self.sent_from_pipedrive_flag = self._enum_matching(
                sent_from_pipedrive_flag,
                DataSentFromPipedriveFlag5.list(),
                "sent_from_pipedrive_flag",
            )
        if smart_bcc_flag is not None:
            self.smart_bcc_flag = self._enum_matching(
                smart_bcc_flag, DataSmartBccFlag8.list(), "smart_bcc_flag"
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
                DataHasAttachmentsFlag8.list(),
                "has_attachments_flag",
            )
        if has_inline_attachments_flag is not None:
            self.has_inline_attachments_flag = self._enum_matching(
                has_inline_attachments_flag,
                DataHasInlineAttachmentsFlag8.list(),
                "has_inline_attachments_flag",
            )
        if has_real_attachments_flag is not None:
            self.has_real_attachments_flag = self._enum_matching(
                has_real_attachments_flag,
                DataHasRealAttachmentsFlag8.list(),
                "has_real_attachments_flag",
            )
        if nylas_id is not None:
            self.nylas_id = nylas_id
        if s3_bucket is not None:
            self.s3_bucket = s3_bucket
        if s3_bucket_path is not None:
            self.s3_bucket_path = s3_bucket_path
        if external_deleted_flag is not None:
            self.external_deleted_flag = external_deleted_flag
        if mua_message_id is not None:
            self.mua_message_id = mua_message_id
        if template_id is not None:
            self.template_id = template_id
        if timestamp is not None:
            self.timestamp = timestamp
        if item_type is not None:
            self.item_type = item_type
        if company_id is not None:
            self.company_id = company_id


@JsonMap({})
class GetPersonMailMessagesOkResponseData(BaseModel):
    """GetPersonMailMessagesOkResponseData

    :param object: The type of the data item, defaults to None
    :type object: str, optional
    :param timestamp: The date and time when the item was created, defaults to None
    :type timestamp: str, optional
    :param data: data, defaults to None
    :type data: DataData3, optional
    """

    def __init__(
        self, object: str = None, timestamp: str = None, data: DataData3 = None
    ):
        if object is not None:
            self.object = object
        if timestamp is not None:
            self.timestamp = timestamp
        if data is not None:
            self.data = self._define_object(data, DataData3)


@JsonMap({})
class GetPersonMailMessagesOkResponseAdditionalData(BaseModel):
    """The additional data of the list

    :param start: Pagination start, defaults to None
    :type start: int, optional
    :param limit: Items shown per page, defaults to None
    :type limit: int, optional
    :param more_items_in_collection: If there are more list items in the collection than displayed or not, defaults to None
    :type more_items_in_collection: bool, optional
    """

    def __init__(
        self,
        start: int = None,
        limit: int = None,
        more_items_in_collection: bool = None,
    ):
        if start is not None:
            self.start = start
        if limit is not None:
            self.limit = limit
        if more_items_in_collection is not None:
            self.more_items_in_collection = more_items_in_collection


@JsonMap({})
class GetPersonMailMessagesOkResponse(BaseModel):
    """GetPersonMailMessagesOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of mail messages, defaults to None
    :type data: List[GetPersonMailMessagesOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetPersonMailMessagesOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetPersonMailMessagesOkResponseData] = None,
        additional_data: GetPersonMailMessagesOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetPersonMailMessagesOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetPersonMailMessagesOkResponseAdditionalData
            )
