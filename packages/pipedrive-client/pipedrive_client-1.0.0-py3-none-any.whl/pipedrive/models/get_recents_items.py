from enum import Enum


class GetRecentsItems(Enum):
    """An enumeration representing different categories.

    :cvar ACTIVITY: "activity"
    :vartype ACTIVITY: str
    :cvar ACTIVITYTYPE: "activityType"
    :vartype ACTIVITYTYPE: str
    :cvar DEAL: "deal"
    :vartype DEAL: str
    :cvar FILE: "file"
    :vartype FILE: str
    :cvar FILTER: "filter"
    :vartype FILTER: str
    :cvar NOTE: "note"
    :vartype NOTE: str
    :cvar PERSON: "person"
    :vartype PERSON: str
    :cvar ORGANIZATION: "organization"
    :vartype ORGANIZATION: str
    :cvar PIPELINE: "pipeline"
    :vartype PIPELINE: str
    :cvar PRODUCT: "product"
    :vartype PRODUCT: str
    :cvar STAGE: "stage"
    :vartype STAGE: str
    :cvar USER: "user"
    :vartype USER: str
    """

    ACTIVITY = "activity"
    ACTIVITYTYPE = "activityType"
    DEAL = "deal"
    FILE = "file"
    FILTER = "filter"
    NOTE = "note"
    PERSON = "person"
    ORGANIZATION = "organization"
    PIPELINE = "pipeline"
    PRODUCT = "product"
    STAGE = "stage"
    USER = "user"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, GetRecentsItems._member_map_.values()))
