from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class UpdateLeadLabelRequestColor(Enum):
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
        return list(
            map(lambda x: x.value, UpdateLeadLabelRequestColor._member_map_.values())
        )


@JsonMap({})
class UpdateLeadLabelRequest(BaseModel):
    """UpdateLeadLabelRequest

    :param name: The name of the lead label, defaults to None
    :type name: str, optional
    :param color: The color of the label. Only a subset of colors can be used., defaults to None
    :type color: UpdateLeadLabelRequestColor, optional
    """

    def __init__(self, name: str = None, color: UpdateLeadLabelRequestColor = None):
        if name is not None:
            self.name = name
        if color is not None:
            self.color = self._enum_matching(
                color, UpdateLeadLabelRequestColor.list(), "color"
            )
