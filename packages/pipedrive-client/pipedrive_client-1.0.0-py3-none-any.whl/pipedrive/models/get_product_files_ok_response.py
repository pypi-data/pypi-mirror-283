from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class GetProductFilesOkResponseData(BaseModel):
    """The file data

    :param id_: The ID of the file, defaults to None
    :type id_: int, optional
    :param product_id: The ID of the product associated with the file, defaults to None
    :type product_id: int, optional
    :param add_time: The UTC date time when the file was uploaded. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    :param update_time: The UTC date time when the file was last updated. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type update_time: str, optional
    :param file_name: The original name of the file, defaults to None
    :type file_name: str, optional
    :param file_size: The size of the file in bytes, defaults to None
    :type file_size: int, optional
    :param active_flag: Whether the user is active or not., defaults to None
    :type active_flag: bool, optional
    :param inline_flag: Whether the file was uploaded as inline or not, defaults to None
    :type inline_flag: bool, optional
    :param remote_location: The location type to send the file to. Only googledrive is supported at the moment., defaults to None
    :type remote_location: str, optional
    :param remote_id: The ID of the remote item, defaults to None
    :type remote_id: str, optional
    :param s3_bucket: The location of the cloud storage, defaults to None
    :type s3_bucket: str, optional
    :param product_name: The name of the product associated with the file, defaults to None
    :type product_name: str, optional
    :param url: The URL to download the file, defaults to None
    :type url: str, optional
    :param name: The visible name of the file, defaults to None
    :type name: str, optional
    :param description: The description of the file, defaults to None
    :type description: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        product_id: int = None,
        add_time: str = None,
        update_time: str = None,
        file_name: str = None,
        file_size: int = None,
        active_flag: bool = None,
        inline_flag: bool = None,
        remote_location: str = None,
        remote_id: str = None,
        s3_bucket: str = None,
        product_name: str = None,
        url: str = None,
        name: str = None,
        description: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if product_id is not None:
            self.product_id = product_id
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
        if s3_bucket is not None:
            self.s3_bucket = s3_bucket
        if product_name is not None:
            self.product_name = product_name
        if url is not None:
            self.url = url
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description


@JsonMap({})
class GetProductFilesOkResponseAdditionalData(BaseModel):
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
class GetProductFilesOkResponse(BaseModel):
    """GetProductFilesOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of files, defaults to None
    :type data: List[GetProductFilesOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetProductFilesOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetProductFilesOkResponseData] = None,
        additional_data: GetProductFilesOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetProductFilesOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetProductFilesOkResponseAdditionalData
            )
