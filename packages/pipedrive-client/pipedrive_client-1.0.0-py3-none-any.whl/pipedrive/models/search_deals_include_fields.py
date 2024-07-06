from enum import Enum


class SearchDealsIncludeFields(Enum):
    """An enumeration representing different categories.

    :cvar DEAL_CC_EMAIL: "deal.cc_email"
    :vartype DEAL_CC_EMAIL: str
    """

    DEAL_CC_EMAIL = "deal.cc_email"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, SearchDealsIncludeFields._member_map_.values())
        )
