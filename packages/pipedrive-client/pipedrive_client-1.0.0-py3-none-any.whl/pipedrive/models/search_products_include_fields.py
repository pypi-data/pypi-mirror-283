from enum import Enum


class SearchProductsIncludeFields(Enum):
    """An enumeration representing different categories.

    :cvar PRODUCT_PRICE: "product.price"
    :vartype PRODUCT_PRICE: str
    """

    PRODUCT_PRICE = "product.price"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, SearchProductsIncludeFields._member_map_.values())
        )
