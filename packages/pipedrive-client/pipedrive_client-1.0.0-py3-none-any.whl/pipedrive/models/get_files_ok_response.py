from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class GetFilesOkResponseData(BaseModel):
    """The file data

    :param id_: The ID of the file, defaults to None
    :type id_: int, optional
    :param user_id: The ID of the user to associate the file with, defaults to None
    :type user_id: int, optional
    :param deal_id: The ID of the deal to associate the file with, defaults to None
    :type deal_id: int, optional
    :param person_id: The ID of the person to associate the file with, defaults to None
    :type person_id: int, optional
    :param org_id: The ID of the organization to associate the file with, defaults to None
    :type org_id: int, optional
    :param product_id: The ID of the product to associate the file with, defaults to None
    :type product_id: int, optional
    :param activity_id: The ID of the activity to associate the file with, defaults to None
    :type activity_id: int, optional
    :param lead_id: The ID of the lead to associate the file with, defaults to None
    :type lead_id: str, optional
    :param add_time: The date and time when the file was added/created. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    :param update_time: The last updated date and time of the file. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type update_time: str, optional
    :param file_name: The original name of the file, defaults to None
    :type file_name: str, optional
    :param file_size: The size of the file, defaults to None
    :type file_size: int, optional
    :param active_flag: Whether the user is active or not. false = Not activated, true = Activated, defaults to None
    :type active_flag: bool, optional
    :param inline_flag: Whether the file was uploaded as inline or not, defaults to None
    :type inline_flag: bool, optional
    :param remote_location: The location type to send the file to. Only googledrive is supported at the moment., defaults to None
    :type remote_location: str, optional
    :param remote_id: The ID of the remote item, defaults to None
    :type remote_id: str, optional
    :param cid: The ID of the inline attachment, defaults to None
    :type cid: str, optional
    :param s3_bucket: The location of the cloud storage, defaults to None
    :type s3_bucket: str, optional
    :param mail_message_id: The ID of the mail message to associate the file with, defaults to None
    :type mail_message_id: str, optional
    :param mail_template_id: The ID of the mail template to associate the file with, defaults to None
    :type mail_template_id: str, optional
    :param deal_name: The name of the deal associated with the file, defaults to None
    :type deal_name: str, optional
    :param person_name: The name of the person associated with the file, defaults to None
    :type person_name: str, optional
    :param org_name: The name of the organization associated with the file, defaults to None
    :type org_name: str, optional
    :param product_name: The name of the product associated with the file, defaults to None
    :type product_name: str, optional
    :param lead_name: The name of the lead associated with the file, defaults to None
    :type lead_name: str, optional
    :param url: The URL of the download file, defaults to None
    :type url: str, optional
    :param name: The visible name of the file, defaults to None
    :type name: str, optional
    :param description: The description of the file, defaults to None
    :type description: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        user_id: int = None,
        deal_id: int = None,
        person_id: int = None,
        org_id: int = None,
        product_id: int = None,
        activity_id: int = None,
        lead_id: str = None,
        add_time: str = None,
        update_time: str = None,
        file_name: str = None,
        file_size: int = None,
        active_flag: bool = None,
        inline_flag: bool = None,
        remote_location: str = None,
        remote_id: str = None,
        cid: str = None,
        s3_bucket: str = None,
        mail_message_id: str = None,
        mail_template_id: str = None,
        deal_name: str = None,
        person_name: str = None,
        org_name: str = None,
        product_name: str = None,
        lead_name: str = None,
        url: str = None,
        name: str = None,
        description: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if user_id is not None:
            self.user_id = user_id
        if deal_id is not None:
            self.deal_id = deal_id
        if person_id is not None:
            self.person_id = person_id
        if org_id is not None:
            self.org_id = org_id
        if product_id is not None:
            self.product_id = product_id
        if activity_id is not None:
            self.activity_id = activity_id
        if lead_id is not None:
            self.lead_id = lead_id
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if file_name is not None:
            self.file_name = file_name
        if file_size is not None:
            self.file_size = file_size
        if active_flag is not None:
            self.active_flag = active_flag
        if inline_flag is not None:
            self.inline_flag = inline_flag
        if remote_location is not None:
            self.remote_location = remote_location
        if remote_id is not None:
            self.remote_id = remote_id
        if cid is not None:
            self.cid = cid
        if s3_bucket is not None:
            self.s3_bucket = s3_bucket
        if mail_message_id is not None:
            self.mail_message_id = mail_message_id
        if mail_template_id is not None:
            self.mail_template_id = mail_template_id
        if deal_name is not None:
            self.deal_name = deal_name
        if person_name is not None:
            self.person_name = person_name
        if org_name is not None:
            self.org_name = org_name
        if product_name is not None:
            self.product_name = product_name
        if lead_name is not None:
            self.lead_name = lead_name
        if url is not None:
            self.url = url
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description


@JsonMap({})
class AdditionalDataPagination5(BaseModel):
    """AdditionalDataPagination5

    :param start: Pagination start, defaults to None
    :type start: int, optional
    :param limit: Items shown per page, defaults to None
    :type limit: int, optional
    :param more_items_in_collection: If there are more list items in the collection than displayed or not, defaults to None
    :type more_items_in_collection: bool, optional
    :param next_start: Next pagination start, defaults to None
    :type next_start: int, optional
    """

    def __init__(
        self,
        start: int = None,
        limit: int = None,
        more_items_in_collection: bool = None,
        next_start: int = None,
    ):
        if start is not None:
            self.start = start
        if limit is not None:
            self.limit = limit
        if more_items_in_collection is not None:
            self.more_items_in_collection = more_items_in_collection
        if next_start is not None:
            self.next_start = next_start


@JsonMap({})
class GetFilesOkResponseAdditionalData(BaseModel):
    """GetFilesOkResponseAdditionalData

    :param pagination: pagination, defaults to None
    :type pagination: AdditionalDataPagination5, optional
    """

    def __init__(self, pagination: AdditionalDataPagination5 = None):
        if pagination is not None:
            self.pagination = self._define_object(pagination, AdditionalDataPagination5)


@JsonMap({})
class GetFilesOkResponse(BaseModel):
    """GetFilesOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of all uploaded files, defaults to None
    :type data: List[GetFilesOkResponseData], optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: GetFilesOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetFilesOkResponseData] = None,
        additional_data: GetFilesOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetFilesOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetFilesOkResponseAdditionalData
            )
