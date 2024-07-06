from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AddPersonRequestEmail(BaseModel):
    """AddPersonRequestEmail

    :param value: The email, defaults to None
    :type value: str, optional
    :param primary: Boolean that indicates if email is primary for the person or not, defaults to None
    :type primary: bool, optional
    :param label: The label that indicates the type of the email. (Possible values - work, home or other), defaults to None
    :type label: str, optional
    """

    def __init__(self, value: str = None, primary: bool = None, label: str = None):
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary
        if label is not None:
            self.label = label


@JsonMap({})
class AddPersonRequestPhone(BaseModel):
    """AddPersonRequestPhone

    :param value: The phone number, defaults to None
    :type value: str, optional
    :param primary: Boolean that indicates if phone number is primary for the person or not, defaults to None
    :type primary: bool, optional
    :param label: The label that indicates the type of the phone number. (Possible values - work, home, mobile or other), defaults to None
    :type label: str, optional
    """

    def __init__(self, value: str = None, primary: bool = None, label: str = None):
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary
        if label is not None:
            self.label = label


class AddPersonRequestVisibleTo(Enum):
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
            map(lambda x: x.value, AddPersonRequestVisibleTo._member_map_.values())
        )


class AddPersonRequestMarketingStatus(Enum):
    """An enumeration representing different categories.

    :cvar NO_CONSENT: "no_consent"
    :vartype NO_CONSENT: str
    :cvar UNSUBSCRIBED: "unsubscribed"
    :vartype UNSUBSCRIBED: str
    :cvar SUBSCRIBED: "subscribed"
    :vartype SUBSCRIBED: str
    :cvar ARCHIVED: "archived"
    :vartype ARCHIVED: str
    """

    NO_CONSENT = "no_consent"
    UNSUBSCRIBED = "unsubscribed"
    SUBSCRIBED = "subscribed"
    ARCHIVED = "archived"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(
                lambda x: x.value, AddPersonRequestMarketingStatus._member_map_.values()
            )
        )


@JsonMap({})
class AddPersonRequest(BaseModel):
    """AddPersonRequest

    :param name: The name of the person
    :type name: str
    :param owner_id: The ID of the user who will be marked as the owner of this person. When omitted, the authorized user ID will be used., defaults to None
    :type owner_id: int, optional
    :param org_id: The ID of the organization this person will belong to, defaults to None
    :type org_id: int, optional
    :param email: An email address as a string or an array of email objects related to the person. The structure of the array is as follows: `[{ "value": "mail@example.com", "primary": "true", "label": "main" }]`. Please note that only `value` is required., defaults to None
    :type email: List[AddPersonRequestEmail], optional
    :param phone: A phone number supplied as a string or an array of phone objects related to the person. The structure of the array is as follows: `[{ "value": "12345", "primary": "true", "label": "mobile" }]`. Please note that only `value` is required., defaults to None
    :type phone: List[AddPersonRequestPhone], optional
    :param label: The ID of the label., defaults to None
    :type label: int, optional
    :param visible_to: visible_to, defaults to None
    :type visible_to: AddPersonRequestVisibleTo, optional
    :param marketing_status: marketing_status, defaults to None
    :type marketing_status: AddPersonRequestMarketingStatus, optional
    :param add_time: The optional creation date & time of the person in UTC. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    """

    def __init__(
        self,
        name: str,
        owner_id: int = None,
        org_id: int = None,
        email: List[AddPersonRequestEmail] = None,
        phone: List[AddPersonRequestPhone] = None,
        label: int = None,
        visible_to: AddPersonRequestVisibleTo = None,
        marketing_status: AddPersonRequestMarketingStatus = None,
        add_time: str = None,
    ):
        self.name = name
        if owner_id is not None:
            self.owner_id = owner_id
        if org_id is not None:
            self.org_id = org_id
        if email is not None:
            self.email = self._define_list(email, AddPersonRequestEmail)
        if phone is not None:
            self.phone = self._define_list(phone, AddPersonRequestPhone)
        if label is not None:
            self.label = label
        if visible_to is not None:
            self.visible_to = self._enum_matching(
                visible_to, AddPersonRequestVisibleTo.list(), "visible_to"
            )
        if marketing_status is not None:
            self.marketing_status = self._enum_matching(
                marketing_status,
                AddPersonRequestMarketingStatus.list(),
                "marketing_status",
            )
        if add_time is not None:
            self.add_time = add_time
