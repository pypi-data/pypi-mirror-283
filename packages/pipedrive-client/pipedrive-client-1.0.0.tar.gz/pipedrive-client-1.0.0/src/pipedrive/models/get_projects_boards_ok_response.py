from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class GetProjectsBoardsOkResponseData(BaseModel):
    """GetProjectsBoardsOkResponseData

    :param id_: The ID of the project board, defaults to None
    :type id_: int, optional
    :param name: Name of a project board, defaults to None
    :type name: str, optional
    :param order_nr: The order of a board, defaults to None
    :type order_nr: float, optional
    :param add_time: The creation date and time of the board in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param update_time: The update date and time of the board in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        order_nr: float = None,
        add_time: str = None,
        update_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if order_nr is not None:
            self.order_nr = order_nr
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time


@JsonMap({})
class GetProjectsBoardsOkResponse(BaseModel):
    """GetProjectsBoardsOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetProjectsBoardsOkResponseData], optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: dict, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetProjectsBoardsOkResponseData] = None,
        additional_data: dict = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetProjectsBoardsOkResponseData)
        if additional_data is not None:
            self.additional_data = additional_data
