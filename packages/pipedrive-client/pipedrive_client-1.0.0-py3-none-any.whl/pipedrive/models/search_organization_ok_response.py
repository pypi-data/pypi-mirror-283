from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class ItemOwner3(BaseModel):
    """ItemOwner3

    :param id_: The ID of the owner of the deal, defaults to None
    :type id_: int, optional
    """

    def __init__(self, id_: int = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({"id_": "id", "type_": "type"})
class ItemsItem3(BaseModel):
    """ItemsItem3

    :param id_: The ID of the organization, defaults to None
    :type id_: int, optional
    :param type_: The type of the item, defaults to None
    :type type_: str, optional
    :param name: The name of the organization, defaults to None
    :type name: str, optional
    :param address: The address of the organization, defaults to None
    :type address: str, optional
    :param visible_to: The visibility of the organization, defaults to None
    :type visible_to: int, optional
    :param owner: owner, defaults to None
    :type owner: ItemOwner3, optional
    :param custom_fields: Custom fields, defaults to None
    :type custom_fields: List[str], optional
    :param notes: An array of notes, defaults to None
    :type notes: List[str], optional
    """

    def __init__(
        self,
        id_: int = None,
        type_: str = None,
        name: str = None,
        address: str = None,
        visible_to: int = None,
        owner: ItemOwner3 = None,
        custom_fields: List[str] = None,
        notes: List[str] = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if type_ is not None:
            self.type_ = type_
        if name is not None:
            self.name = name
        if address is not None:
            self.address = address
        if visible_to is not None:
            self.visible_to = visible_to
        if owner is not None:
            self.owner = self._define_object(owner, ItemOwner3)
        if custom_fields is not None:
            self.custom_fields = custom_fields
        if notes is not None:
            self.notes = notes


@JsonMap({})
class DataItems4(BaseModel):
    """DataItems4

    :param result_score: Search result relevancy, defaults to None
    :type result_score: float, optional
    :param item: item, defaults to None
    :type item: ItemsItem3, optional
    """

    def __init__(self, result_score: float = None, item: ItemsItem3 = None):
        if result_score is not None:
            self.result_score = result_score
        if item is not None:
            self.item = self._define_object(item, ItemsItem3)


@JsonMap({})
class SearchOrganizationOkResponseData(BaseModel):
    """SearchOrganizationOkResponseData

    :param items: The array of found items, defaults to None
    :type items: List[DataItems4], optional
    """

    def __init__(self, items: List[DataItems4] = None):
        if items is not None:
            self.items = self._define_list(items, DataItems4)


@JsonMap({})
class AdditionalDataPagination12(BaseModel):
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
class SearchOrganizationOkResponseAdditionalData(BaseModel):
    """SearchOrganizationOkResponseAdditionalData

    :param pagination: Pagination details of the list, defaults to None
    :type pagination: AdditionalDataPagination12, optional
    """

    def __init__(self, pagination: AdditionalDataPagination12 = None):
        if pagination is not None:
            self.pagination = self._define_object(
                pagination, AdditionalDataPagination12
            )


@JsonMap({})
class SearchOrganizationOkResponse(BaseModel):
    """SearchOrganizationOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: SearchOrganizationOkResponseData, optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: SearchOrganizationOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: SearchOrganizationOkResponseData = None,
        additional_data: SearchOrganizationOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, SearchOrganizationOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, SearchOrganizationOkResponseAdditionalData
            )
