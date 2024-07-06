from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class DataFieldType14(Enum):
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
        return list(map(lambda x: x.value, DataFieldType14._member_map_.values()))


@JsonMap({"id_": "id"})
class UpdatePersonFieldOkResponseData(BaseModel):
    """UpdatePersonFieldOkResponseData

    :param id_: The ID of the field. Value is `null` in case of subfields., defaults to None
    :type id_: int, optional
    :param key: The key of the field. For custom fields this is generated upon creation., defaults to None
    :type key: str, optional
    :param name: The name of the field, defaults to None
    :type name: str, optional
    :param order_nr: The order number of the field, defaults to None
    :type order_nr: int, optional
    :param field_type: The type of the field<table><tr><th>Value</th><th>Description</th></tr><tr><td>`address`</td><td>Address field</td></tr><tr><td>`date`</td><td>Date (format YYYY-MM-DD)</td></tr><tr><td>`daterange`</td><td>Date-range field (has a start date and end date value, both YYYY-MM-DD)</td></tr><tr><td>`double`</td><td>Numeric value</td></tr><tr><td>`enum`</td><td>Options field with a single possible chosen option</td></tr><tr></tr><tr><td>`monetary`</td><td>Monetary field (has a numeric value and a currency value)</td></tr><tr><td>`org`</td><td>Organization field (contains an organization ID which is stored on the same account)</td></tr><tr><td>`people`</td><td>Person field (contains a person ID which is stored on the same account)</td></tr><tr><td>`phone`</td><td>Phone field (up to 255 numbers and/or characters)</td></tr><tr><td>`set`</td><td>Options field with a possibility of having multiple chosen options</td></tr><tr><td>`text`</td><td>Long text (up to 65k characters)</td></tr><tr><td>`time`</td><td>Time field (format HH:MM:SS)</td></tr><tr><td>`timerange`</td><td>Time-range field (has a start time and end time value, both HH:MM:SS)</td></tr><tr><td>`user`</td><td>User field (contains a user ID of another Pipedrive user)</td></tr><tr><td>`varchar`</td><td>Text (up to 255 characters)</td></tr><tr><td>`varchar_auto`</td><td>Autocomplete text (up to 255 characters)</td></tr><tr><td>`visible_to`</td><td>System field that keeps item's visibility setting</td></tr></table>, defaults to None
    :type field_type: DataFieldType14, optional
    :param add_time: The creation time of the field, defaults to None
    :type add_time: str, optional
    :param update_time: The update time of the field, defaults to None
    :type update_time: str, optional
    :param last_updated_by_user_id: The ID of the user who created or most recently updated the field, only applicable for custom fields, defaults to None
    :type last_updated_by_user_id: int, optional
    :param created_by_user_id: The ID of the user who created the field, defaults to None
    :type created_by_user_id: int, optional
    :param active_flag: The active flag of the field, defaults to None
    :type active_flag: bool, optional
    :param edit_flag: The edit flag of the field, defaults to None
    :type edit_flag: bool, optional
    :param index_visible_flag: Not used, defaults to None
    :type index_visible_flag: bool, optional
    :param details_visible_flag: Not used, defaults to None
    :type details_visible_flag: bool, optional
    :param add_visible_flag: Not used, defaults to None
    :type add_visible_flag: bool, optional
    :param important_flag: Not used, defaults to None
    :type important_flag: bool, optional
    :param bulk_edit_allowed: Whether or not the field of an item can be edited in bulk, defaults to None
    :type bulk_edit_allowed: bool, optional
    :param searchable_flag: Whether or not items can be searched by this field, defaults to None
    :type searchable_flag: bool, optional
    :param filtering_allowed: Whether or not items can be filtered by this field, defaults to None
    :type filtering_allowed: bool, optional
    :param sortable_flag: Whether or not items can be sorted by this field, defaults to None
    :type sortable_flag: bool, optional
    :param mandatory_flag: Whether or not the field is mandatory, defaults to None
    :type mandatory_flag: bool, optional
    :param options: The options of the field. When there are no options, `null` is returned., defaults to None
    :type options: List[dict], optional
    :param options_deleted: The deleted options of the field. Only present when there is at least 1 deleted option., defaults to None
    :type options_deleted: List[dict], optional
    :param is_subfield: Whether or not the field is a subfield of another field. Only present if field is subfield., defaults to None
    :type is_subfield: bool, optional
    :param subfields: The subfields of the field. Only present when the field has subfields., defaults to None
    :type subfields: List[dict], optional
    """

    def __init__(
        self,
        id_: int = None,
        key: str = None,
        name: str = None,
        order_nr: int = None,
        field_type: DataFieldType14 = None,
        add_time: str = None,
        update_time: str = None,
        last_updated_by_user_id: int = None,
        created_by_user_id: int = None,
        active_flag: bool = None,
        edit_flag: bool = None,
        index_visible_flag: bool = None,
        details_visible_flag: bool = None,
        add_visible_flag: bool = None,
        important_flag: bool = None,
        bulk_edit_allowed: bool = None,
        searchable_flag: bool = None,
        filtering_allowed: bool = None,
        sortable_flag: bool = None,
        mandatory_flag: bool = None,
        options: List[dict] = None,
        options_deleted: List[dict] = None,
        is_subfield: bool = None,
        subfields: List[dict] = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if key is not None:
            self.key = key
        if name is not None:
            self.name = name
        if order_nr is not None:
            self.order_nr = order_nr
        if field_type is not None:
            self.field_type = self._enum_matching(
                field_type, DataFieldType14.list(), "field_type"
            )
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if last_updated_by_user_id is not None:
            self.last_updated_by_user_id = last_updated_by_user_id
        if created_by_user_id is not None:
            self.created_by_user_id = created_by_user_id
        if active_flag is not None:
            self.active_flag = active_flag
        if edit_flag is not None:
            self.edit_flag = edit_flag
        if index_visible_flag is not None:
            self.index_visible_flag = index_visible_flag
        if details_visible_flag is not None:
            self.details_visible_flag = details_visible_flag
        if add_visible_flag is not None:
            self.add_visible_flag = add_visible_flag
        if important_flag is not None:
            self.important_flag = important_flag
        if bulk_edit_allowed is not None:
            self.bulk_edit_allowed = bulk_edit_allowed
        if searchable_flag is not None:
            self.searchable_flag = searchable_flag
        if filtering_allowed is not None:
            self.filtering_allowed = filtering_allowed
        if sortable_flag is not None:
            self.sortable_flag = sortable_flag
        if mandatory_flag is not None:
            self.mandatory_flag = mandatory_flag
        if options is not None:
            self.options = options
        if options_deleted is not None:
            self.options_deleted = options_deleted
        if is_subfield is not None:
            self.is_subfield = is_subfield
        if subfields is not None:
            self.subfields = subfields


@JsonMap({})
class UpdatePersonFieldOkResponse(BaseModel):
    """UpdatePersonFieldOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: UpdatePersonFieldOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: UpdatePersonFieldOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, UpdatePersonFieldOkResponseData)
