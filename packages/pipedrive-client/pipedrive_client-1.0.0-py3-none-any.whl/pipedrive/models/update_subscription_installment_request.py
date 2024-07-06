from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class UpdateSubscriptionInstallmentRequest(BaseModel):
    """UpdateSubscriptionInstallmentRequest

    :param payments: Array of payments. It requires a minimum structure as follows: [{ amount:SUM, description:DESCRIPTION, due_at:PAYMENT_DATE }]. Replace SUM with a payment amount, DESCRIPTION with a explanation string, PAYMENT_DATE with a date (format YYYY-MM-DD).
    :type payments: List[dict]
    :param update_deal_value: Indicates that the deal value must be set to installment subscription's total value, defaults to None
    :type update_deal_value: bool, optional
    """

    def __init__(self, payments: List[dict], update_deal_value: bool = None):
        self.payments = payments
        if update_deal_value is not None:
            self.update_deal_value = update_deal_value
