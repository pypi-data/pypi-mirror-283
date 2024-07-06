from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GetLeadSourcesOkResponseData(BaseModel):
    """GetLeadSourcesOkResponseData

    :param name: The unique name of a lead source, defaults to None
    :type name: str, optional
    """

    def __init__(self, name: str = None):
        if name is not None:
            self.name = name


@JsonMap({})
class GetLeadSourcesOkResponse(BaseModel):
    """GetLeadSourcesOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetLeadSourcesOkResponseData], optional
    """

    def __init__(
        self, success: bool = None, data: List[GetLeadSourcesOkResponseData] = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetLeadSourcesOkResponseData)
