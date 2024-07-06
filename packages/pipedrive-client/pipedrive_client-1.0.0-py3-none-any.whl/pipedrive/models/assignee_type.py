from enum import Enum


class AssigneeType(Enum):
    """An enumeration representing different categories.

    :cvar PERSON: "person"
    :vartype PERSON: str
    :cvar COMPANY: "company"
    :vartype COMPANY: str
    :cvar TEAM: "team"
    :vartype TEAM: str
    """

    PERSON = "person"
    COMPANY = "company"
    TEAM = "team"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, AssigneeType._member_map_.values()))
