from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class AddOrganizationRelationshipRequestType(Enum):
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
                AddOrganizationRelationshipRequestType._member_map_.values(),
            )
        )


@JsonMap({"type_": "type"})
class AddOrganizationRelationshipRequest(BaseModel):
    """AddOrganizationRelationshipRequest

    :param org_id: The ID of the base organization for the returned calculated values, defaults to None
    :type org_id: int, optional
    :param type_: The type of organization relationship
    :type type_: AddOrganizationRelationshipRequestType
    :param rel_owner_org_id: The owner of the relationship. If type is `parent`, then the owner is the parent and the linked organization is the daughter.
    :type rel_owner_org_id: int
    :param rel_linked_org_id: The linked organization in the relationship. If type is `parent`, then the linked organization is the daughter.
    :type rel_linked_org_id: int
    """

    def __init__(
        self,
        type_: AddOrganizationRelationshipRequestType,
        rel_owner_org_id: int,
        rel_linked_org_id: int,
        org_id: int = None,
    ):
        if org_id is not None:
            self.org_id = org_id
        self.type_ = self._enum_matching(
            type_, AddOrganizationRelationshipRequestType.list(), "type_"
        )
        self.rel_owner_org_id = rel_owner_org_id
        self.rel_linked_org_id = rel_linked_org_id
