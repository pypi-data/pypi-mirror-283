from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class DataDiscountType1(Enum):
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
        return list(map(lambda x: x.value, DataDiscountType1._member_map_.values()))


class DataTaxMethod1(Enum):
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
        return list(map(lambda x: x.value, DataTaxMethod1._member_map_.values()))


class ProductVisibleTo1(Enum):
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
        return list(map(lambda x: x.value, ProductVisibleTo1._member_map_.values()))


class ProductBillingFrequency(Enum):
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
            map(lambda x: x.value, ProductBillingFrequency._member_map_.values())
        )


@JsonMap({"id_": "id"})
class DataProduct(BaseModel):
    """DataProduct

    :param id_: The ID of the product, defaults to None
    :type id_: float, optional
    :param name: The name of the product, defaults to None
    :type name: str, optional
    :param code: The product code, defaults to None
    :type code: str, optional
    :param unit: The unit in which this product is sold, defaults to None
    :type unit: str, optional
    :param tax: The tax percentage, defaults to None
    :type tax: float, optional
    :param active_flag: Whether this product is active or not, defaults to None
    :type active_flag: bool, optional
    :param selectable: Whether this product is selected in deals or not, defaults to None
    :type selectable: bool, optional
    :param visible_to: visible_to, defaults to None
    :type visible_to: ProductVisibleTo1, optional
    :param owner_id: Information about the Pipedrive user who owns the product, defaults to None
    :type owner_id: dict, optional
    :param billing_frequency: Only available in Advanced and above plans How often a customer is billed for access to a service or product , defaults to None
    :type billing_frequency: ProductBillingFrequency, optional
    :param billing_frequency_cycles: Only available in Advanced and above plans The number of times the billing frequency repeats for a product in a deal When `billing_frequency` is set to `one-time`, this field is always `null` For all the other values of `billing_frequency`, `null` represents a product billed indefinitely Must be a positive integer less or equal to 312 , defaults to None
    :type billing_frequency_cycles: int, optional
    :param prices: Array of objects, each containing: currency (string), price (number), cost (number, optional), overhead_cost (number, optional), defaults to None
    :type prices: List[dict], optional
    """

    def __init__(
        self,
        id_: float = None,
        name: str = None,
        code: str = None,
        unit: str = None,
        tax: float = None,
        active_flag: bool = None,
        selectable: bool = None,
        visible_to: ProductVisibleTo1 = None,
        owner_id: dict = None,
        billing_frequency: ProductBillingFrequency = None,
        billing_frequency_cycles: int = None,
        prices: List[dict] = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
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
                visible_to, ProductVisibleTo1.list(), "visible_to"
            )
        if owner_id is not None:
            self.owner_id = owner_id
        if billing_frequency is not None:
            self.billing_frequency = self._enum_matching(
                billing_frequency, ProductBillingFrequency.list(), "billing_frequency"
            )
        if billing_frequency_cycles is not None:
            self.billing_frequency_cycles = billing_frequency_cycles
        if prices is not None:
            self.prices = prices


@JsonMap({"id_": "id"})
class GetDealProductsOkResponseData(BaseModel):
    """GetDealProductsOkResponseData

    :param id_: The ID of the deal-product (the ID of the product attached to the deal), defaults to None
    :type id_: int, optional
    :param deal_id: The ID of the deal, defaults to None
    :type deal_id: int, optional
    :param order_nr: The order number of the product, defaults to None
    :type order_nr: int, optional
    :param product_id: The ID of the product, defaults to None
    :type product_id: int, optional
    :param product_variation_id: The ID of the product variation, defaults to None
    :type product_variation_id: int, optional
    :param item_price: The price value of the product, defaults to None
    :type item_price: int, optional
    :param discount: The value of the discount. The `discount_type` field can be used to specify whether the value is an amount or a percentage, defaults to None
    :type discount: float, optional
    :param discount_type: The type of the discount's value, defaults to None
    :type discount_type: DataDiscountType1, optional
    :param sum: The sum of all the products attached to the deal, defaults to None
    :type sum: float, optional
    :param currency: The currency associated with the deal product, defaults to None
    :type currency: str, optional
    :param enabled_flag: Whether the product is enabled or not, defaults to None
    :type enabled_flag: bool, optional
    :param add_time: The date and time when the product was added to the deal, defaults to None
    :type add_time: str, optional
    :param last_edit: The date and time when the deal product was last edited, defaults to None
    :type last_edit: str, optional
    :param comments: The comments of the product, defaults to None
    :type comments: str, optional
    :param active_flag: Whether the product is active or not, defaults to None
    :type active_flag: bool, optional
    :param tax: The product tax, defaults to None
    :type tax: float, optional
    :param tax_method: The tax option to be applied to the products. When using `inclusive`, the tax percentage will already be included in the price. When using `exclusive`, the tax will not be included in the price. When using `none`, no tax will be added. Use the `tax` field for defining the tax percentage amount. By default, the user setting value for tax options will be used. Changing this in one product affects the rest of the products attached to the deal, defaults to None
    :type tax_method: DataTaxMethod1, optional
    :param name: The product name, defaults to None
    :type name: str, optional
    :param sum_formatted: The formatted sum of the product, defaults to None
    :type sum_formatted: str, optional
    :param quantity_formatted: The formatted quantity of the product, defaults to None
    :type quantity_formatted: str, optional
    :param quantity: The quantity of the product, defaults to None
    :type quantity: int, optional
    :param product: product, defaults to None
    :type product: DataProduct, optional
    """

    def __init__(
        self,
        id_: int = None,
        deal_id: int = None,
        order_nr: int = None,
        product_id: int = None,
        product_variation_id: int = None,
        item_price: int = None,
        discount: float = None,
        discount_type: DataDiscountType1 = None,
        sum: float = None,
        currency: str = None,
        enabled_flag: bool = None,
        add_time: str = None,
        last_edit: str = None,
        comments: str = None,
        active_flag: bool = None,
        tax: float = None,
        tax_method: DataTaxMethod1 = None,
        name: str = None,
        sum_formatted: str = None,
        quantity_formatted: str = None,
        quantity: int = None,
        product: DataProduct = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if deal_id is not None:
            self.deal_id = deal_id
        if order_nr is not None:
            self.order_nr = order_nr
        if product_id is not None:
            self.product_id = product_id
        if product_variation_id is not None:
            self.product_variation_id = product_variation_id
        if item_price is not None:
            self.item_price = item_price
        if discount is not None:
            self.discount = discount
        if discount_type is not None:
            self.discount_type = self._enum_matching(
                discount_type, DataDiscountType1.list(), "discount_type"
            )
        if sum is not None:
            self.sum = sum
        if currency is not None:
            self.currency = currency
        if enabled_flag is not None:
            self.enabled_flag = enabled_flag
        if add_time is not None:
            self.add_time = add_time
        if last_edit is not None:
            self.last_edit = last_edit
        if comments is not None:
            self.comments = comments
        if active_flag is not None:
            self.active_flag = active_flag
        if tax is not None:
            self.tax = tax
        if tax_method is not None:
            self.tax_method = self._enum_matching(
                tax_method, DataTaxMethod1.list(), "tax_method"
            )
        if name is not None:
            self.name = name
        if sum_formatted is not None:
            self.sum_formatted = sum_formatted
        if quantity_formatted is not None:
            self.quantity_formatted = quantity_formatted
        if quantity is not None:
            self.quantity = quantity
        if product is not None:
            self.product = self._define_object(product, DataProduct)


@JsonMap({})
class AdditionalDataPagination4(BaseModel):
    """Pagination details of the list

    :param start: Pagination start, defaults to None
    :type start: int, optional
    :param limit: Items shown per page, defaults to None
    :type limit: int, optional
    :param more_items_in_collection: Whether there are more list items in the collection than displayed, defaults to None
    :type more_items_in_collection: bool, optional
    :param next_start: Next pagination start, defaults to None
    :type next_start: int, optional
    """

    def __init__(
        self,
        start: int = None,
        limit: int = None,
        more_items_in_collection: bool = None,
        next_start: int = None,
    ):
        if start is not None:
            self.start = start
        if limit is not None:
            self.limit = limit
        if more_items_in_collection is not None:
            self.more_items_in_collection = more_items_in_collection
        if next_start is not None:
            self.next_start = next_start


@JsonMap({})
class GetDealProductsOkResponseAdditionalData(BaseModel):
    """GetDealProductsOkResponseAdditionalData

    :param products_quantity_total: The total quantity of the products, defaults to None
    :type products_quantity_total: int, optional
    :param products_sum_total: The total sum of the products, defaults to None
    :type products_sum_total: int, optional
    :param products_quantity_total_formatted: The total formatted quantity of the products, defaults to None
    :type products_quantity_total_formatted: str, optional
    :param products_sum_total_formatted: The total formatted sum of the products, defaults to None
    :type products_sum_total_formatted: str, optional
    :param pagination: Pagination details of the list, defaults to None
    :type pagination: AdditionalDataPagination4, optional
    """

    def __init__(
        self,
        products_quantity_total: int = None,
        products_sum_total: int = None,
        products_quantity_total_formatted: str = None,
        products_sum_total_formatted: str = None,
        pagination: AdditionalDataPagination4 = None,
    ):
        if products_quantity_total is not None:
            self.products_quantity_total = products_quantity_total
        if products_sum_total is not None:
            self.products_sum_total = products_sum_total
        if products_quantity_total_formatted is not None:
            self.products_quantity_total_formatted = products_quantity_total_formatted
        if products_sum_total_formatted is not None:
            self.products_sum_total_formatted = products_sum_total_formatted
        if pagination is not None:
            self.pagination = self._define_object(pagination, AdditionalDataPagination4)


@JsonMap({"id_": "id"})
class UserUserId14(BaseModel):
    """UserUserId14

    :param id_: The ID of the user, defaults to None
    :type id_: int, optional
    :param name: The name of the user, defaults to None
    :type name: str, optional
    :param email: The email of the user, defaults to None
    :type email: str, optional
    :param has_pic: Whether the user has picture or not. 0 = No picture, 1 = Has picture., defaults to None
    :type has_pic: int, optional
    :param pic_hash: The user picture hash, defaults to None
    :type pic_hash: str, optional
    :param active_flag: Whether the user is active or not, defaults to None
    :type active_flag: bool, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        email: str = None,
        has_pic: int = None,
        pic_hash: str = None,
        active_flag: bool = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if has_pic is not None:
            self.has_pic = has_pic
        if pic_hash is not None:
            self.pic_hash = pic_hash
        if active_flag is not None:
            self.active_flag = active_flag


@JsonMap({"user_id": "USER_ID"})
class RelatedObjectsUser14(BaseModel):
    """RelatedObjectsUser14

    :param user_id: user_id, defaults to None
    :type user_id: UserUserId14, optional
    """

    def __init__(self, user_id: UserUserId14 = None):
        if user_id is not None:
            self.user_id = self._define_object(user_id, UserUserId14)


@JsonMap({})
class GetDealProductsOkResponseRelatedObjects(BaseModel):
    """GetDealProductsOkResponseRelatedObjects

    :param user: user, defaults to None
    :type user: RelatedObjectsUser14, optional
    """

    def __init__(self, user: RelatedObjectsUser14 = None):
        if user is not None:
            self.user = self._define_object(user, RelatedObjectsUser14)


@JsonMap({})
class GetDealProductsOkResponse(BaseModel):
    """GetDealProductsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of products, defaults to None
    :type data: List[GetDealProductsOkResponseData], optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: GetDealProductsOkResponseAdditionalData, optional
    :param related_objects: related_objects, defaults to None
    :type related_objects: GetDealProductsOkResponseRelatedObjects, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetDealProductsOkResponseData] = None,
        additional_data: GetDealProductsOkResponseAdditionalData = None,
        related_objects: GetDealProductsOkResponseRelatedObjects = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetDealProductsOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetDealProductsOkResponseAdditionalData
            )
        if related_objects is not None:
            self.related_objects = self._define_object(
                related_objects, GetDealProductsOkResponseRelatedObjects
            )
