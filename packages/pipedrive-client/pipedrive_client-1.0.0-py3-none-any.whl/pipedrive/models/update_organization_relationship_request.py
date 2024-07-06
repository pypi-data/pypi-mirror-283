from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class UpdateOrganizationRelationshipRequestType(Enum):
    """An enumeration representing different categories.

    :cvar PARENT: "parent"
    :vartype PARENT: str
    :cvar RELATED: "related"
    :vartype RELATED: str
    """

    PARENT = "parent"
    RELATED = "related"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(
                lambda x: x.value,
                UpdateOrganizationRelationshipRequestType._member_map_.values(),
            )
        )


@JsonMap({"type_": "type"})
class UpdateOrganizationRelationshipRequest(BaseModel):
    """UpdateOrganizationRelationshipRequest

    :param org_id: The ID of the base organization for the returned calculated values, defaults to None
    :type org_id: int, optional
    :param type_: The type of organization relationship, defaults to None
    :type type_: UpdateOrganizationRelationshipRequestType, optional
    :param rel_owner_org_id: The owner of this relationship. If type is `parent`, then the owner is the parent and the linked organization is the daughter., defaults to None
    :type rel_owner_org_id: int, optional
    :param rel_linked_org_id: The linked organization in this relationship. If type is `parent`, then the linked organization is the daughter., defaults to None
    :type rel_linked_org_id: int, optional
    """

    def __init__(
        self,
        org_id: int = None,
        type_: UpdateOrganizationRelationshipRequestType = None,
        rel_owner_org_id: int = None,
        rel_linked_org_id: int = None,
    ):
        if org_id is not None:
            self.org_id = org_id
        if type_ is not None:
            self.type_ = self._enum_matching(
                type_, UpdateOrganizationRelationshipRequestType.list(), "type_"
            )
        if rel_owner_org_id is not None:
            self.rel_owner_org_id = rel_owner_org_id
        if rel_linked_org_id is not None:
            self.rel_linked_org_id = rel_linked_org_id
