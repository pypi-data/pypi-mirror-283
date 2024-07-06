from enum import Enum


class GetDealsSummaryStatus(Enum):
    """An enumeration representing different categories.

    :cvar OPEN: "open"
    :vartype OPEN: str
    :cvar WON: "won"
    :vartype WON: str
    :cvar LOST: "lost"
    :vartype LOST: str
    """

    OPEN = "open"
    WON = "won"
    LOST = "lost"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, GetDealsSummaryStatus._member_map_.values()))
