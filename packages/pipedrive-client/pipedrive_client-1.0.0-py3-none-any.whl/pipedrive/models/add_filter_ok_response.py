from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class DataType1(Enum):
    """An enumeration representing different categories.

    :cvar DEALS: "deals"
    :vartype DEALS: str
    :cvar LEADS: "leads"
    :vartype LEADS: str
    :cvar ORG: "org"
    :vartype ORG: str
    :cvar PEOPLE: "people"
    :vartype PEOPLE: str
    :cvar PRODUCTS: "products"
    :vartype PRODUCTS: str
    :cvar ACTIVITY: "activity"
    :vartype ACTIVITY: str
    :cvar PROJECTS: "projects"
    :vartype PROJECTS: str
    """

    DEALS = "deals"
    LEADS = "leads"
    ORG = "org"
    PEOPLE = "people"
    PRODUCTS = "products"
    ACTIVITY = "activity"
    PROJECTS = "projects"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, DataType1._member_map_.values()))


@JsonMap({"id_": "id", "type_": "type"})
class AddFilterOkResponseData(BaseModel):
    """AddFilterOkResponseData

    :param id_: The ID of the created filter, defaults to None
    :type id_: int, optional
    :param name: The name of the created filter, defaults to None
    :type name: str, optional
    :param active_flag: The activity flag of the created filter, defaults to None
    :type active_flag: bool, optional
    :param type_: type_, defaults to None
    :type type_: DataType1, optional
    :param temporary_flag: If the created filter is temporary or not, defaults to None
    :type temporary_flag: bool, optional
    :param user_id: The user ID of the created filter, defaults to None
    :type user_id: int, optional
    :param add_time: The add time of the created filter, defaults to None
    :type add_time: str, optional
    :param update_time: The update time of the created filter, defaults to None
    :type update_time: str, optional
    :param visible_to: The visibility group ID of the created filter, defaults to None
    :type visible_to: int, optional
    :param custom_view_id: The custom view ID of the created filter, defaults to None
    :type custom_view_id: int, optional
    :param conditions: The created filter conditions object, defaults to None
    :type conditions: dict, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        active_flag: bool = None,
        type_: DataType1 = None,
        temporary_flag: bool = None,
        user_id: int = None,
        add_time: str = None,
        update_time: str = None,
        visible_to: int = None,
        custom_view_id: int = None,
        conditions: dict = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if active_flag is not None:
            self.active_flag = active_flag
        if type_ is not None:
            self.type_ = self._enum_matching(type_, DataType1.list(), "type_")
        if temporary_flag is not None:
            self.temporary_flag = temporary_flag
        if user_id is not None:
            self.user_id = user_id
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if visible_to is not None:
            self.visible_to = visible_to
        if custom_view_id is not None:
            self.custom_view_id = custom_view_id
        if conditions is not None:
            self.conditions = conditions


@JsonMap({})
class AddFilterOkResponse(BaseModel):
    """AddFilterOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: AddFilterOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: AddFilterOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, AddFilterOkResponseData)
