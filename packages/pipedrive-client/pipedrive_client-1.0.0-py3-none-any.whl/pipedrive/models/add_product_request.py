from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class AddProductRequestVisibleTo(Enum):
    """An enumeration representing different categories.

    :cvar _1: "1"
    :vartype _1: str
    :cvar _3: "3"
    :vartype _3: str
    :cvar _5: "5"
    :vartype _5: str
    :cvar _7: "7"
    :vartype _7: str
    """

    _1 = "1"
    _3 = "3"
    _5 = "5"
    _7 = "7"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, AddProductRequestVisibleTo._member_map_.values())
        )


class AddProductRequestBillingFrequency(Enum):
    """An enumeration representing different categories.

    :cvar ONE_TIME: "one-time"
    :vartype ONE_TIME: str
    :cvar ANNUALLY: "annually"
    :vartype ANNUALLY: str
    :cvar SEMI_ANNUALLY: "semi-annually"
    :vartype SEMI_ANNUALLY: str
    :cvar QUARTERLY: "quarterly"
    :vartype QUARTERLY: str
    :cvar MONTHLY: "monthly"
    :vartype MONTHLY: str
    :cvar WEEKLY: "weekly"
    :vartype WEEKLY: str
    """

    ONE_TIME = "one-time"
    ANNUALLY = "annually"
    SEMI_ANNUALLY = "semi-annually"
    QUARTERLY = "quarterly"
    MONTHLY = "monthly"
    WEEKLY = "weekly"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(
                lambda x: x.value,
                AddProductRequestBillingFrequency._member_map_.values(),
            )
        )


@JsonMap({})
class AddProductRequest(BaseModel):
    """AddProductRequest

    :param name: The name of the product
    :type name: str
    :param code: The product code, defaults to None
    :type code: str, optional
    :param unit: The unit in which this product is sold, defaults to None
    :type unit: str, optional
    :param tax: The tax percentage, defaults to None
    :type tax: float, optional
    :param active_flag: Whether this product will be made active or not, defaults to None
    :type active_flag: bool, optional
    :param selectable: Whether this product can be selected in deals or not, defaults to None
    :type selectable: bool, optional
    :param visible_to: visible_to, defaults to None
    :type visible_to: AddProductRequestVisibleTo, optional
    :param owner_id: The ID of the user who will be marked as the owner of this product. When omitted, the authorized user ID will be used, defaults to None
    :type owner_id: int, optional
    :param prices: An array of objects, each containing: `currency` (string), `price` (number), `cost` (number, optional), `overhead_cost` (number, optional). Note that there can only be one price per product per currency. When `prices` is omitted altogether, a default price of 0 and a default currency based on the company's currency will be assigned., defaults to None
    :type prices: List[dict], optional
    :param billing_frequency: Only available in Advanced and above plans How often a customer is billed for access to a service or product , defaults to None
    :type billing_frequency: AddProductRequestBillingFrequency, optional
    :param billing_frequency_cycles: Only available in Advanced and above plans The number of times the billing frequency repeats for a product in a deal When `billing_frequency` is set to `one-time`, this field must be `null` For all the other values of `billing_frequency`, `null` represents a product billed indefinitely Must be a positive integer less or equal to 312 , defaults to None
    :type billing_frequency_cycles: int, optional
    """

    def __init__(
        self,
        name: str,
        code: str = None,
        unit: str = None,
        tax: float = None,
        active_flag: bool = None,
        selectable: bool = None,
        visible_to: AddProductRequestVisibleTo = None,
        owner_id: int = None,
        prices: List[dict] = None,
        billing_frequency: AddProductRequestBillingFrequency = None,
        billing_frequency_cycles: int = None,
    ):
        self.name = name
        if code is not None:
            self.code = code
        if unit is not None:
            self.unit = unit
        if tax is not None:
            self.tax = tax
        if active_flag is not None:
            self.active_flag = active_flag
        if selectable is not None:
            self.selectable = selectable
        if visible_to is not None:
            self.visible_to = self._enum_matching(
                visible_to, AddProductRequestVisibleTo.list(), "visible_to"
            )
        if owner_id is not None:
            self.owner_id = owner_id
        if prices is not None:
            self.prices = prices
        if billing_frequency is not None:
            self.billing_frequency = self._enum_matching(
                billing_frequency,
                AddProductRequestBillingFrequency.list(),
                "billing_frequency",
            )
        if billing_frequency_cycles is not None:
            self.billing_frequency_cycles = billing_frequency_cycles
