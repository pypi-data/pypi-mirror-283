from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class AddProductFollowerCreatedResponseData(BaseModel):
    """AddProductFollowerCreatedResponseData

    :param user_id: The ID of the user that was added as follower, defaults to None
    :type user_id: int, optional
    :param id_: The ID of the follower, defaults to None
    :type id_: int, optional
    :param product_id: The ID of the product, defaults to None
    :type product_id: int, optional
    :param add_time: The follower creation time. Format: YYYY-MM-DD HH:MM:SS, defaults to None
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
class AddProductFollowerCreatedResponse(BaseModel):
    """AddProductFollowerCreatedResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: AddProductFollowerCreatedResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: AddProductFollowerCreatedResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, AddProductFollowerCreatedResponseData)
