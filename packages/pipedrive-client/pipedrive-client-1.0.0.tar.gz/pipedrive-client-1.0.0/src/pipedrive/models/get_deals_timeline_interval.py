from enum import Enum


class GetDealsTimelineInterval(Enum):
    """An enumeration representing different categories.

    :cvar DAY: "day"
    :vartype DAY: str
    :cvar WEEK: "week"
    :vartype WEEK: str
    :cvar MONTH: "month"
    :vartype MONTH: str
    :cvar QUARTER: "quarter"
    :vartype QUARTER: str
    """

    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, GetDealsTimelineInterval._member_map_.values())
        )
