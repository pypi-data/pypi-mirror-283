from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteDealFollowerOkResponseData(BaseModel):
    """DeleteDealFollowerOkResponseData

    :param id_: The ID of the deal follower that was deleted, defaults to None
    :type id_: int, optional
    """

    def __init__(self, id_: int = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteDealFollowerOkResponse(BaseModel):
    """DeleteDealFollowerOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteDealFollowerOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: DeleteDealFollowerOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteDealFollowerOkResponseData)
