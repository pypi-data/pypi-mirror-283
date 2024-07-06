from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class AddLeadLabelRequestColor(Enum):
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
            map(lambda x: x.value, AddLeadLabelRequestColor._member_map_.values())
        )


@JsonMap({})
class AddLeadLabelRequest(BaseModel):
    """AddLeadLabelRequest

    :param name: The name of the lead label
    :type name: str
    :param color: The color of the label. Only a subset of colors can be used.
    :type color: AddLeadLabelRequestColor
    """

    def __init__(self, name: str, color: AddLeadLabelRequestColor):
        self.name = name
        self.color = self._enum_matching(
            color, AddLeadLabelRequestColor.list(), "color"
        )
