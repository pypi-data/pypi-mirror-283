from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AddRoleAssignmentOkResponseData(BaseModel):
    """The response data

    :param user_id: The ID of the user that was added to the role, defaults to None
    :type user_id: int, optional
    :param role_id: The ID of the role the user was added to, defaults to None
    :type role_id: int, optional
    """

    def __init__(self, user_id: int = None, role_id: int = None):
        if user_id is not None:
            self.user_id = user_id
        if role_id is not None:
            self.role_id = role_id


@JsonMap({})
class AddRoleAssignmentOkResponse(BaseModel):
    """AddRoleAssignmentOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The response data, defaults to None
    :type data: AddRoleAssignmentOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: AddRoleAssignmentOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, AddRoleAssignmentOkResponseData)
