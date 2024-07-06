from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteDealsOkResponseData(BaseModel):
    """DeleteDealsOkResponseData

    :param id_: The list of deleted deals IDs, defaults to None
    :type id_: List[int], optional
    """

    def __init__(self, id_: List[int] = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteDealsOkResponse(BaseModel):
    """DeleteDealsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteDealsOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: DeleteDealsOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteDealsOkResponseData)
