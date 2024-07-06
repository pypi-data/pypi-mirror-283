from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class DataColor1(Enum):
    """An enumeration representing different categories.

    :cvar GREEN: "green"
    :vartype GREEN: str
    :cvar BLUE: "blue"
    :vartype BLUE: str
    :cvar RED: "red"
    :vartype RED: str
    :cvar YELLOW: "yellow"
    :vartype YELLOW: str
    :cvar PURPLE: "purple"
    :vartype PURPLE: str
    :cvar GRAY: "gray"
    :vartype GRAY: str
    """

    GREEN = "green"
    BLUE = "blue"
    RED = "red"
    YELLOW = "yellow"
    PURPLE = "purple"
    GRAY = "gray"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, DataColor1._member_map_.values()))


@JsonMap({"id_": "id"})
class GetLeadLabelsOkResponseData(BaseModel):
    """GetLeadLabelsOkResponseData

    :param id_: The unique ID of the lead label, defaults to None
    :type id_: str, optional
    :param name: The name of the lead label, defaults to None
    :type name: str, optional
    :param color: The color of the label. Only a subset of colors can be used., defaults to None
    :type color: DataColor1, optional
    :param add_time: The date and time of when the lead label was created. In ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ., defaults to None
    :type add_time: str, optional
    :param update_time: The date and time of when the lead label was last updated. In ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ., defaults to None
    :type update_time: str, optional
    """

    def __init__(
        self,
        id_: str = None,
        name: str = None,
        color: DataColor1 = None,
        add_time: str = None,
        update_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if color is not None:
            self.color = self._enum_matching(color, DataColor1.list(), "color")
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time


@JsonMap({})
class GetLeadLabelsOkResponse(BaseModel):
    """GetLeadLabelsOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetLeadLabelsOkResponseData], optional
    """

    def __init__(
        self, success: bool = None, data: List[GetLeadLabelsOkResponseData] = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetLeadLabelsOkResponseData)
