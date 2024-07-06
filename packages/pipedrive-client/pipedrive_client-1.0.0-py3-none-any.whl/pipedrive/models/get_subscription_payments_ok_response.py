from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class RevenueMovementType(Enum):
    """An enumeration representing different categories.

    :cvar NEW: "new"
    :vartype NEW: str
    :cvar RECURRING: "recurring"
    :vartype RECURRING: str
    :cvar EXPANSION: "expansion"
    :vartype EXPANSION: str
    :cvar CONTRACTION: "contraction"
    :vartype CONTRACTION: str
    :cvar NONE: "none"
    :vartype NONE: str
    :cvar CHURN: "churn"
    :vartype CHURN: str
    """

    NEW = "new"
    RECURRING = "recurring"
    EXPANSION = "expansion"
    CONTRACTION = "contraction"
    NONE = "none"
    CHURN = "churn"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, RevenueMovementType._member_map_.values()))


class PaymentType(Enum):
    """An enumeration representing different categories.

    :cvar RECURRING: "recurring"
    :vartype RECURRING: str
    :cvar ADDITIONAL: "additional"
    :vartype ADDITIONAL: str
    :cvar INSTALLMENT: "installment"
    :vartype INSTALLMENT: str
    """

    RECURRING = "recurring"
    ADDITIONAL = "additional"
    INSTALLMENT = "installment"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, PaymentType._member_map_.values()))


@JsonMap({"id_": "id"})
class GetSubscriptionPaymentsOkResponseData(BaseModel):
    """GetSubscriptionPaymentsOkResponseData

    :param id_: The ID of the payment, defaults to None
    :type id_: int, optional
    :param subscription_id: The ID of the subscription this payment is associated with, defaults to None
    :type subscription_id: int, optional
    :param deal_id: The ID of the deal this payment is associated with, defaults to None
    :type deal_id: int, optional
    :param is_active: The payment status, defaults to None
    :type is_active: bool, optional
    :param amount: The payment amount, defaults to None
    :type amount: float, optional
    :param currency: The currency of the payment, defaults to None
    :type currency: str, optional
    :param change_amount: The difference between the amount of the current payment and the previous payment. The value can be either positive or negative., defaults to None
    :type change_amount: float, optional
    :param due_at: The date when payment occurs, defaults to None
    :type due_at: str, optional
    :param revenue_movement_type: Represents the movement of revenue in comparison with the previous payment. Possible values are: `New` - first payment of the subscription. `Recurring` - no movement. `Expansion` - current payment amount > previous payment amount. `Contraction` - current payment amount < previous payment amount. `Churn` - last payment of the subscription., defaults to None
    :type revenue_movement_type: RevenueMovementType, optional
    :param payment_type: The type of the payment. Possible values are: `Recurring` - payments occur over fixed intervals of time, `Additional` - extra payment not the recurring payment of the recurring subscription, `Installment` - payment of the installment subscription., defaults to None
    :type payment_type: PaymentType, optional
    :param description: The description of the payment, defaults to None
    :type description: str, optional
    :param add_time: The creation time of the payment, defaults to None
    :type add_time: str, optional
    :param update_time: The update time of the payment, defaults to None
    :type update_time: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        subscription_id: int = None,
        deal_id: int = None,
        is_active: bool = None,
        amount: float = None,
        currency: str = None,
        change_amount: float = None,
        due_at: str = None,
        revenue_movement_type: RevenueMovementType = None,
        payment_type: PaymentType = None,
        description: str = None,
        add_time: str = None,
        update_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if subscription_id is not None:
            self.subscription_id = subscription_id
        if deal_id is not None:
            self.deal_id = deal_id
        if is_active is not None:
            self.is_active = is_active
        if amount is not None:
            self.amount = amount
        if currency is not None:
            self.currency = currency
        if change_amount is not None:
            self.change_amount = change_amount
        if due_at is not None:
            self.due_at = due_at
        if revenue_movement_type is not None:
            self.revenue_movement_type = self._enum_matching(
                revenue_movement_type,
                RevenueMovementType.list(),
                "revenue_movement_type",
            )
        if payment_type is not None:
            self.payment_type = self._enum_matching(
                payment_type, PaymentType.list(), "payment_type"
            )
        if description is not None:
            self.description = description
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time


@JsonMap({})
class GetSubscriptionPaymentsOkResponse(BaseModel):
    """GetSubscriptionPaymentsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetSubscriptionPaymentsOkResponseData], optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetSubscriptionPaymentsOkResponseData] = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetSubscriptionPaymentsOkResponseData)
