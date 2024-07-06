from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class AddDealFollowerOkResponseData(BaseModel):
    """AddDealFollowerOkResponseData

    :param user_id: The user ID who added the follower, defaults to None
    :type user_id: int, optional
    :param id_: The follower ID, defaults to None
    :type id_: int, optional
    :param deal_id: The ID of the deal which the follower was added to, defaults to None
    :type deal_id: int, optional
    :param add_time: The date and time when the deal follower was added, defaults to None
    :type add_time: str, optional
    """

    def __init__(
        self,
        user_id: int = None,
        id_: int = None,
        deal_id: int = None,
        add_time: str = None,
    ):
        if user_id is not None:
            self.user_id = user_id
        if id_ is not None:
            self.id_ = id_
        if deal_id is not None:
            self.deal_id = deal_id
        if add_time is not None:
            self.add_time = add_time


@JsonMap({})
class AddDealFollowerOkResponse(BaseModel):
    """AddDealFollowerOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: AddDealFollowerOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: AddDealFollowerOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, AddDealFollowerOkResponseData)
