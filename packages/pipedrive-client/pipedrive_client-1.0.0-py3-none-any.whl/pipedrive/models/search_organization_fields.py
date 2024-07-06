from enum import Enum


class SearchOrganizationFields(Enum):
    """An enumeration representing different categories.

    :cvar ADDRESS: "address"
    :vartype ADDRESS: str
    :cvar CUSTOM_FIELDS: "custom_fields"
    :vartype CUSTOM_FIELDS: str
    :cvar NOTES: "notes"
    :vartype NOTES: str
    :cvar NAME: "name"
    :vartype NAME: str
    """

    ADDRESS = "address"
    CUSTOM_FIELDS = "custom_fields"
    NOTES = "notes"
    NAME = "name"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, SearchOrganizationFields._member_map_.values())
        )
