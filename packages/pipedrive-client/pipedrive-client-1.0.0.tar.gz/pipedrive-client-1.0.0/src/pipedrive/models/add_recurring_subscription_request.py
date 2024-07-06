from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class CadenceType(Enum):
    """An enumeration representing different categories.

    :cvar WEEKLY: "weekly"
    :vartype WEEKLY: str
    :cvar MONTHLY: "monthly"
    :vartype MONTHLY: str
    :cvar QUARTERLY: "quarterly"
    :vartype QUARTERLY: str
    :cvar YEARLY: "yearly"
    :vartype YEARLY: str
    """

    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, CadenceType._member_map_.values()))


@JsonMap({})
class AddRecurringSubscriptionRequest(BaseModel):
    """AddRecurringSubscriptionRequest

    :param deal_id: The ID of the deal this recurring subscription is associated with
    :type deal_id: int
    :param currency: The currency of the recurring subscription. Accepts a 3-character currency code.
    :type currency: str
    :param description: The description of the recurring subscription, defaults to None
    :type description: str, optional
    :param cadence_type: The interval between payments
    :type cadence_type: CadenceType
    :param cycles_count: Shows how many payments the subscription has. Note that one field must be set: `cycles_count` or `infinite`. If `cycles_count` is set, then `cycle_amount` and `start_date` are also required., defaults to None
    :type cycles_count: int, optional
    :param cycle_amount: The amount of each payment
    :type cycle_amount: int
    :param start_date: The start date of the recurring subscription. Format: YYYY-MM-DD
    :type start_date: str
    :param infinite: This indicates that the recurring subscription will last until it's manually canceled or deleted. Note that only one field must be set: `cycles_count` or `infinite`., defaults to None
    :type infinite: bool, optional
    :param payments: Array of additional payments. It requires a minimum structure as follows: [{ amount:SUM, description:DESCRIPTION, due_at:PAYMENT_DATE }]. Replace SUM with a payment amount, DESCRIPTION with an explanation string, PAYMENT_DATE with a date (format YYYY-MM-DD)., defaults to None
    :type payments: List[dict], optional
    :param update_deal_value: Indicates that the deal value must be set to recurring subscription's MRR value, defaults to None
    :type update_deal_value: bool, optional
    """

    def __init__(
        self,
        deal_id: int,
        currency: str,
        cadence_type: CadenceType,
        cycle_amount: int,
        start_date: str,
        description: str = None,
        cycles_count: int = None,
        infinite: bool = None,
        payments: List[dict] = None,
        update_deal_value: bool = None,
    ):
        self.deal_id = deal_id
        self.currency = currency
        if description is not None:
            self.description = description
        self.cadence_type = self._enum_matching(
            cadence_type, CadenceType.list(), "cadence_type"
        )
        if cycles_count is not None:
            self.cycles_count = cycles_count
        self.cycle_amount = cycle_amount
        self.start_date = start_date
        if infinite is not None:
            self.infinite = infinite
        if payments is not None:
            self.payments = payments
        if update_deal_value is not None:
            self.update_deal_value = update_deal_value
