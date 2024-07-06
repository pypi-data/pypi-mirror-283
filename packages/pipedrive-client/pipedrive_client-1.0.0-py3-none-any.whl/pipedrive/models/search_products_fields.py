from enum import Enum


class SearchProductsFields(Enum):
    """An enumeration representing different categories.

    :cvar CODE: "code"
    :vartype CODE: str
    :cvar CUSTOM_FIELDS: "custom_fields"
    :vartype CUSTOM_FIELDS: str
    :cvar NAME: "name"
    :vartype NAME: str
    """

    CODE = "code"
    CUSTOM_FIELDS = "custom_fields"
    NAME = "name"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SearchProductsFields._member_map_.values()))
