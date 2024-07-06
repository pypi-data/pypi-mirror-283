from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteDealFieldsOkResponseData(BaseModel):
    """DeleteDealFieldsOkResponseData

    :param id_: The list of deleted field IDs, defaults to None
    :type id_: List[int], optional
    """

    def __init__(self, id_: List[int] = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteDealFieldsOkResponse(BaseModel):
    """DeleteDealFieldsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteDealFieldsOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: DeleteDealFieldsOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteDealFieldsOkResponseData)
