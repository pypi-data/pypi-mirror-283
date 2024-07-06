from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteDealOkResponseData(BaseModel):
    """DeleteDealOkResponseData

    :param id_: The ID of the deal that was deleted, defaults to None
    :type id_: int, optional
    """

    def __init__(self, id_: int = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteDealOkResponse(BaseModel):
    """DeleteDealOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteDealOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: DeleteDealOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteDealOkResponseData)
