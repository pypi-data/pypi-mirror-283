from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class UpdateDealProductRequestDiscountType(Enum):
    """An enumeration representing different categories.

    :cvar PERCENTAGE: "percentage"
    :vartype PERCENTAGE: str
    :cvar AMOUNT: "amount"
    :vartype AMOUNT: str
    """

    PERCENTAGE = "percentage"
    AMOUNT = "amount"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(
                lambda x: x.value,
                UpdateDealProductRequestDiscountType._member_map_.values(),
            )
        )


class UpdateDealProductRequestTaxMethod(Enum):
    """An enumeration representing different categories.

    :cvar EXCLUSIVE: "exclusive"
    :vartype EXCLUSIVE: str
    :cvar INCLUSIVE: "inclusive"
    :vartype INCLUSIVE: str
    :cvar NONE: "none"
    :vartype NONE: str
    """

    EXCLUSIVE = "exclusive"
    INCLUSIVE = "inclusive"
    NONE = "none"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(
                lambda x: x.value,
                UpdateDealProductRequestTaxMethod._member_map_.values(),
            )
        )


class UpdateDealProductRequestBillingFrequency(Enum):
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
                UpdateDealProductRequestBillingFrequency._member_map_.values(),
            )
        )


@JsonMap({})
class UpdateDealProductRequest(BaseModel):
    """UpdateDealProductRequest

    :param product_id: The ID of the product to use, defaults to None
    :type product_id: int, optional
    :param item_price: The price at which this product will be added to the deal, defaults to None
    :type item_price: float, optional
    :param quantity: How many items of this product will be added to the deal, defaults to None
    :type quantity: int, optional
    :param discount: The value of the discount. The `discount_type` field can be used to specify whether the value is an amount or a percentage, defaults to None
    :type discount: float, optional
    :param discount_type: The type of the discount's value, defaults to None
    :type discount_type: UpdateDealProductRequestDiscountType, optional
    :param product_variation_id: The ID of the product variation to use. When omitted, no variation will be used, defaults to None
    :type product_variation_id: int, optional
    :param comments: A textual comment associated with this product-deal attachment, defaults to None
    :type comments: str, optional
    :param tax: The tax percentage, defaults to None
    :type tax: float, optional
    :param tax_method: The tax option to be applied to the products. When using `inclusive`, the tax percentage will already be included in the price. When using `exclusive`, the tax will not be included in the price. When using `none`, no tax will be added. Use the `tax` field for defining the tax percentage amount, defaults to None
    :type tax_method: UpdateDealProductRequestTaxMethod, optional
    :param enabled_flag: Whether the product is enabled for a deal or not. This makes it possible to add products to a deal with a specific price and discount criteria, but keep them disabled, which refrains them from being included in the deal value calculation. When omitted, the product will be marked as enabled by default, defaults to None
    :type enabled_flag: bool, optional
    :param billing_frequency: Only available in Advanced and above plans How often a customer is billed for access to a service or product A deal can have up to 20 products attached with `billing_frequency` different than `one-time` , defaults to None
    :type billing_frequency: UpdateDealProductRequestBillingFrequency, optional
    :param billing_frequency_cycles: Only available in Advanced and above plans The number of times the billing frequency repeats for a product in a deal When `billing_frequency` is set to `one-time`, this field must be `null` For all the other values of `billing_frequency`, `null` represents a product billed indefinitely Must be a positive integer less or equal to 312 , defaults to None
    :type billing_frequency_cycles: int, optional
    :param billing_start_date: Only available in Advanced and above plans The billing start date. Must be between 15 years in the past and 15 years in the future , defaults to None
    :type billing_start_date: str, optional
    """

    def __init__(
        self,
        product_id: int = None,
        item_price: float = None,
        quantity: int = None,
        discount: float = None,
        discount_type: UpdateDealProductRequestDiscountType = None,
        product_variation_id: int = None,
        comments: str = None,
        tax: float = None,
        tax_method: UpdateDealProductRequestTaxMethod = None,
        enabled_flag: bool = None,
        billing_frequency: UpdateDealProductRequestBillingFrequency = None,
        billing_frequency_cycles: int = None,
        billing_start_date: str = None,
    ):
        if product_id is not None:
            self.product_id = product_id
        if item_price is not None:
            self.item_price = item_price
        if quantity is not None:
            self.quantity = quantity
        if discount is not None:
            self.discount = discount
        if discount_type is not None:
            self.discount_type = self._enum_matching(
                discount_type,
                UpdateDealProductRequestDiscountType.list(),
                "discount_type",
            )
        if product_variation_id is not None:
            self.product_variation_id = product_variation_id
        if comments is not None:
            self.comments = comments
        if tax is not None:
            self.tax = tax
        if tax_method is not None:
            self.tax_method = self._enum_matching(
                tax_method, UpdateDealProductRequestTaxMethod.list(), "tax_method"
            )
        if enabled_flag is not None:
            self.enabled_flag = enabled_flag
        if billing_frequency is not None:
            self.billing_frequency = self._enum_matching(
                billing_frequency,
                UpdateDealProductRequestBillingFrequency.list(),
                "billing_frequency",
            )
        if billing_frequency_cycles is not None:
            self.billing_frequency_cycles = billing_frequency_cycles
        if billing_start_date is not None:
            self.billing_start_date = billing_start_date
