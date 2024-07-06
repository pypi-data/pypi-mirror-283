from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class UpdateRoleRequest(BaseModel):
    """The details of the role

    :param parent_role_id: The ID of the parent role, defaults to None
    :type parent_role_id: int, optional
    :param name: The name of the role, defaults to None
    :type name: str, optional
    """

    def __init__(self, parent_role_id: int = None, name: str = None):
        if parent_role_id is not None:
            self.parent_role_id = parent_role_id
        if name is not None:
            self.name = name
