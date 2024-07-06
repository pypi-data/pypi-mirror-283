from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteActivitiesOkResponseData(BaseModel):
    """DeleteActivitiesOkResponseData

    :param id_: An array of the IDs of activities that were deleted, defaults to None
    :type id_: List[int], optional
    """

    def __init__(self, id_: List[int] = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteActivitiesOkResponse(BaseModel):
    """DeleteActivitiesOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteActivitiesOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: DeleteActivitiesOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteActivitiesOkResponseData)
