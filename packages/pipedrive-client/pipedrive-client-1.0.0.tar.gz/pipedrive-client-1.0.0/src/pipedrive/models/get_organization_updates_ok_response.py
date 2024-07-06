from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GetOrganizationUpdatesOkResponseData(BaseModel):
    """GetOrganizationUpdatesOkResponseData

    :param object: The type of the person update. (Possible object types - organizationChange, dealChange, file, activity), defaults to None
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
class GetOrganizationUpdatesOkResponseAdditionalData(BaseModel):
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
class OrganizationOrganizationId18(BaseModel):
    """OrganizationOrganizationId18

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
class RelatedObjectsOrganization18(BaseModel):
    """RelatedObjectsOrganization18

    :param organization_id: organization_id, defaults to None
    :type organization_id: OrganizationOrganizationId18, optional
    """

    def __init__(self, organization_id: OrganizationOrganizationId18 = None):
        if organization_id is not None:
            self.organization_id = self._define_object(
                organization_id, OrganizationOrganizationId18
            )


@JsonMap({"id_": "id"})
class UserUserId20(BaseModel):
    """UserUserId20

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
class RelatedObjectsUser20(BaseModel):
    """RelatedObjectsUser20

    :param user_id: user_id, defaults to None
    :type user_id: UserUserId20, optional
    """

    def __init__(self, user_id: UserUserId20 = None):
        if user_id is not None:
            self.user_id = self._define_object(user_id, UserUserId20)


@JsonMap({})
class GetOrganizationUpdatesOkResponseRelatedObjects(BaseModel):
    """GetOrganizationUpdatesOkResponseRelatedObjects

    :param organization: organization, defaults to None
    :type organization: RelatedObjectsOrganization18, optional
    :param user: user, defaults to None
    :type user: RelatedObjectsUser20, optional
    """

    def __init__(
        self,
        organization: RelatedObjectsOrganization18 = None,
        user: RelatedObjectsUser20 = None,
    ):
        if organization is not None:
            self.organization = self._define_object(
                organization, RelatedObjectsOrganization18
            )
        if user is not None:
            self.user = self._define_object(user, RelatedObjectsUser20)


@JsonMap({})
class GetOrganizationUpdatesOkResponse(BaseModel):
    """GetOrganizationUpdatesOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetOrganizationUpdatesOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetOrganizationUpdatesOkResponseAdditionalData, optional
    :param related_objects: related_objects, defaults to None
    :type related_objects: GetOrganizationUpdatesOkResponseRelatedObjects, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetOrganizationUpdatesOkResponseData] = None,
        additional_data: GetOrganizationUpdatesOkResponseAdditionalData = None,
        related_objects: GetOrganizationUpdatesOkResponseRelatedObjects = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetOrganizationUpdatesOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetOrganizationUpdatesOkResponseAdditionalData
            )
        if related_objects is not None:
            self.related_objects = self._define_object(
                related_objects, GetOrganizationUpdatesOkResponseRelatedObjects
            )
