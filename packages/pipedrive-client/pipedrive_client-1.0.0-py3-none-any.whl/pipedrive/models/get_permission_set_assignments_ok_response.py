from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GetPermissionSetAssignmentsOkResponseData(BaseModel):
    """GetPermissionSetAssignmentsOkResponseData

    :param user_id: The ID of the user in the permission set, defaults to None
    :type user_id: int, optional
    :param permission_set_id: The ID of the permission set, defaults to None
    :type permission_set_id: str, optional
    :param name: The name of the permission set, defaults to None
    :type name: str, optional
    """

    def __init__(
        self, user_id: int = None, permission_set_id: str = None, name: str = None
    ):
        if user_id is not None:
            self.user_id = user_id
        if permission_set_id is not None:
            self.permission_set_id = permission_set_id
        if name is not None:
            self.name = name


@JsonMap({})
class GetPermissionSetAssignmentsOkResponse(BaseModel):
    """GetPermissionSetAssignmentsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: An array of the assignments of the user, defaults to None
    :type data: List[GetPermissionSetAssignmentsOkResponseData], optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetPermissionSetAssignmentsOkResponseData] = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(
                data, GetPermissionSetAssignmentsOkResponseData
            )
