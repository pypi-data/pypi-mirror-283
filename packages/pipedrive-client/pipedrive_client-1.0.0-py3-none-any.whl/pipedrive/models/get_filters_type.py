from enum import Enum


class GetFiltersType(Enum):
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
        return list(map(lambda x: x.value, GetFiltersType._member_map_.values()))
