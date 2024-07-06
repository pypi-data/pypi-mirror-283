from enum import Enum


class ItemTypes(Enum):
    """An enumeration representing different categories.

    :cvar DEAL: "deal"
    :vartype DEAL: str
    :cvar PERSON: "person"
    :vartype PERSON: str
    :cvar ORGANIZATION: "organization"
    :vartype ORGANIZATION: str
    :cvar PRODUCT: "product"
    :vartype PRODUCT: str
    :cvar LEAD: "lead"
    :vartype LEAD: str
    :cvar FILE: "file"
    :vartype FILE: str
    :cvar MAIL_ATTACHMENT: "mail_attachment"
    :vartype MAIL_ATTACHMENT: str
    :cvar PROJECT: "project"
    :vartype PROJECT: str
    """

    DEAL = "deal"
    PERSON = "person"
    ORGANIZATION = "organization"
    PRODUCT = "product"
    LEAD = "lead"
    FILE = "file"
    MAIL_ATTACHMENT = "mail_attachment"
    PROJECT = "project"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ItemTypes._member_map_.values()))
