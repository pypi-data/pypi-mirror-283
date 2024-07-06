from enum import Enum


class SearchDealsFields(Enum):
    """An enumeration representing different categories.

    :cvar CUSTOM_FIELDS: "custom_fields"
    :vartype CUSTOM_FIELDS: str
    :cvar NOTES: "notes"
    :vartype NOTES: str
    :cvar TITLE: "title"
    :vartype TITLE: str
    """

    CUSTOM_FIELDS = "custom_fields"
    NOTES = "notes"
    TITLE = "title"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SearchDealsFields._member_map_.values()))
