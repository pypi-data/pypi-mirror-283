from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DataRelOwnerOrgId4(BaseModel):
    """DataRelOwnerOrgId4

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
class DataRelLinkedOrgId4(BaseModel):
    """DataRelLinkedOrgId4

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
class UpdateOrganizationRelationshipOkResponseData(BaseModel):
    """UpdateOrganizationRelationshipOkResponseData

    :param id_: The ID of the organization relationship, defaults to None
    :type id_: int, optional
    :param type_: The type of the relationship, defaults to None
    :type type_: str, optional
    :param rel_owner_org_id: rel_owner_org_id, defaults to None
    :type rel_owner_org_id: DataRelOwnerOrgId4, optional
    :param rel_linked_org_id: rel_linked_org_id, defaults to None
    :type rel_linked_org_id: DataRelLinkedOrgId4, optional
    :param add_time: The creation date and time of the relationship, defaults to None
    :type add_time: str, optional
    :param update_time: The last updated date and time of the relationship, defaults to None
    :type update_time: str, optional
    :param active_flag: Whether the relationship is active or not, defaults to None
    :type active_flag: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        type_: str = None,
        rel_owner_org_id: DataRelOwnerOrgId4 = None,
        rel_linked_org_id: DataRelLinkedOrgId4 = None,
        add_time: str = None,
        update_time: str = None,
        active_flag: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if type_ is not None:
            self.type_ = type_
        if rel_owner_org_id is not None:
            self.rel_owner_org_id = self._define_object(
                rel_owner_org_id, DataRelOwnerOrgId4
            )
        if rel_linked_org_id is not None:
            self.rel_linked_org_id = self._define_object(
                rel_linked_org_id, DataRelLinkedOrgId4
            )
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if active_flag is not None:
            self.active_flag = active_flag


@JsonMap({"id_": "id"})
class OrganizationOrganizationId23(BaseModel):
    """OrganizationOrganizationId23

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
class RelatedObjectsOrganization23(BaseModel):
    """RelatedObjectsOrganization23

    :param organization_id: organization_id, defaults to None
    :type organization_id: OrganizationOrganizationId23, optional
    """

    def __init__(self, organization_id: OrganizationOrganizationId23 = None):
        if organization_id is not None:
            self.organization_id = self._define_object(
                organization_id, OrganizationOrganizationId23
            )


@JsonMap({})
class UpdateOrganizationRelationshipOkResponseRelatedObjects(BaseModel):
    """UpdateOrganizationRelationshipOkResponseRelatedObjects

    :param organization: organization, defaults to None
    :type organization: RelatedObjectsOrganization23, optional
    """

    def __init__(self, organization: RelatedObjectsOrganization23 = None):
        if organization is not None:
            self.organization = self._define_object(
                organization, RelatedObjectsOrganization23
            )


@JsonMap({})
class UpdateOrganizationRelationshipOkResponse(BaseModel):
    """UpdateOrganizationRelationshipOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: UpdateOrganizationRelationshipOkResponseData, optional
    :param related_objects: related_objects, defaults to None
    :type related_objects: UpdateOrganizationRelationshipOkResponseRelatedObjects, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: UpdateOrganizationRelationshipOkResponseData = None,
        related_objects: UpdateOrganizationRelationshipOkResponseRelatedObjects = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(
                data, UpdateOrganizationRelationshipOkResponseData
            )
        if related_objects is not None:
            self.related_objects = self._define_object(
                related_objects, UpdateOrganizationRelationshipOkResponseRelatedObjects
            )
