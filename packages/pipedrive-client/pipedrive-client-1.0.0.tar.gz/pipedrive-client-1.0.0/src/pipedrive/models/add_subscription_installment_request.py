from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AddSubscriptionInstallmentRequest(BaseModel):
    """AddSubscriptionInstallmentRequest

    :param deal_id: The ID of the deal this installment subscription is associated with
    :type deal_id: int
    :param currency: The currency of the installment subscription. Accepts a 3-character currency code.
    :type currency: str
    :param payments: Array of payments. It requires a minimum structure as follows: [{ amount:SUM, description:DESCRIPTION, due_at:PAYMENT_DATE }]. Replace SUM with a payment amount, DESCRIPTION with an explanation string, PAYMENT_DATE with a date (format YYYY-MM-DD).
    :type payments: List[dict]
    :param update_deal_value: Indicates that the deal value must be set to the installment subscription's total value, defaults to None
    :type update_deal_value: bool, optional
    """

    def __init__(
        self,
        deal_id: int,
        currency: str,
        payments: List[dict],
        update_deal_value: bool = None,
    ):
        self.deal_id = deal_id
        self.currency = currency
        self.payments = payments
        if update_deal_value is not None:
            self.update_deal_value = update_deal_value
