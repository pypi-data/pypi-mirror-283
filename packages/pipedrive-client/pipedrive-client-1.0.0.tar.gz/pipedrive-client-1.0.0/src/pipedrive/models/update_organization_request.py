from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class UpdateOrganizationRequestVisibleTo(Enum):
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
            map(
                lambda x: x.value,
                UpdateOrganizationRequestVisibleTo._member_map_.values(),
            )
        )


@JsonMap({})
class UpdateOrganizationRequest(BaseModel):
    """UpdateOrganizationRequest

    :param name: The name of the organization, defaults to None
    :type name: str, optional
    :param owner_id: The ID of the user who will be marked as the owner of this organization. When omitted, the authorized user ID will be used., defaults to None
    :type owner_id: int, optional
    :param label: The ID of the label., defaults to None
    :type label: int, optional
    :param visible_to: visible_to, defaults to None
    :type visible_to: UpdateOrganizationRequestVisibleTo, optional
    """

    def __init__(
        self,
        name: str = None,
        owner_id: int = None,
        label: int = None,
        visible_to: UpdateOrganizationRequestVisibleTo = None,
    ):
        if name is not None:
            self.name = name
        if owner_id is not None:
            self.owner_id = owner_id
        if label is not None:
            self.label = label
        if visible_to is not None:
            self.visible_to = self._enum_matching(
                visible_to, UpdateOrganizationRequestVisibleTo.list(), "visible_to"
            )
