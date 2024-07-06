from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class AddActivityTypeRequestIconKey(Enum):
    """An enumeration representing different categories.

    :cvar TASK: "task"
    :vartype TASK: str
    :cvar EMAIL: "email"
    :vartype EMAIL: str
    :cvar MEETING: "meeting"
    :vartype MEETING: str
    :cvar DEADLINE: "deadline"
    :vartype DEADLINE: str
    :cvar CALL: "call"
    :vartype CALL: str
    :cvar LUNCH: "lunch"
    :vartype LUNCH: str
    :cvar CALENDAR: "calendar"
    :vartype CALENDAR: str
    :cvar DOWNARROW: "downarrow"
    :vartype DOWNARROW: str
    :cvar DOCUMENT: "document"
    :vartype DOCUMENT: str
    :cvar SMARTPHONE: "smartphone"
    :vartype SMARTPHONE: str
    :cvar CAMERA: "camera"
    :vartype CAMERA: str
    :cvar SCISSORS: "scissors"
    :vartype SCISSORS: str
    :cvar COGS: "cogs"
    :vartype COGS: str
    :cvar BUBBLE: "bubble"
    :vartype BUBBLE: str
    :cvar UPARROW: "uparrow"
    :vartype UPARROW: str
    :cvar CHECKBOX: "checkbox"
    :vartype CHECKBOX: str
    :cvar SIGNPOST: "signpost"
    :vartype SIGNPOST: str
    :cvar SHUFFLE: "shuffle"
    :vartype SHUFFLE: str
    :cvar ADDRESSBOOK: "addressbook"
    :vartype ADDRESSBOOK: str
    :cvar LINEGRAPH: "linegraph"
    :vartype LINEGRAPH: str
    :cvar PICTURE: "picture"
    :vartype PICTURE: str
    :cvar CAR: "car"
    :vartype CAR: str
    :cvar WORLD: "world"
    :vartype WORLD: str
    :cvar SEARCH: "search"
    :vartype SEARCH: str
    :cvar CLIP: "clip"
    :vartype CLIP: str
    :cvar SOUND: "sound"
    :vartype SOUND: str
    :cvar BRUSH: "brush"
    :vartype BRUSH: str
    :cvar KEY: "key"
    :vartype KEY: str
    :cvar PADLOCK: "padlock"
    :vartype PADLOCK: str
    :cvar PRICETAG: "pricetag"
    :vartype PRICETAG: str
    :cvar SUITCASE: "suitcase"
    :vartype SUITCASE: str
    :cvar FINISH: "finish"
    :vartype FINISH: str
    :cvar PLANE: "plane"
    :vartype PLANE: str
    :cvar LOOP: "loop"
    :vartype LOOP: str
    :cvar WIFI: "wifi"
    :vartype WIFI: str
    :cvar TRUCK: "truck"
    :vartype TRUCK: str
    :cvar CART: "cart"
    :vartype CART: str
    :cvar BULB: "bulb"
    :vartype BULB: str
    :cvar BELL: "bell"
    :vartype BELL: str
    :cvar PRESENTATION: "presentation"
    :vartype PRESENTATION: str
    """

    TASK = "task"
    EMAIL = "email"
    MEETING = "meeting"
    DEADLINE = "deadline"
    CALL = "call"
    LUNCH = "lunch"
    CALENDAR = "calendar"
    DOWNARROW = "downarrow"
    DOCUMENT = "document"
    SMARTPHONE = "smartphone"
    CAMERA = "camera"
    SCISSORS = "scissors"
    COGS = "cogs"
    BUBBLE = "bubble"
    UPARROW = "uparrow"
    CHECKBOX = "checkbox"
    SIGNPOST = "signpost"
    SHUFFLE = "shuffle"
    ADDRESSBOOK = "addressbook"
    LINEGRAPH = "linegraph"
    PICTURE = "picture"
    CAR = "car"
    WORLD = "world"
    SEARCH = "search"
    CLIP = "clip"
    SOUND = "sound"
    BRUSH = "brush"
    KEY = "key"
    PADLOCK = "padlock"
    PRICETAG = "pricetag"
    SUITCASE = "suitcase"
    FINISH = "finish"
    PLANE = "plane"
    LOOP = "loop"
    WIFI = "wifi"
    TRUCK = "truck"
    CART = "cart"
    BULB = "bulb"
    BELL = "bell"
    PRESENTATION = "presentation"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, AddActivityTypeRequestIconKey._member_map_.values())
        )


@JsonMap({})
class AddActivityTypeRequest(BaseModel):
    """AddActivityTypeRequest

    :param name: The name of the activity type
    :type name: str
    :param icon_key: Icon graphic to use for representing this activity type
    :type icon_key: AddActivityTypeRequestIconKey
    :param color: A designated color for the activity type in 6-character HEX format (e.g. `FFFFFF` for white, `000000` for black), defaults to None
    :type color: str, optional
    """

    def __init__(
        self, name: str, icon_key: AddActivityTypeRequestIconKey, color: str = None
    ):
        self.name = name
        self.icon_key = self._enum_matching(
            icon_key, AddActivityTypeRequestIconKey.list(), "icon_key"
        )
        if color is not None:
            self.color = color
