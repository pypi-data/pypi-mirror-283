from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class CancelRecurringSubscriptionRequest(BaseModel):
    """CancelRecurringSubscriptionRequest

    :param end_date: The subscription termination date. All payments after the specified date will be deleted. The end_date of the subscription will be set to the due date of the payment to follow the specified date. Default value is the current date., defaults to None
    :type end_date: str, optional
    """

    def __init__(self, end_date: str = None):
        if end_date is not None:
            self.end_date = end_date
