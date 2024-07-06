from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteActivityTypesOkResponseData(BaseModel):
    """DeleteActivityTypesOkResponseData

    :param id_: The IDs of the deleted activity types, defaults to None
    :type id_: List[int], optional
    """

    def __init__(self, id_: List[int] = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteActivityTypesOkResponse(BaseModel):
    """DeleteActivityTypesOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteActivityTypesOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: DeleteActivityTypesOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteActivityTypesOkResponseData)
