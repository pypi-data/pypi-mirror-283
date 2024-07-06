from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class DataVisibleTo7(Enum):
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
        return list(map(lambda x: x.value, DataVisibleTo7._member_map_.values()))


class DataBillingFrequency5(Enum):
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
        return list(map(lambda x: x.value, DataBillingFrequency5._member_map_.values()))


@JsonMap({"id_": "id"})
class GetProductOkResponseData(BaseModel):
    """GetProductOkResponseData

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
    :type visible_to: DataVisibleTo7, optional
    :param owner_id: Information about the Pipedrive user who owns the product, defaults to None
    :type owner_id: dict, optional
    :param billing_frequency: Only available in Advanced and above plans How often a customer is billed for access to a service or product , defaults to None
    :type billing_frequency: DataBillingFrequency5, optional
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
        visible_to: DataVisibleTo7 = None,
        owner_id: dict = None,
        billing_frequency: DataBillingFrequency5 = None,
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
                visible_to, DataVisibleTo7.list(), "visible_to"
            )
        if owner_id is not None:
            self.owner_id = owner_id
        if billing_frequency is not None:
            self.billing_frequency = self._enum_matching(
                billing_frequency, DataBillingFrequency5.list(), "billing_frequency"
            )
        if billing_frequency_cycles is not None:
            self.billing_frequency_cycles = billing_frequency_cycles
        if prices is not None:
            self.prices = prices


@JsonMap({"id_": "id"})
class UserUserId31(BaseModel):
    """UserUserId31

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
class RelatedObjectsUser31(BaseModel):
    """RelatedObjectsUser31

    :param user_id: user_id, defaults to None
    :type user_id: UserUserId31, optional
    """

    def __init__(self, user_id: UserUserId31 = None):
        if user_id is not None:
            self.user_id = self._define_object(user_id, UserUserId31)


@JsonMap({"id_": "id"})
class DealDealId11(BaseModel):
    """The ID of the deal which is associated with the item

    :param id_: The ID of the deal associated with the item, defaults to None
    :type id_: int, optional
    :param title: The title of the deal associated with the item, defaults to None
    :type title: str, optional
    :param status: The status of the deal associated with the item, defaults to None
    :type status: str, optional
    :param value: The value of the deal that is associated with the item, defaults to None
    :type value: float, optional
    :param currency: The currency of the deal value, defaults to None
    :type currency: str, optional
    :param stage_id: The ID of the stage the deal is currently at, defaults to None
    :type stage_id: int, optional
    :param pipeline_id: The ID of the pipeline the deal is in, defaults to None
    :type pipeline_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        title: str = None,
        status: str = None,
        value: float = None,
        currency: str = None,
        stage_id: int = None,
        pipeline_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if title is not None:
            self.title = title
        if status is not None:
            self.status = status
        if value is not None:
            self.value = value
        if currency is not None:
            self.currency = currency
        if stage_id is not None:
            self.stage_id = stage_id
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id


@JsonMap({"deal_id": "DEAL_ID"})
class RelatedObjectsDeal11(BaseModel):
    """RelatedObjectsDeal11

    :param deal_id: The ID of the deal which is associated with the item, defaults to None
    :type deal_id: DealDealId11, optional
    """

    def __init__(self, deal_id: DealDealId11 = None):
        if deal_id is not None:
            self.deal_id = self._define_object(deal_id, DealDealId11)


@JsonMap({})
class PersonIdEmail25(BaseModel):
    """PersonIdEmail25

    :param label: The type of the email, defaults to None
    :type label: str, optional
    :param value: The email of the associated person, defaults to None
    :type value: str, optional
    :param primary: Whether this is the primary email or not, defaults to None
    :type primary: bool, optional
    """

    def __init__(self, label: str = None, value: str = None, primary: bool = None):
        if label is not None:
            self.label = label
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary


@JsonMap({})
class PersonIdPhone25(BaseModel):
    """PersonIdPhone25

    :param label: The type of the phone number, defaults to None
    :type label: str, optional
    :param value: The phone number of the person associated with the item, defaults to None
    :type value: str, optional
    :param primary: Whether this is the primary phone number or not, defaults to None
    :type primary: bool, optional
    """

    def __init__(self, label: str = None, value: str = None, primary: bool = None):
        if label is not None:
            self.label = label
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary


@JsonMap({"id_": "id"})
class PersonPersonId19(BaseModel):
    """PersonPersonId19

    :param id_: The ID of the person associated with the item, defaults to None
    :type id_: int, optional
    :param name: The name of the person associated with the item, defaults to None
    :type name: str, optional
    :param email: The emails of the person associated with the item, defaults to None
    :type email: List[PersonIdEmail25], optional
    :param phone: The phone numbers of the person associated with the item, defaults to None
    :type phone: List[PersonIdPhone25], optional
    :param owner_id: The ID of the owner of the person that is associated with the item, defaults to None
    :type owner_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        email: List[PersonIdEmail25] = None,
        phone: List[PersonIdPhone25] = None,
        owner_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if email is not None:
            self.email = self._define_list(email, PersonIdEmail25)
        if phone is not None:
            self.phone = self._define_list(phone, PersonIdPhone25)
        if owner_id is not None:
            self.owner_id = owner_id


@JsonMap({"person_id": "PERSON_ID"})
class RelatedObjectsPerson19(BaseModel):
    """RelatedObjectsPerson19

    :param person_id: person_id, defaults to None
    :type person_id: PersonPersonId19, optional
    """

    def __init__(self, person_id: PersonPersonId19 = None):
        if person_id is not None:
            self.person_id = self._define_object(person_id, PersonPersonId19)


@JsonMap({"id_": "id"})
class OrganizationOrganizationId31(BaseModel):
    """OrganizationOrganizationId31

    :param id_: The ID of the organization associated with the item, defaults to None
    :type id_: int, optional
    :param name: The name of the organization associated with the item, defaults to None
    :type name: str, optional
    :param people_count: The number of people connected with the organization that is associated with the item, defaults to None
    :type people_count: int, optional
    :param owner_id: The ID of the owner of the organization that is associated with the item, defaults to None
    :type owner_id: int, optional
    :param address: The address of the organization, defaults to None
    :type address: str, optional
    :param cc_email: The BCC email of the organization associated with the item, defaults to None
    :type cc_email: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        people_count: int = None,
        owner_id: int = None,
        address: str = None,
        cc_email: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if people_count is not None:
            self.people_count = people_count
        if owner_id is not None:
            self.owner_id = owner_id
        if address is not None:
            self.address = address
        if cc_email is not None:
            self.cc_email = cc_email


@JsonMap({"organization_id": "ORGANIZATION_ID"})
class RelatedObjectsOrganization31(BaseModel):
    """RelatedObjectsOrganization31

    :param organization_id: organization_id, defaults to None
    :type organization_id: OrganizationOrganizationId31, optional
    """

    def __init__(self, organization_id: OrganizationOrganizationId31 = None):
        if organization_id is not None:
            self.organization_id = self._define_object(
                organization_id, OrganizationOrganizationId31
            )


@JsonMap({})
class GetProductOkResponseRelatedObjects(BaseModel):
    """GetProductOkResponseRelatedObjects

    :param user: user, defaults to None
    :type user: RelatedObjectsUser31, optional
    :param deal: deal, defaults to None
    :type deal: RelatedObjectsDeal11, optional
    :param person: person, defaults to None
    :type person: RelatedObjectsPerson19, optional
    :param organization: organization, defaults to None
    :type organization: RelatedObjectsOrganization31, optional
    """

    def __init__(
        self,
        user: RelatedObjectsUser31 = None,
        deal: RelatedObjectsDeal11 = None,
        person: RelatedObjectsPerson19 = None,
        organization: RelatedObjectsOrganization31 = None,
    ):
        if user is not None:
            self.user = self._define_object(user, RelatedObjectsUser31)
        if deal is not None:
            self.deal = self._define_object(deal, RelatedObjectsDeal11)
        if person is not None:
            self.person = self._define_object(person, RelatedObjectsPerson19)
        if organization is not None:
            self.organization = self._define_object(
                organization, RelatedObjectsOrganization31
            )


@JsonMap({})
class GetProductOkResponse(BaseModel):
    """GetProductOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: GetProductOkResponseData, optional
    :param related_objects: related_objects, defaults to None
    :type related_objects: GetProductOkResponseRelatedObjects, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: GetProductOkResponseData = None,
        related_objects: GetProductOkResponseRelatedObjects = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetProductOkResponseData)
        if related_objects is not None:
            self.related_objects = self._define_object(
                related_objects, GetProductOkResponseRelatedObjects
            )
