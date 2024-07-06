from enum import Enum


class SearchPersonsFields(Enum):
    """An enumeration representing different categories.

    :cvar CUSTOM_FIELDS: "custom_fields"
    :vartype CUSTOM_FIELDS: str
    :cvar EMAIL: "email"
    :vartype EMAIL: str
    :cvar NOTES: "notes"
    :vartype NOTES: str
    :cvar PHONE: "phone"
    :vartype PHONE: str
    :cvar NAME: "name"
    :vartype NAME: str
    """

    CUSTOM_FIELDS = "custom_fields"
    EMAIL = "email"
    NOTES = "notes"
    PHONE = "phone"
    NAME = "name"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SearchPersonsFields._member_map_.values()))
