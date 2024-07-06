from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class GetOrganizationFollowersOkResponseData(BaseModel):
    """GetOrganizationFollowersOkResponseData

    :param org_id: The ID of the organization, defaults to None
    :type org_id: int, optional
    :param user_id: The user ID of the follower related to the item, defaults to None
    :type user_id: int, optional
    :param id_: The ID of the follower, defaults to None
    :type id_: int, optional
    :param add_time: The date and time of adding the follower to the item, defaults to None
    :type add_time: str, optional
    """

    def __init__(
        self,
        org_id: int = None,
        user_id: int = None,
        id_: int = None,
        add_time: str = None,
    ):
        if org_id is not None:
            self.org_id = org_id
        if user_id is not None:
            self.user_id = user_id
        if id_ is not None:
            self.id_ = id_
        if add_time is not None:
            self.add_time = add_time


@JsonMap({})
class AdditionalDataPagination13(BaseModel):
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
class GetOrganizationFollowersOkResponseAdditionalData(BaseModel):
    """GetOrganizationFollowersOkResponseAdditionalData

    :param pagination: Pagination details of the list, defaults to None
    :type pagination: AdditionalDataPagination13, optional
    """

    def __init__(self, pagination: AdditionalDataPagination13 = None):
        if pagination is not None:
            self.pagination = self._define_object(
                pagination, AdditionalDataPagination13
            )


@JsonMap({})
class GetOrganizationFollowersOkResponse(BaseModel):
    """GetOrganizationFollowersOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of followers, defaults to None
    :type data: List[GetOrganizationFollowersOkResponseData], optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: GetOrganizationFollowersOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetOrganizationFollowersOkResponseData] = None,
        additional_data: GetOrganizationFollowersOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetOrganizationFollowersOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetOrganizationFollowersOkResponseAdditionalData
            )
