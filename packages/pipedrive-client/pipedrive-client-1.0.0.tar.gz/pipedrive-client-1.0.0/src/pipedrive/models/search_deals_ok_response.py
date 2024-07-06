from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class ItemOwner1(BaseModel):
    """ItemOwner1

    :param id_: The ID of the owner of the deal, defaults to None
    :type id_: int, optional
    """

    def __init__(self, id_: int = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({"id_": "id"})
class ItemStage(BaseModel):
    """ItemStage

    :param id_: The ID of the stage of the deal, defaults to None
    :type id_: int, optional
    :param name: The name of the stage of the deal, defaults to None
    :type name: str, optional
    """

    def __init__(self, id_: int = None, name: str = None):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name


@JsonMap({"id_": "id"})
class ItemPerson1(BaseModel):
    """ItemPerson1

    :param id_: The ID of the person the deal is associated with, defaults to None
    :type id_: int, optional
    :param name: The name of the person the deal is associated with, defaults to None
    :type name: str, optional
    """

    def __init__(self, id_: int = None, name: str = None):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name


@JsonMap({"id_": "id"})
class ItemOrganization1(BaseModel):
    """ItemOrganization1

    :param id_: The ID of the organization the deal is associated with, defaults to None
    :type id_: int, optional
    :param name: The name of the organization the deal is associated with, defaults to None
    :type name: str, optional
    """

    def __init__(self, id_: int = None, name: str = None):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name


@JsonMap({"id_": "id", "type_": "type"})
class ItemsItem1(BaseModel):
    """ItemsItem1

    :param id_: The ID of the deal, defaults to None
    :type id_: int, optional
    :param type_: The type of the item, defaults to None
    :type type_: str, optional
    :param title: The title of the deal, defaults to None
    :type title: str, optional
    :param value: The value of the deal, defaults to None
    :type value: int, optional
    :param currency: The currency of the deal, defaults to None
    :type currency: str, optional
    :param status: The status of the deal, defaults to None
    :type status: str, optional
    :param visible_to: The visibility of the deal, defaults to None
    :type visible_to: int, optional
    :param owner: owner, defaults to None
    :type owner: ItemOwner1, optional
    :param stage: stage, defaults to None
    :type stage: ItemStage, optional
    :param person: person, defaults to None
    :type person: ItemPerson1, optional
    :param organization: organization, defaults to None
    :type organization: ItemOrganization1, optional
    :param custom_fields: Custom fields, defaults to None
    :type custom_fields: List[str], optional
    :param notes: An array of notes, defaults to None
    :type notes: List[str], optional
    """

    def __init__(
        self,
        id_: int = None,
        type_: str = None,
        title: str = None,
        value: int = None,
        currency: str = None,
        status: str = None,
        visible_to: int = None,
        owner: ItemOwner1 = None,
        stage: ItemStage = None,
        person: ItemPerson1 = None,
        organization: ItemOrganization1 = None,
        custom_fields: List[str] = None,
        notes: List[str] = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if type_ is not None:
            self.type_ = type_
        if title is not None:
            self.title = title
        if value is not None:
            self.value = value
        if currency is not None:
            self.currency = currency
        if status is not None:
            self.status = status
        if visible_to is not None:
            self.visible_to = visible_to
        if owner is not None:
            self.owner = self._define_object(owner, ItemOwner1)
        if stage is not None:
            self.stage = self._define_object(stage, ItemStage)
        if person is not None:
            self.person = self._define_object(person, ItemPerson1)
        if organization is not None:
            self.organization = self._define_object(organization, ItemOrganization1)
        if custom_fields is not None:
            self.custom_fields = custom_fields
        if notes is not None:
            self.notes = notes


@JsonMap({})
class DataItems1(BaseModel):
    """DataItems1

    :param result_score: Search result relevancy, defaults to None
    :type result_score: float, optional
    :param item: item, defaults to None
    :type item: ItemsItem1, optional
    """

    def __init__(self, result_score: float = None, item: ItemsItem1 = None):
        if result_score is not None:
            self.result_score = result_score
        if item is not None:
            self.item = self._define_object(item, ItemsItem1)


@JsonMap({})
class SearchDealsOkResponseData(BaseModel):
    """SearchDealsOkResponseData

    :param items: The array of deals, defaults to None
    :type items: List[DataItems1], optional
    """

    def __init__(self, items: List[DataItems1] = None):
        if items is not None:
            self.items = self._define_list(items, DataItems1)


@JsonMap({})
class AdditionalDataPagination3(BaseModel):
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
class SearchDealsOkResponseAdditionalData(BaseModel):
    """SearchDealsOkResponseAdditionalData

    :param pagination: Pagination details of the list, defaults to None
    :type pagination: AdditionalDataPagination3, optional
    """

    def __init__(self, pagination: AdditionalDataPagination3 = None):
        if pagination is not None:
            self.pagination = self._define_object(pagination, AdditionalDataPagination3)


@JsonMap({})
class SearchDealsOkResponse(BaseModel):
    """SearchDealsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: SearchDealsOkResponseData, optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: SearchDealsOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: SearchDealsOkResponseData = None,
        additional_data: SearchDealsOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, SearchDealsOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, SearchDealsOkResponseAdditionalData
            )
