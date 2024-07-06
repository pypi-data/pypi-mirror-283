from enum import Enum


class SearchItemIncludeFields(Enum):
    """An enumeration representing different categories.

    :cvar DEAL_CC_EMAIL: "deal.cc_email"
    :vartype DEAL_CC_EMAIL: str
    :cvar PERSON_PICTURE: "person.picture"
    :vartype PERSON_PICTURE: str
    :cvar PRODUCT_PRICE: "product.price"
    :vartype PRODUCT_PRICE: str
    """

    DEAL_CC_EMAIL = "deal.cc_email"
    PERSON_PICTURE = "person.picture"
    PRODUCT_PRICE = "product.price"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, SearchItemIncludeFields._member_map_.values())
        )
