from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class UpdateRecurringSubscriptionRequest(BaseModel):
    """UpdateRecurringSubscriptionRequest

    :param description: The description of the recurring subscription, defaults to None
    :type description: str, optional
    :param cycle_amount: The amount of each payment, defaults to None
    :type cycle_amount: int, optional
    :param payments: Array of additional payments. It requires a minimum structure as follows: [{ amount:SUM, description:DESCRIPTION, due_at:PAYMENT_DATE }]. Replace SUM with a payment amount, DESCRIPTION with an explanation string, PAYMENT_DATE with a date (format YYYY-MM-DD)., defaults to None
    :type payments: List[dict], optional
    :param update_deal_value: Indicates that the deal value must be set to recurring subscription's MRR value, defaults to None
    :type update_deal_value: bool, optional
    :param effective_date: All payments after that date will be affected. Format: YYYY-MM-DD
    :type effective_date: str
    """

    def __init__(
        self,
        effective_date: str,
        description: str = None,
        cycle_amount: int = None,
        payments: List[dict] = None,
        update_deal_value: bool = None,
    ):
        if description is not None:
            self.description = description
        if cycle_amount is not None:
            self.cycle_amount = cycle_amount
        if payments is not None:
            self.payments = payments
        if update_deal_value is not None:
            self.update_deal_value = update_deal_value
        self.effective_date = effective_date
