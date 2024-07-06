from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GetRolePipelinesOkResponseData(BaseModel):
    """The response data

    :param pipeline_ids: Either visible or hidden pipeline ids, defaults to None
    :type pipeline_ids: List[float], optional
    :param visible: Whether visible or hidden pipeline ids were returned, defaults to None
    :type visible: bool, optional
    """

    def __init__(self, pipeline_ids: List[float] = None, visible: bool = None):
        if pipeline_ids is not None:
            self.pipeline_ids = pipeline_ids
        if visible is not None:
            self.visible = visible


@JsonMap({})
class GetRolePipelinesOkResponse(BaseModel):
    """GetRolePipelinesOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The response data, defaults to None
    :type data: GetRolePipelinesOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: GetRolePipelinesOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetRolePipelinesOkResponseData)
