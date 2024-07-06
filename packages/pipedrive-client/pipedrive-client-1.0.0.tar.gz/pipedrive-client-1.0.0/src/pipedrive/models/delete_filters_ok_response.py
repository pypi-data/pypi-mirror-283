from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteFiltersOkResponseData(BaseModel):
    """DeleteFiltersOkResponseData

    :param id_: The array of the IDs of the deleted filter, defaults to None
    :type id_: List[int], optional
    """

    def __init__(self, id_: List[int] = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteFiltersOkResponse(BaseModel):
    """DeleteFiltersOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteFiltersOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: DeleteFiltersOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteFiltersOkResponseData)
