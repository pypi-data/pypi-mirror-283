from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AddRoleRequest(BaseModel):
    """The details of the role

    :param name: The name of the role
    :type name: str
    :param parent_role_id: The ID of the parent role, defaults to None
    :type parent_role_id: int, optional
    """

    def __init__(self, name: str, parent_role_id: int = None):
        self.name = name
        if parent_role_id is not None:
            self.parent_role_id = parent_role_id
