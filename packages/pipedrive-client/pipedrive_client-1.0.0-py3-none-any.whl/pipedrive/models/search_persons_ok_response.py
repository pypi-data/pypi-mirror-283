from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class ItemOwner4(BaseModel):
    """ItemOwner4

    :param id_: The ID of the owner of the person, defaults to None
    :type id_: int, optional
    """

    def __init__(self, id_: int = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({"id_": "id"})
class ItemOrganization3(BaseModel):
    """ItemOrganization3

    :param id_: The ID of the organization the person is associated with, defaults to None
    :type id_: int, optional
    :param name: The name of the organization the person is associated with, defaults to None
    :type name: str, optional
    """

    def __init__(self, id_: int = None, name: str = None):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name


@JsonMap({"id_": "id", "type_": "type"})
class ItemsItem4(BaseModel):
    """ItemsItem4

    :param id_: The ID of the person, defaults to None
    :type id_: int, optional
    :param type_: The type of the item, defaults to None
    :type type_: str, optional
    :param name: The name of the person, defaults to None
    :type name: str, optional
    :param phones: An array of phone numbers, defaults to None
    :type phones: List[str], optional
    :param emails: An array of email addresses, defaults to None
    :type emails: List[str], optional
    :param visible_to: The visibility of the person, defaults to None
    :type visible_to: int, optional
    :param owner: owner, defaults to None
    :type owner: ItemOwner4, optional
    :param organization: organization, defaults to None
    :type organization: ItemOrganization3, optional
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
        phones: List[str] = None,
        emails: List[str] = None,
        visible_to: int = None,
        owner: ItemOwner4 = None,
        organization: ItemOrganization3 = None,
        custom_fields: List[str] = None,
        notes: List[str] = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if type_ is not None:
            self.type_ = type_
        if name is not None:
            self.name = name
        if phones is not None:
            self.phones = phones
        if emails is not None:
            self.emails = emails
        if visible_to is not None:
            self.visible_to = visible_to
        if owner is not None:
            self.owner = self._define_object(owner, ItemOwner4)
        if organization is not None:
            self.organization = self._define_object(organization, ItemOrganization3)
        if custom_fields is not None:
            self.custom_fields = custom_fields
        if notes is not None:
            self.notes = notes


@JsonMap({})
class DataItems5(BaseModel):
    """DataItems5

    :param result_score: Search result relevancy, defaults to None
    :type result_score: float, optional
    :param item: item, defaults to None
    :type item: ItemsItem4, optional
    """

    def __init__(self, result_score: float = None, item: ItemsItem4 = None):
        if result_score is not None:
            self.result_score = result_score
        if item is not None:
            self.item = self._define_object(item, ItemsItem4)


@JsonMap({})
class SearchPersonsOkResponseData(BaseModel):
    """SearchPersonsOkResponseData

    :param items: The array of found items, defaults to None
    :type items: List[DataItems5], optional
    """

    def __init__(self, items: List[DataItems5] = None):
        if items is not None:
            self.items = self._define_list(items, DataItems5)


@JsonMap({})
class AdditionalDataPagination15(BaseModel):
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
class SearchPersonsOkResponseAdditionalData(BaseModel):
    """SearchPersonsOkResponseAdditionalData

    :param pagination: Pagination details of the list, defaults to None
    :type pagination: AdditionalDataPagination15, optional
    """

    def __init__(self, pagination: AdditionalDataPagination15 = None):
        if pagination is not None:
            self.pagination = self._define_object(
                pagination, AdditionalDataPagination15
            )


@JsonMap({})
class SearchPersonsOkResponse(BaseModel):
    """SearchPersonsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: SearchPersonsOkResponseData, optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: SearchPersonsOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: SearchPersonsOkResponseData = None,
        additional_data: SearchPersonsOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, SearchPersonsOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, SearchPersonsOkResponseAdditionalData
            )
