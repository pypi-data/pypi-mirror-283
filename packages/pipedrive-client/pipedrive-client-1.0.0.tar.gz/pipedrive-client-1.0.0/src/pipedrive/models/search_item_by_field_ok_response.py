from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id", "field_key": "$field_key"})
class SearchItemByFieldOkResponseData(BaseModel):
    """SearchItemByFieldOkResponseData

    :param id_: The ID of the item, defaults to None
    :type id_: int, optional
    :param field_key: The value of the searched `field_key`, defaults to None
    :type field_key: any, optional
    """

    def __init__(self, id_: int = None, field_key: any = None):
        if id_ is not None:
            self.id_ = id_
        if field_key is not None:
            self.field_key = field_key


@JsonMap({})
class AdditionalDataPagination7(BaseModel):
    """Pagination details of the list

    :param start: Pagination start, defaults to None
    :type start: int, optional
    :param limit: Items shown per page, defaults to None
    :type limit: int, optional
    :param more_items_in_collection: Whether there are more list items in the collection than displayed, defaults to None
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
class SearchItemByFieldOkResponseAdditionalData(BaseModel):
    """SearchItemByFieldOkResponseAdditionalData

    :param pagination: Pagination details of the list, defaults to None
    :type pagination: AdditionalDataPagination7, optional
    """

    def __init__(self, pagination: AdditionalDataPagination7 = None):
        if pagination is not None:
            self.pagination = self._define_object(pagination, AdditionalDataPagination7)


@JsonMap({})
class SearchItemByFieldOkResponse(BaseModel):
    """SearchItemByFieldOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of results, defaults to None
    :type data: List[SearchItemByFieldOkResponseData], optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: SearchItemByFieldOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[SearchItemByFieldOkResponseData] = None,
        additional_data: SearchItemByFieldOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, SearchItemByFieldOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, SearchItemByFieldOkResponseAdditionalData
            )
