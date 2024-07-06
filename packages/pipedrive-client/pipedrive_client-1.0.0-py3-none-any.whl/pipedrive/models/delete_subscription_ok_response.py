from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteSubscriptionOkResponseData(BaseModel):
    """DeleteSubscriptionOkResponseData

    :param id_: The ID of the subscription, defaults to None
    :type id_: int, optional
    :param user_id: The ID of the user who created the subscription, defaults to None
    :type user_id: int, optional
    :param deal_id: The ID of the deal this subscription is associated with, defaults to None
    :type deal_id: int, optional
    :param description: The description of the recurring subscription, defaults to None
    :type description: str, optional
    :param is_active: The subscription status, defaults to None
    :type is_active: bool, optional
    :param cycles_count: Shows how many payments a recurring subscription has, defaults to None
    :type cycles_count: int, optional
    :param cycle_amount: The amount of each payment, defaults to None
    :type cycle_amount: int, optional
    :param infinite: Indicates that the recurring subscription will last until it is manually canceled or deleted, defaults to None
    :type infinite: bool, optional
    :param currency: The currency of the subscription, defaults to None
    :type currency: str, optional
    :param cadence_type: The interval between payments, defaults to None
    :type cadence_type: str, optional
    :param start_date: The start date of the recurring subscription, defaults to None
    :type start_date: str, optional
    :param end_date: The end date of the subscription, defaults to None
    :type end_date: str, optional
    :param lifetime_value: The total value of all payments, defaults to None
    :type lifetime_value: float, optional
    :param final_status: The final status of the subscription, defaults to None
    :type final_status: str, optional
    :param add_time: The creation time of the subscription, defaults to None
    :type add_time: str, optional
    :param update_time: The update time of the subscription, defaults to None
    :type update_time: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        user_id: int = None,
        deal_id: int = None,
        description: str = None,
        is_active: bool = None,
        cycles_count: int = None,
        cycle_amount: int = None,
        infinite: bool = None,
        currency: str = None,
        cadence_type: str = None,
        start_date: str = None,
        end_date: str = None,
        lifetime_value: float = None,
        final_status: str = None,
        add_time: str = None,
        update_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if user_id is not None:
            self.user_id = user_id
        if deal_id is not None:
            self.deal_id = deal_id
        if description is not None:
            self.description = description
        if is_active is not None:
            self.is_active = is_active
        if cycles_count is not None:
            self.cycles_count = cycles_count
        if cycle_amount is not None:
            self.cycle_amount = cycle_amount
        if infinite is not None:
            self.infinite = infinite
        if currency is not None:
            self.currency = currency
        if cadence_type is not None:
            self.cadence_type = cadence_type
        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date
        if lifetime_value is not None:
            self.lifetime_value = lifetime_value
        if final_status is not None:
            self.final_status = final_status
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time


@JsonMap({})
class DeleteSubscriptionOkResponse(BaseModel):
    """DeleteSubscriptionOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteSubscriptionOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: DeleteSubscriptionOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteSubscriptionOkResponseData)
