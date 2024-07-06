from enum import Enum


class SearchPersonsIncludeFields(Enum):
    """An enumeration representing different categories.

    :cvar PERSON_PICTURE: "person.picture"
    :vartype PERSON_PICTURE: str
    """

    PERSON_PICTURE = "person.picture"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, SearchPersonsIncludeFields._member_map_.values())
        )
