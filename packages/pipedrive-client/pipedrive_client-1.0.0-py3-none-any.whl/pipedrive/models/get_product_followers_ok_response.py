from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class GetProductFollowersOkResponseData(BaseModel):
    """GetProductFollowersOkResponseData

    :param user_id: The ID of the user, defaults to None
    :type user_id: int, optional
    :param id_: The ID of the user follower, defaults to None
    :type id_: int, optional
    :param product_id: The ID of the product, defaults to None
    :type product_id: int, optional
    :param add_time: The date and time when the follower was added to the person, defaults to None
    :type add_time: str, optional
    """

    def __init__(
        self,
        user_id: int = None,
        id_: int = None,
        product_id: int = None,
        add_time: str = None,
    ):
        if user_id is not None:
            self.user_id = user_id
        if id_ is not None:
            self.id_ = id_
        if product_id is not None:
            self.product_id = product_id
        if add_time is not None:
            self.add_time = add_time


@JsonMap({})
class GetProductFollowersOkResponseAdditionalData(BaseModel):
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
class GetProductFollowersOkResponse(BaseModel):
    """GetProductFollowersOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The list of followers, defaults to None
    :type data: List[GetProductFollowersOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetProductFollowersOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetProductFollowersOkResponseData] = None,
        additional_data: GetProductFollowersOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetProductFollowersOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetProductFollowersOkResponseAdditionalData
            )
