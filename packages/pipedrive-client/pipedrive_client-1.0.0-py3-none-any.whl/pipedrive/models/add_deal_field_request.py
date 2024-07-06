from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class AddDealFieldRequestFieldType(Enum):
    """An enumeration representing different categories.

    :cvar ADDRESS: "address"
    :vartype ADDRESS: str
    :cvar DATE: "date"
    :vartype DATE: str
    :cvar DATERANGE: "daterange"
    :vartype DATERANGE: str
    :cvar DOUBLE: "double"
    :vartype DOUBLE: str
    :cvar ENUM: "enum"
    :vartype ENUM: str
    :cvar MONETARY: "monetary"
    :vartype MONETARY: str
    :cvar ORG: "org"
    :vartype ORG: str
    :cvar PEOPLE: "people"
    :vartype PEOPLE: str
    :cvar PHONE: "phone"
    :vartype PHONE: str
    :cvar SET: "set"
    :vartype SET: str
    :cvar TEXT: "text"
    :vartype TEXT: str
    :cvar TIME: "time"
    :vartype TIME: str
    :cvar TIMERANGE: "timerange"
    :vartype TIMERANGE: str
    :cvar USER: "user"
    :vartype USER: str
    :cvar VARCHAR: "varchar"
    :vartype VARCHAR: str
    :cvar VARCHAR_AUTO: "varchar_auto"
    :vartype VARCHAR_AUTO: str
    :cvar VISIBLE_TO: "visible_to"
    :vartype VISIBLE_TO: str
    """

    ADDRESS = "address"
    DATE = "date"
    DATERANGE = "daterange"
    DOUBLE = "double"
    ENUM = "enum"
    MONETARY = "monetary"
    ORG = "org"
    PEOPLE = "people"
    PHONE = "phone"
    SET = "set"
    TEXT = "text"
    TIME = "time"
    TIMERANGE = "timerange"
    USER = "user"
    VARCHAR = "varchar"
    VARCHAR_AUTO = "varchar_auto"
    VISIBLE_TO = "visible_to"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, AddDealFieldRequestFieldType._member_map_.values())
        )


@JsonMap({})
class AddDealFieldRequest(BaseModel):
    """AddDealFieldRequest

    :param name: The name of the field
    :type name: str
    :param options: When `field_type` is either set or enum, possible options must be supplied as a JSON-encoded sequential array of objects. Example: `[{"label":"New Item"}]`, defaults to None
    :type options: List[dict], optional
    :param add_visible_flag: Whether the field is available in the 'add new' modal or not (both in the web and mobile app), defaults to None
    :type add_visible_flag: bool, optional
    :param field_type: The type of the field<table><tr><th>Value</th><th>Description</th></tr><tr><td>`address`</td><td>Address field</td></tr><tr><td>`date`</td><td>Date (format YYYY-MM-DD)</td></tr><tr><td>`daterange`</td><td>Date-range field (has a start date and end date value, both YYYY-MM-DD)</td></tr><tr><td>`double`</td><td>Numeric value</td></tr><tr><td>`enum`</td><td>Options field with a single possible chosen option</td></tr><tr></tr><tr><td>`monetary`</td><td>Monetary field (has a numeric value and a currency value)</td></tr><tr><td>`org`</td><td>Organization field (contains an organization ID which is stored on the same account)</td></tr><tr><td>`people`</td><td>Person field (contains a person ID which is stored on the same account)</td></tr><tr><td>`phone`</td><td>Phone field (up to 255 numbers and/or characters)</td></tr><tr><td>`set`</td><td>Options field with a possibility of having multiple chosen options</td></tr><tr><td>`text`</td><td>Long text (up to 65k characters)</td></tr><tr><td>`time`</td><td>Time field (format HH:MM:SS)</td></tr><tr><td>`timerange`</td><td>Time-range field (has a start time and end time value, both HH:MM:SS)</td></tr><tr><td>`user`</td><td>User field (contains a user ID of another Pipedrive user)</td></tr><tr><td>`varchar`</td><td>Text (up to 255 characters)</td></tr><tr><td>`varchar_auto`</td><td>Autocomplete text (up to 255 characters)</td></tr><tr><td>`visible_to`</td><td>System field that keeps item's visibility setting</td></tr></table>
    :type field_type: AddDealFieldRequestFieldType
    """

    def __init__(
        self,
        name: str,
        field_type: AddDealFieldRequestFieldType,
        options: List[dict] = None,
        add_visible_flag: bool = None,
    ):
        self.name = name
        if options is not None:
            self.options = options
        if add_visible_flag is not None:
            self.add_visible_flag = add_visible_flag
        self.field_type = self._enum_matching(
            field_type, AddDealFieldRequestFieldType.list(), "field_type"
        )
