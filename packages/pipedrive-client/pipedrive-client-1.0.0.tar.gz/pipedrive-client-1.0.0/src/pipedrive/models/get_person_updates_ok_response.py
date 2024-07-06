from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GetPersonUpdatesOkResponseData(BaseModel):
    """GetPersonUpdatesOkResponseData

    :param object: The type of the person update. (Possible object types - personChange, note, activity, file), defaults to None
    :type object: str, optional
    :param timestamp: The creation date and time of the update, defaults to None
    :type timestamp: str, optional
    :param data: The data related to the update, defaults to None
    :type data: dict, optional
    """

    def __init__(self, object: str = None, timestamp: str = None, data: dict = None):
        if object is not None:
            self.object = object
        if timestamp is not None:
            self.timestamp = timestamp
        if data is not None:
            self.data = data


@JsonMap({})
class GetPersonUpdatesOkResponseAdditionalData(BaseModel):
    """The additional data of the list

    :param start: Pagination start, defaults to None
    :type start: int, optional
    :param limit: Items shown per page, defaults to None
    :type limit: int, optional
    :param more_items_in_collection: If there are more list items in the collection than displayed or not, defaults to None
    :type more_items_in_collection: bool, optional
    """

    def __init__(
        self,
        start: int = None,
        limit: int = None,
        more_items_in_collection: bool = None,
    ):
        if start is not None:
            self.start = start
        if limit is not None:
            self.limit = limit
        if more_items_in_collection is not None:
            self.more_items_in_collection = more_items_in_collection


@JsonMap({"id_": "id"})
class DealDealId7(BaseModel):
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
class RelatedObjectsDeal7(BaseModel):
    """RelatedObjectsDeal7

    :param deal_id: The ID of the deal which is associated with the item, defaults to None
    :type deal_id: DealDealId7, optional
    """

    def __init__(self, deal_id: DealDealId7 = None):
        if deal_id is not None:
            self.deal_id = self._define_object(deal_id, DealDealId7)


@JsonMap({"id_": "id"})
class OrganizationOrganizationId27(BaseModel):
    """OrganizationOrganizationId27

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
class RelatedObjectsOrganization27(BaseModel):
    """RelatedObjectsOrganization27

    :param organization_id: organization_id, defaults to None
    :type organization_id: OrganizationOrganizationId27, optional
    """

    def __init__(self, organization_id: OrganizationOrganizationId27 = None):
        if organization_id is not None:
            self.organization_id = self._define_object(
                organization_id, OrganizationOrganizationId27
            )


@JsonMap({"id_": "id"})
class UserUserId27(BaseModel):
    """UserUserId27

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
class RelatedObjectsUser27(BaseModel):
    """RelatedObjectsUser27

    :param user_id: user_id, defaults to None
    :type user_id: UserUserId27, optional
    """

    def __init__(self, user_id: UserUserId27 = None):
        if user_id is not None:
            self.user_id = self._define_object(user_id, UserUserId27)


@JsonMap({})
class PersonIdEmail21(BaseModel):
    """PersonIdEmail21

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
class PersonIdPhone21(BaseModel):
    """PersonIdPhone21

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
class PersonPersonId15(BaseModel):
    """PersonPersonId15

    :param active_flag: Whether the associated person is active or not, defaults to None
    :type active_flag: bool, optional
    :param id_: The ID of the person associated with the item, defaults to None
    :type id_: int, optional
    :param name: The name of the person associated with the item, defaults to None
    :type name: str, optional
    :param email: The emails of the person associated with the item, defaults to None
    :type email: List[PersonIdEmail21], optional
    :param phone: The phone numbers of the person associated with the item, defaults to None
    :type phone: List[PersonIdPhone21], optional
    :param owner_id: The ID of the owner of the person that is associated with the item, defaults to None
    :type owner_id: int, optional
    """

    def __init__(
        self,
        active_flag: bool = None,
        id_: int = None,
        name: str = None,
        email: List[PersonIdEmail21] = None,
        phone: List[PersonIdPhone21] = None,
        owner_id: int = None,
    ):
        if active_flag is not None:
            self.active_flag = active_flag
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if email is not None:
            self.email = self._define_list(email, PersonIdEmail21)
        if phone is not None:
            self.phone = self._define_list(phone, PersonIdPhone21)
        if owner_id is not None:
            self.owner_id = owner_id


@JsonMap({"person_id": "PERSON_ID"})
class RelatedObjectsPerson15(BaseModel):
    """RelatedObjectsPerson15

    :param person_id: person_id, defaults to None
    :type person_id: PersonPersonId15, optional
    """

    def __init__(self, person_id: PersonPersonId15 = None):
        if person_id is not None:
            self.person_id = self._define_object(person_id, PersonPersonId15)


@JsonMap({})
class GetPersonUpdatesOkResponseRelatedObjects(BaseModel):
    """GetPersonUpdatesOkResponseRelatedObjects

    :param deal: deal, defaults to None
    :type deal: RelatedObjectsDeal7, optional
    :param organization: organization, defaults to None
    :type organization: RelatedObjectsOrganization27, optional
    :param user: user, defaults to None
    :type user: RelatedObjectsUser27, optional
    :param person: person, defaults to None
    :type person: RelatedObjectsPerson15, optional
    """

    def __init__(
        self,
        deal: RelatedObjectsDeal7 = None,
        organization: RelatedObjectsOrganization27 = None,
        user: RelatedObjectsUser27 = None,
        person: RelatedObjectsPerson15 = None,
    ):
        if deal is not None:
            self.deal = self._define_object(deal, RelatedObjectsDeal7)
        if organization is not None:
            self.organization = self._define_object(
                organization, RelatedObjectsOrganization27
            )
        if user is not None:
            self.user = self._define_object(user, RelatedObjectsUser27)
        if person is not None:
            self.person = self._define_object(person, RelatedObjectsPerson15)


@JsonMap({})
class GetPersonUpdatesOkResponse(BaseModel):
    """GetPersonUpdatesOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetPersonUpdatesOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetPersonUpdatesOkResponseAdditionalData, optional
    :param related_objects: related_objects, defaults to None
    :type related_objects: GetPersonUpdatesOkResponseRelatedObjects, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetPersonUpdatesOkResponseData] = None,
        additional_data: GetPersonUpdatesOkResponseAdditionalData = None,
        related_objects: GetPersonUpdatesOkResponseRelatedObjects = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetPersonUpdatesOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetPersonUpdatesOkResponseAdditionalData
            )
        if related_objects is not None:
            self.related_objects = self._define_object(
                related_objects, GetPersonUpdatesOkResponseRelatedObjects
            )
