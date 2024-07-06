from enum import Enum


class SearchItemByFieldFieldType(Enum):
    """An enumeration representing different categories.

    :cvar DEALFIELD: "dealField"
    :vartype DEALFIELD: str
    :cvar LEADFIELD: "leadField"
    :vartype LEADFIELD: str
    :cvar PERSONFIELD: "personField"
    :vartype PERSONFIELD: str
    :cvar ORGANIZATIONFIELD: "organizationField"
    :vartype ORGANIZATIONFIELD: str
    :cvar PRODUCTFIELD: "productField"
    :vartype PRODUCTFIELD: str
    :cvar PROJECTFIELD: "projectField"
    :vartype PROJECTFIELD: str
    """

    DEALFIELD = "dealField"
    LEADFIELD = "leadField"
    PERSONFIELD = "personField"
    ORGANIZATIONFIELD = "organizationField"
    PRODUCTFIELD = "productField"
    PROJECTFIELD = "projectField"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, SearchItemByFieldFieldType._member_map_.values())
        )
