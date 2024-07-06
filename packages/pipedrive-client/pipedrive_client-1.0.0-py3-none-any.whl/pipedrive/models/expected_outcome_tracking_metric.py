from enum import Enum


class ExpectedOutcomeTrackingMetric(Enum):
    """An enumeration representing different categories.

    :cvar QUANTITY: "quantity"
    :vartype QUANTITY: str
    :cvar SUM: "sum"
    :vartype SUM: str
    """

    QUANTITY = "quantity"
    SUM = "sum"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, ExpectedOutcomeTrackingMetric._member_map_.values())
        )
