from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class DataFieldType18(Enum):
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
        return list(map(lambda x: x.value, DataFieldType18._member_map_.values()))


@JsonMap({"id_": "id"})
class UpdateProductFieldOkResponseData(BaseModel):
    """UpdateProductFieldOkResponseData

    :param name: The name of the field
    :type name: str
    :param options: When `field_type` is either `set` or `enum`, possible options must be supplied as a JSON-encoded sequential array, for example:</br>`[{"label":"red"}, {"label":"blue"}, {"label":"lilac"}]`, defaults to None
    :type options: List[dict], optional
    :param field_type: The type of the field<table><tr><th>Value</th><th>Description</th></tr><tr><td>`varchar`</td><td>Text (up to 255 characters)</td><tr><td>`varchar_auto`</td><td>Autocomplete text (up to 255 characters)</td><tr><td>`text`</td><td>Long text (up to 65k characters)</td><tr><td>`double`</td><td>Numeric value</td><tr><td>`monetary`</td><td>Monetary field (has a numeric value and a currency value)</td><tr><td>`date`</td><td>Date (format YYYY-MM-DD)</td><tr><td>`set`</td><td>Options field with a possibility of having multiple chosen options</td><tr><td>`enum`</td><td>Options field with a single possible chosen option</td><tr><td>`user`</td><td>User field (contains a user ID of another Pipedrive user)</td><tr><td>`org`</td><td>Organization field (contains an organization ID which is stored on the same account)</td><tr><td>`people`</td><td>Person field (contains a product ID which is stored on the same account)</td><tr><td>`phone`</td><td>Phone field (up to 255 numbers and/or characters)</td><tr><td>`time`</td><td>Time field (format HH:MM:SS)</td><tr><td>`timerange`</td><td>Time-range field (has a start time and end time value, both HH:MM:SS)</td><tr><td>`daterange`</td><td>Date-range field (has a start date and end date value, both YYYY-MM-DD)</td><tr><td>`address`</td><td>Address field</dd></table>
    :type field_type: DataFieldType18
    :param id_: The ID of the product field, defaults to None
    :type id_: int, optional
    :param key: The key of the product field, defaults to None
    :type key: str, optional
    :param order_nr: The position (index) of the product field in the detail view, defaults to None
    :type order_nr: int, optional
    :param add_time: The product field creation time. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    :param update_time: The product field last update time. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type update_time: str, optional
    :param last_updated_by_user_id: The ID of the last user to update the product field, defaults to None
    :type last_updated_by_user_id: int, optional
    :param created_by_user_id: The ID of the user who created the product field, defaults to None
    :type created_by_user_id: int, optional
    :param active_flag: Whether or not the product field is currently active, defaults to None
    :type active_flag: bool, optional
    :param edit_flag: Whether or not the product field name and metadata is editable, defaults to None
    :type edit_flag: bool, optional
    :param add_visible_flag: Whether or not the product field is visible in the Add Product Modal, defaults to None
    :type add_visible_flag: bool, optional
    :param important_flag: Whether or not the product field is marked as important, defaults to None
    :type important_flag: bool, optional
    :param bulk_edit_allowed: Whether or not the product field data can be edited, defaults to None
    :type bulk_edit_allowed: bool, optional
    :param searchable_flag: Whether or not the product field is searchable, defaults to None
    :type searchable_flag: bool, optional
    :param filtering_allowed: Whether or not the product field value can be used when filtering searches, defaults to None
    :type filtering_allowed: bool, optional
    :param sortable_flag: Whether or not the product field is sortable, defaults to None
    :type sortable_flag: bool, optional
    :param mandatory_flag: Whether or not the product field is mandatory when creating products, defaults to None
    :type mandatory_flag: bool, optional
    """

    def __init__(
        self,
        name: str,
        field_type: DataFieldType18,
        options: List[dict] = None,
        id_: int = None,
        key: str = None,
        order_nr: int = None,
        add_time: str = None,
        update_time: str = None,
        last_updated_by_user_id: int = None,
        created_by_user_id: int = None,
        active_flag: bool = None,
        edit_flag: bool = None,
        add_visible_flag: bool = None,
        important_flag: bool = None,
        bulk_edit_allowed: bool = None,
        searchable_flag: bool = None,
        filtering_allowed: bool = None,
        sortable_flag: bool = None,
        mandatory_flag: bool = None,
    ):
        self.name = name
        if options is not None:
            self.options = options
        self.field_type = self._enum_matching(
            field_type, DataFieldType18.list(), "field_type"
        )
        if id_ is not None:
            self.id_ = id_
        if key is not None:
            self.key = key
        if order_nr is not None:
            self.order_nr = order_nr
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


@JsonMap({})
class UpdateProductFieldOkResponse(BaseModel):
    """UpdateProductFieldOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: UpdateProductFieldOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: UpdateProductFieldOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, UpdateProductFieldOkResponseData)
