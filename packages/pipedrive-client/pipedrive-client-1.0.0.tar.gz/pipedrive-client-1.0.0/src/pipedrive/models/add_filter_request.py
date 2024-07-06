from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class AddFilterRequestType(Enum):
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
        return list(map(lambda x: x.value, AddFilterRequestType._member_map_.values()))


@JsonMap({"type_": "type"})
class AddFilterRequest(BaseModel):
    """AddFilterRequest

    :param name: The name of the filter
    :type name: str
    :param conditions: The conditions of the filter as a JSON object. Please note that a maximum of 16 conditions is allowed per filter and `date` values must be supplied in the `YYYY-MM-DD` format. It requires a minimum structure as follows: `{"glue":"and","conditions":[{"glue":"and","conditions": [CONDITION_OBJECTS]},{"glue":"or","conditions":[CONDITION_OBJECTS]}]}`. Replace `CONDITION_OBJECTS` with JSON objects of the following structure: `{"object":"","field_id":"", "operator":"","value":"", "extra_value":""}` or leave the array empty. Depending on the object type you should use another API endpoint to get `field_id`. There are five types of objects you can choose from: `"person"`, `"deal"`, `"organization"`, `"product"`, `"activity"` and you can use these types of operators depending on what type of a field you have: `"IS NOT NULL"`, `"IS NULL"`, `"<="`, `">="`, `"<"`, `">"`, `"!="`, `"="`, `"LIKE '$%'"`, `"LIKE '%$%'"`, `"NOT LIKE '$%'"`. To get a better understanding of how filters work try creating them directly from the Pipedrive application.
    :type conditions: dict
    :param type_: type_
    :type type_: AddFilterRequestType
    """

    def __init__(self, name: str, conditions: dict, type_: AddFilterRequestType):
        self.name = name
        self.conditions = conditions
        self.type_ = self._enum_matching(type_, AddFilterRequestType.list(), "type_")
