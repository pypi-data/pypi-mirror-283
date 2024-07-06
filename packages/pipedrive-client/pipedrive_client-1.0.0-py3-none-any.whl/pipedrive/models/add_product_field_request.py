from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class AddProductFieldRequestFieldType(Enum):
    """An enumeration representing different categories.

    :cvar VARCHAR: "varchar"
    :vartype VARCHAR: str
    :cvar VARCHAR_AUTO: "varchar_auto"
    :vartype VARCHAR_AUTO: str
    :cvar TEXT: "text"
    :vartype TEXT: str
    :cvar DOUBLE: "double"
    :vartype DOUBLE: str
    :cvar MONETARY: "monetary"
    :vartype MONETARY: str
    :cvar DATE: "date"
    :vartype DATE: str
    :cvar SET: "set"
    :vartype SET: str
    :cvar ENUM: "enum"
    :vartype ENUM: str
    :cvar USER: "user"
    :vartype USER: str
    :cvar ORG: "org"
    :vartype ORG: str
    :cvar PEOPLE: "people"
    :vartype PEOPLE: str
    :cvar PHONE: "phone"
    :vartype PHONE: str
    :cvar TIME: "time"
    :vartype TIME: str
    :cvar TIMERANGE: "timerange"
    :vartype TIMERANGE: str
    :cvar DATERANGE: "daterange"
    :vartype DATERANGE: str
    :cvar ADDRESS: "address"
    :vartype ADDRESS: str
    """

    VARCHAR = "varchar"
    VARCHAR_AUTO = "varchar_auto"
    TEXT = "text"
    DOUBLE = "double"
    MONETARY = "monetary"
    DATE = "date"
    SET = "set"
    ENUM = "enum"
    USER = "user"
    ORG = "org"
    PEOPLE = "people"
    PHONE = "phone"
    TIME = "time"
    TIMERANGE = "timerange"
    DATERANGE = "daterange"
    ADDRESS = "address"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(
                lambda x: x.value, AddProductFieldRequestFieldType._member_map_.values()
            )
        )


@JsonMap({})
class AddProductFieldRequest(BaseModel):
    """AddProductFieldRequest

    :param name: The name of the field
    :type name: str
    :param options: When `field_type` is either `set` or `enum`, possible options must be supplied as a JSON-encoded sequential array, for example:</br>`[{"label":"red"}, {"label":"blue"}, {"label":"lilac"}]`, defaults to None
    :type options: List[dict], optional
    :param field_type: The type of the field<table><tr><th>Value</th><th>Description</th></tr><tr><td>`varchar`</td><td>Text (up to 255 characters)</td><tr><td>`varchar_auto`</td><td>Autocomplete text (up to 255 characters)</td><tr><td>`text`</td><td>Long text (up to 65k characters)</td><tr><td>`double`</td><td>Numeric value</td><tr><td>`monetary`</td><td>Monetary field (has a numeric value and a currency value)</td><tr><td>`date`</td><td>Date (format YYYY-MM-DD)</td><tr><td>`set`</td><td>Options field with a possibility of having multiple chosen options</td><tr><td>`enum`</td><td>Options field with a single possible chosen option</td><tr><td>`user`</td><td>User field (contains a user ID of another Pipedrive user)</td><tr><td>`org`</td><td>Organization field (contains an organization ID which is stored on the same account)</td><tr><td>`people`</td><td>Person field (contains a product ID which is stored on the same account)</td><tr><td>`phone`</td><td>Phone field (up to 255 numbers and/or characters)</td><tr><td>`time`</td><td>Time field (format HH:MM:SS)</td><tr><td>`timerange`</td><td>Time-range field (has a start time and end time value, both HH:MM:SS)</td><tr><td>`daterange`</td><td>Date-range field (has a start date and end date value, both YYYY-MM-DD)</td><tr><td>`address`</td><td>Address field</dd></table>
    :type field_type: AddProductFieldRequestFieldType
    """

    def __init__(
        self,
        name: str,
        field_type: AddProductFieldRequestFieldType,
        options: List[dict] = None,
    ):
        self.name = name
        if options is not None:
            self.options = options
        self.field_type = self._enum_matching(
            field_type, AddProductFieldRequestFieldType.list(), "field_type"
        )
