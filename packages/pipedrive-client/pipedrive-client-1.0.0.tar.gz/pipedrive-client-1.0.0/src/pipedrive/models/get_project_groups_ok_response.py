from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class GetProjectGroupsOkResponseData(BaseModel):
    """GetProjectGroupsOkResponseData

    :param id_: ID of the group, defaults to None
    :type id_: float, optional
    :param name: Name of the group, defaults to None
    :type name: str, optional
    :param order_nr: Order number of the group, defaults to None
    :type order_nr: float, optional
    """

    def __init__(self, id_: float = None, name: str = None, order_nr: float = None):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if order_nr is not None:
            self.order_nr = order_nr


@JsonMap({})
class GetProjectGroupsOkResponse(BaseModel):
    """GetProjectGroupsOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetProjectGroupsOkResponseData], optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: dict, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetProjectGroupsOkResponseData] = None,
        additional_data: dict = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetProjectGroupsOkResponseData)
        if additional_data is not None:
            self.additional_data = additional_data
