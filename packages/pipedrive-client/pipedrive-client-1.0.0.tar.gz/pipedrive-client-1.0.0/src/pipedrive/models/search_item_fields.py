from enum import Enum


class SearchItemFields(Enum):
    """An enumeration representing different categories.

    :cvar ADDRESS: "address"
    :vartype ADDRESS: str
    :cvar CODE: "code"
    :vartype CODE: str
    :cvar CUSTOM_FIELDS: "custom_fields"
    :vartype CUSTOM_FIELDS: str
    :cvar EMAIL: "email"
    :vartype EMAIL: str
    :cvar NAME: "name"
    :vartype NAME: str
    :cvar NOTES: "notes"
    :vartype NOTES: str
    :cvar ORGANIZATION_NAME: "organization_name"
    :vartype ORGANIZATION_NAME: str
    :cvar PERSON_NAME: "person_name"
    :vartype PERSON_NAME: str
    :cvar PHONE: "phone"
    :vartype PHONE: str
    :cvar TITLE: "title"
    :vartype TITLE: str
    :cvar DESCRIPTION: "description"
    :vartype DESCRIPTION: str
    """

    ADDRESS = "address"
    CODE = "code"
    CUSTOM_FIELDS = "custom_fields"
    EMAIL = "email"
    NAME = "name"
    NOTES = "notes"
    ORGANIZATION_NAME = "organization_name"
    PERSON_NAME = "person_name"
    PHONE = "phone"
    TITLE = "title"
    DESCRIPTION = "description"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SearchItemFields._member_map_.values()))
