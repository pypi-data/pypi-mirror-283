from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DataItems2(BaseModel):
    """DataItems2

    :param result_score: Search result relevancy, defaults to None
    :type result_score: float, optional
    :param item: Item, defaults to None
    :type item: dict, optional
    """

    def __init__(self, result_score: float = None, item: dict = None):
        if result_score is not None:
            self.result_score = result_score
        if item is not None:
            self.item = item


@JsonMap({})
class RelatedItems(BaseModel):
    """RelatedItems

    :param result_score: Search result relevancy, defaults to None
    :type result_score: float, optional
    :param item: Item, defaults to None
    :type item: dict, optional
    """

    def __init__(self, result_score: float = None, item: dict = None):
        if result_score is not None:
            self.result_score = result_score
        if item is not None:
            self.item = item


@JsonMap({})
class SearchItemOkResponseData(BaseModel):
    """SearchItemOkResponseData

    :param items: The array of found items, defaults to None
    :type items: List[DataItems2], optional
    :param related_items: The array of related items if `search_for_related_items` was enabled, defaults to None
    :type related_items: List[RelatedItems], optional
    """

    def __init__(
        self, items: List[DataItems2] = None, related_items: List[RelatedItems] = None
    ):
        if items is not None:
            self.items = self._define_list(items, DataItems2)
        if related_items is not None:
            self.related_items = self._define_list(related_items, RelatedItems)


@JsonMap({})
class AdditionalDataPagination6(BaseModel):
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
class SearchItemOkResponseAdditionalData(BaseModel):
    """SearchItemOkResponseAdditionalData

    :param pagination: Pagination details of the list, defaults to None
    :type pagination: AdditionalDataPagination6, optional
    """

    def __init__(self, pagination: AdditionalDataPagination6 = None):
        if pagination is not None:
            self.pagination = self._define_object(pagination, AdditionalDataPagination6)


@JsonMap({})
class SearchItemOkResponse(BaseModel):
    """SearchItemOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: SearchItemOkResponseData, optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: SearchItemOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: SearchItemOkResponseData = None,
        additional_data: SearchItemOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, SearchItemOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, SearchItemOkResponseAdditionalData
            )
