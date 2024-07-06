from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DataRelOwnerOrgId1(BaseModel):
    """DataRelOwnerOrgId1

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
    :param value: The ID of the organization, defaults to None
    :type value: int, optional
    """

    def __init__(
        self,
        name: str = None,
        people_count: int = None,
        owner_id: int = None,
        address: str = None,
        cc_email: str = None,
        value: int = None,
    ):
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
        if value is not None:
            self.value = value


@JsonMap({})
class DataRelLinkedOrgId1(BaseModel):
    """DataRelLinkedOrgId1

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
    :param value: The ID of the organization, defaults to None
    :type value: int, optional
    """

    def __init__(
        self,
        name: str = None,
        people_count: int = None,
        owner_id: int = None,
        address: str = None,
        cc_email: str = None,
        value: int = None,
    ):
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
        if value is not None:
            self.value = value


@JsonMap({"id_": "id", "type_": "type"})
class GetOrganizationRelationshipsOkResponseData(BaseModel):
    """GetOrganizationRelationshipsOkResponseData

    :param id_: The ID of the organization relationship, defaults to None
    :type id_: int, optional
    :param type_: The type of the relationship, defaults to None
    :type type_: str, optional
    :param rel_owner_org_id: rel_owner_org_id, defaults to None
    :type rel_owner_org_id: DataRelOwnerOrgId1, optional
    :param rel_linked_org_id: rel_linked_org_id, defaults to None
    :type rel_linked_org_id: DataRelLinkedOrgId1, optional
    :param add_time: The creation date and time of the relationship, defaults to None
    :type add_time: str, optional
    :param update_time: The last updated date and time of the relationship, defaults to None
    :type update_time: str, optional
    :param active_flag: Whether the relationship is active or not, defaults to None
    :type active_flag: str, optional
    :param calculated_type: The calculated type of the relationship with the linked organization, defaults to None
    :type calculated_type: str, optional
    :param calculated_related_org_id: The ID of the linked organization, defaults to None
    :type calculated_related_org_id: int, optional
    :param related_organization_name: The name of the linked organization, defaults to None
    :type related_organization_name: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        type_: str = None,
        rel_owner_org_id: DataRelOwnerOrgId1 = None,
        rel_linked_org_id: DataRelLinkedOrgId1 = None,
        add_time: str = None,
        update_time: str = None,
        active_flag: str = None,
        calculated_type: str = None,
        calculated_related_org_id: int = None,
        related_organization_name: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if type_ is not None:
            self.type_ = type_
        if rel_owner_org_id is not None:
            self.rel_owner_org_id = self._define_object(
                rel_owner_org_id, DataRelOwnerOrgId1
            )
        if rel_linked_org_id is not None:
            self.rel_linked_org_id = self._define_object(
                rel_linked_org_id, DataRelLinkedOrgId1
            )
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if active_flag is not None:
            self.active_flag = active_flag
        if calculated_type is not None:
            self.calculated_type = calculated_type
        if calculated_related_org_id is not None:
            self.calculated_related_org_id = calculated_related_org_id
        if related_organization_name is not None:
            self.related_organization_name = related_organization_name


@JsonMap({})
class GetOrganizationRelationshipsOkResponseAdditionalData(BaseModel):
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
class OrganizationOrganizationId20(BaseModel):
    """OrganizationOrganizationId20

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
class RelatedObjectsOrganization20(BaseModel):
    """RelatedObjectsOrganization20

    :param organization_id: organization_id, defaults to None
    :type organization_id: OrganizationOrganizationId20, optional
    """

    def __init__(self, organization_id: OrganizationOrganizationId20 = None):
        if organization_id is not None:
            self.organization_id = self._define_object(
                organization_id, OrganizationOrganizationId20
            )


@JsonMap({})
class GetOrganizationRelationshipsOkResponseRelatedObjects(BaseModel):
    """GetOrganizationRelationshipsOkResponseRelatedObjects

    :param organization: organization, defaults to None
    :type organization: RelatedObjectsOrganization20, optional
    """

    def __init__(self, organization: RelatedObjectsOrganization20 = None):
        if organization is not None:
            self.organization = self._define_object(
                organization, RelatedObjectsOrganization20
            )


@JsonMap({})
class GetOrganizationRelationshipsOkResponse(BaseModel):
    """GetOrganizationRelationshipsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of organization relationships, defaults to None
    :type data: List[GetOrganizationRelationshipsOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetOrganizationRelationshipsOkResponseAdditionalData, optional
    :param related_objects: related_objects, defaults to None
    :type related_objects: GetOrganizationRelationshipsOkResponseRelatedObjects, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetOrganizationRelationshipsOkResponseData] = None,
        additional_data: GetOrganizationRelationshipsOkResponseAdditionalData = None,
        related_objects: GetOrganizationRelationshipsOkResponseRelatedObjects = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(
                data, GetOrganizationRelationshipsOkResponseData
            )
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetOrganizationRelationshipsOkResponseAdditionalData
            )
        if related_objects is not None:
            self.related_objects = self._define_object(
                related_objects, GetOrganizationRelationshipsOkResponseRelatedObjects
            )
