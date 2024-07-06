from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class GetRolesOkResponseData(BaseModel):
    """GetRolesOkResponseData

    :param parent_role_id: The ID of the parent role, defaults to None
    :type parent_role_id: int, optional
    :param name: The name of the role, defaults to None
    :type name: str, optional
    :param id_: The ID of the role, defaults to None
    :type id_: int, optional
    :param active_flag: Whether the role is active or not, defaults to None
    :type active_flag: bool, optional
    :param assignment_count: The number of users assigned to this role, defaults to None
    :type assignment_count: str, optional
    :param sub_role_count: The number of sub-roles, defaults to None
    :type sub_role_count: str, optional
    :param level: The level of role in the role hierarchy, defaults to None
    :type level: int, optional
    """

    def __init__(
        self,
        parent_role_id: int = None,
        name: str = None,
        id_: int = None,
        active_flag: bool = None,
        assignment_count: str = None,
        sub_role_count: str = None,
        level: int = None,
    ):
        if parent_role_id is not None:
            self.parent_role_id = parent_role_id
        if name is not None:
            self.name = name
        if id_ is not None:
            self.id_ = id_
        if active_flag is not None:
            self.active_flag = active_flag
        if assignment_count is not None:
            self.assignment_count = assignment_count
        if sub_role_count is not None:
            self.sub_role_count = sub_role_count
        if level is not None:
            self.level = level


@JsonMap({})
class AdditionalDataPagination19(BaseModel):
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
class GetRolesOkResponseAdditionalData(BaseModel):
    """The additional data in the role list

    :param pagination: The pagination details in the role list, defaults to None
    :type pagination: AdditionalDataPagination19, optional
    """

    def __init__(self, pagination: AdditionalDataPagination19 = None):
        if pagination is not None:
            self.pagination = self._define_object(
                pagination, AdditionalDataPagination19
            )


@JsonMap({})
class GetRolesOkResponse(BaseModel):
    """GetRolesOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of roles, defaults to None
    :type data: List[GetRolesOkResponseData], optional
    :param additional_data: The additional data in the role list, defaults to None
    :type additional_data: GetRolesOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetRolesOkResponseData] = None,
        additional_data: GetRolesOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetRolesOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetRolesOkResponseAdditionalData
            )
