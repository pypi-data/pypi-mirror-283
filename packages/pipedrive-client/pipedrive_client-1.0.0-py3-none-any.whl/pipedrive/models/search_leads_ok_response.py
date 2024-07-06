from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class ItemOwner2(BaseModel):
    """ItemOwner2

    :param id_: The ID of the owner of the lead, defaults to None
    :type id_: int, optional
    """

    def __init__(self, id_: int = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({"id_": "id"})
class ItemPerson2(BaseModel):
    """ItemPerson2

    :param id_: The ID of the person the lead is associated with, defaults to None
    :type id_: int, optional
    :param name: The name of the person the lead is associated with, defaults to None
    :type name: str, optional
    """

    def __init__(self, id_: int = None, name: str = None):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name


@JsonMap({"id_": "id"})
class ItemOrganization2(BaseModel):
    """ItemOrganization2

    :param id_: The ID of the organization the lead is associated with, defaults to None
    :type id_: int, optional
    :param name: The name of the organization the lead is associated with, defaults to None
    :type name: str, optional
    """

    def __init__(self, id_: int = None, name: str = None):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name


@JsonMap({"id_": "id", "type_": "type"})
class ItemsItem2(BaseModel):
    """ItemsItem2

    :param id_: The ID of the lead, defaults to None
    :type id_: str, optional
    :param type_: The type of the item, defaults to None
    :type type_: str, optional
    :param title: The title of the lead, defaults to None
    :type title: str, optional
    :param owner: owner, defaults to None
    :type owner: ItemOwner2, optional
    :param person: person, defaults to None
    :type person: ItemPerson2, optional
    :param organization: organization, defaults to None
    :type organization: ItemOrganization2, optional
    :param phones: phones, defaults to None
    :type phones: List[str], optional
    :param emails: emails, defaults to None
    :type emails: List[str], optional
    :param custom_fields: Custom fields, defaults to None
    :type custom_fields: List[str], optional
    :param notes: An array of notes, defaults to None
    :type notes: List[str], optional
    :param value: The value of the lead, defaults to None
    :type value: int, optional
    :param currency: The currency of the lead, defaults to None
    :type currency: str, optional
    :param visible_to: The visibility of the lead, defaults to None
    :type visible_to: int, optional
    :param is_archived: A flag indicating whether the lead is archived or not, defaults to None
    :type is_archived: bool, optional
    """

    def __init__(
        self,
        id_: str = None,
        type_: str = None,
        title: str = None,
        owner: ItemOwner2 = None,
        person: ItemPerson2 = None,
        organization: ItemOrganization2 = None,
        phones: List[str] = None,
        emails: List[str] = None,
        custom_fields: List[str] = None,
        notes: List[str] = None,
        value: int = None,
        currency: str = None,
        visible_to: int = None,
        is_archived: bool = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if type_ is not None:
            self.type_ = type_
        if title is not None:
            self.title = title
        if owner is not None:
            self.owner = self._define_object(owner, ItemOwner2)
        if person is not None:
            self.person = self._define_object(person, ItemPerson2)
        if organization is not None:
            self.organization = self._define_object(organization, ItemOrganization2)
        if phones is not None:
            self.phones = phones
        if emails is not None:
            self.emails = emails
        if custom_fields is not None:
            self.custom_fields = custom_fields
        if notes is not None:
            self.notes = notes
        if value is not None:
            self.value = value
        if currency is not None:
            self.currency = currency
        if visible_to is not None:
            self.visible_to = visible_to
        if is_archived is not None:
            self.is_archived = is_archived


@JsonMap({})
class DataItems3(BaseModel):
    """DataItems3

    :param result_score: Search result relevancy, defaults to None
    :type result_score: float, optional
    :param item: item, defaults to None
    :type item: ItemsItem2, optional
    """

    def __init__(self, result_score: float = None, item: ItemsItem2 = None):
        if result_score is not None:
            self.result_score = result_score
        if item is not None:
            self.item = self._define_object(item, ItemsItem2)


@JsonMap({})
class SearchLeadsOkResponseData(BaseModel):
    """SearchLeadsOkResponseData

    :param items: The array of leads, defaults to None
    :type items: List[DataItems3], optional
    """

    def __init__(self, items: List[DataItems3] = None):
        if items is not None:
            self.items = self._define_list(items, DataItems3)


@JsonMap({})
class AdditionalDataPagination8(BaseModel):
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
class SearchLeadsOkResponseAdditionalData(BaseModel):
    """SearchLeadsOkResponseAdditionalData

    :param pagination: Pagination details of the list, defaults to None
    :type pagination: AdditionalDataPagination8, optional
    """

    def __init__(self, pagination: AdditionalDataPagination8 = None):
        if pagination is not None:
            self.pagination = self._define_object(pagination, AdditionalDataPagination8)


@JsonMap({})
class SearchLeadsOkResponse(BaseModel):
    """SearchLeadsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: SearchLeadsOkResponseData, optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: SearchLeadsOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: SearchLeadsOkResponseData = None,
        additional_data: SearchLeadsOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, SearchLeadsOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, SearchLeadsOkResponseAdditionalData
            )
