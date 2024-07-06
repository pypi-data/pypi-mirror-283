from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class DataFieldType6(Enum):
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
        return list(map(lambda x: x.value, DataFieldType6._member_map_.values()))


@JsonMap({"id_": "id"})
class Options(BaseModel):
    """Options

    :param id_: id_, defaults to None
    :type id_: int, optional
    :param label: label, defaults to None
    :type label: str, optional
    """

    def __init__(self, id_: int = None, label: str = None):
        if id_ is not None:
            self.id_ = id_
        if label is not None:
            self.label = label


@JsonMap({"id_": "id"})
class GetNoteFieldsOkResponseData(BaseModel):
    """GetNoteFieldsOkResponseData

    :param id_: The ID of the field, defaults to None
    :type id_: int, optional
    :param key: The key of the field, defaults to None
    :type key: str, optional
    :param name: The name of the field, defaults to None
    :type name: str, optional
    :param field_type: The type of the field<table><tr><th>Value</th><th>Description</th></tr><tr><td>`address`</td><td>Address field</td></tr><tr><td>`date`</td><td>Date (format YYYY-MM-DD)</td></tr><tr><td>`daterange`</td><td>Date-range field (has a start date and end date value, both YYYY-MM-DD)</td></tr><tr><td>`double`</td><td>Numeric value</td></tr><tr><td>`enum`</td><td>Options field with a single possible chosen option</td></tr><tr></tr><tr><td>`monetary`</td><td>Monetary field (has a numeric value and a currency value)</td></tr><tr><td>`org`</td><td>Organization field (contains an organization ID which is stored on the same account)</td></tr><tr><td>`people`</td><td>Person field (contains a person ID which is stored on the same account)</td></tr><tr><td>`phone`</td><td>Phone field (up to 255 numbers and/or characters)</td></tr><tr><td>`set`</td><td>Options field with a possibility of having multiple chosen options</td></tr><tr><td>`text`</td><td>Long text (up to 65k characters)</td></tr><tr><td>`time`</td><td>Time field (format HH:MM:SS)</td></tr><tr><td>`timerange`</td><td>Time-range field (has a start time and end time value, both HH:MM:SS)</td></tr><tr><td>`user`</td><td>User field (contains a user ID of another Pipedrive user)</td></tr><tr><td>`varchar`</td><td>Text (up to 255 characters)</td></tr><tr><td>`varchar_auto`</td><td>Autocomplete text (up to 255 characters)</td></tr><tr><td>`visible_to`</td><td>System field that keeps item's visibility setting</td></tr></table>, defaults to None
    :type field_type: DataFieldType6, optional
    :param active_flag: The active flag of the field, defaults to None
    :type active_flag: bool, optional
    :param edit_flag: The edit flag of the field, defaults to None
    :type edit_flag: bool, optional
    :param bulk_edit_allowed: Not used, defaults to None
    :type bulk_edit_allowed: bool, optional
    :param mandatory_flag: Whether or not the field is mandatory, defaults to None
    :type mandatory_flag: bool, optional
    :param options: The options of the field. When there are no options, `null` is returned., defaults to None
    :type options: List[Options], optional
    """

    def __init__(
        self,
        id_: int = None,
        key: str = None,
        name: str = None,
        field_type: DataFieldType6 = None,
        active_flag: bool = None,
        edit_flag: bool = None,
        bulk_edit_allowed: bool = None,
        mandatory_flag: bool = None,
        options: List[Options] = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if key is not None:
            self.key = key
        if name is not None:
            self.name = name
        if field_type is not None:
            self.field_type = self._enum_matching(
                field_type, DataFieldType6.list(), "field_type"
            )
        if active_flag is not None:
            self.active_flag = active_flag
        if edit_flag is not None:
            self.edit_flag = edit_flag
        if bulk_edit_allowed is not None:
            self.bulk_edit_allowed = bulk_edit_allowed
        if mandatory_flag is not None:
            self.mandatory_flag = mandatory_flag
        if options is not None:
            self.options = self._define_list(options, Options)


@JsonMap({})
class GetNoteFieldsOkResponseAdditionalData(BaseModel):
    """The additional data of the list

    :param start: Pagination start, defaults to None
    :type start: int, optional
    :param limit: Items shown per page, defaults to None
    :type limit: int, optional
    :param more_items_in_collection: If there are more list items in the collection than displayed or not, defaults to None
    :type more_items_in_collection: bool, optional
    """

    def __init__(
        self,
        start: int = None,
        limit: int = None,
        more_items_in_collection: bool = None,
    ):
        if start is not None:
            self.start = start
        if limit is not None:
            self.limit = limit
        if more_items_in_collection is not None:
            self.more_items_in_collection = more_items_in_collection


@JsonMap({})
class GetNoteFieldsOkResponse(BaseModel):
    """GetNoteFieldsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetNoteFieldsOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetNoteFieldsOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetNoteFieldsOkResponseData] = None,
        additional_data: GetNoteFieldsOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetNoteFieldsOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetNoteFieldsOkResponseAdditionalData
            )
