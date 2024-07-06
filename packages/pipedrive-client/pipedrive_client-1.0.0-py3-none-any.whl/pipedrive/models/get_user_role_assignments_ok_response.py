from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"type_": "type"})
class GetUserRoleAssignmentsOkResponseData(BaseModel):
    """GetUserRoleAssignmentsOkResponseData

    :param parent_role_id: The ID of the parent role, defaults to None
    :type parent_role_id: int, optional
    :param name: The name of the role, defaults to None
    :type name: str, optional
    :param user_id: The user ID, defaults to None
    :type user_id: int, optional
    :param role_id: The role ID, defaults to None
    :type role_id: int, optional
    :param active_flag: Whether the role is active or not, defaults to None
    :type active_flag: bool, optional
    :param type_: The assignment type, defaults to None
    :type type_: str, optional
    """

    def __init__(
        self,
        parent_role_id: int = None,
        name: str = None,
        user_id: int = None,
        role_id: int = None,
        active_flag: bool = None,
        type_: str = None,
    ):
        if parent_role_id is not None:
            self.parent_role_id = parent_role_id
        if name is not None:
            self.name = name
        if user_id is not None:
            self.user_id = user_id
        if role_id is not None:
            self.role_id = role_id
        if active_flag is not None:
            self.active_flag = active_flag
        if type_ is not None:
            self.type_ = type_


@JsonMap({})
class AdditionalDataPagination21(BaseModel):
    """The pagination details in the role list

    :param start: Pagination start, defaults to None
    :type start: int, optional
    :param limit: Items shown per page, defaults to None
    :type limit: int, optional
    :param more_items_in_collection: Whether there are more list items in the collection than displayed, defaults to None
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


@JsonMap({})
class GetUserRoleAssignmentsOkResponseAdditionalData(BaseModel):
    """The additional data in the role list

    :param pagination: The pagination details in the role list, defaults to None
    :type pagination: AdditionalDataPagination21, optional
    """

    def __init__(self, pagination: AdditionalDataPagination21 = None):
        if pagination is not None:
            self.pagination = self._define_object(
                pagination, AdditionalDataPagination21
            )


@JsonMap({})
class GetUserRoleAssignmentsOkResponse(BaseModel):
    """GetUserRoleAssignmentsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The role assignments, defaults to None
    :type data: List[GetUserRoleAssignmentsOkResponseData], optional
    :param additional_data: The additional data in the role list, defaults to None
    :type additional_data: GetUserRoleAssignmentsOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetUserRoleAssignmentsOkResponseData] = None,
        additional_data: GetUserRoleAssignmentsOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetUserRoleAssignmentsOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetUserRoleAssignmentsOkResponseAdditionalData
            )
