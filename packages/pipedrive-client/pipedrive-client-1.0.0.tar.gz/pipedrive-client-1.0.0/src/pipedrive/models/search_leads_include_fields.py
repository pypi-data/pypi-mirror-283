from enum import Enum


class SearchLeadsIncludeFields(Enum):
    """An enumeration representing different categories.

    :cvar LEAD_WAS_SEEN: "lead.was_seen"
    :vartype LEAD_WAS_SEEN: str
    """

    LEAD_WAS_SEEN = "lead.was_seen"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, SearchLeadsIncludeFields._member_map_.values())
        )
