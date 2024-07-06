from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class GetRoleOkResponseData(BaseModel):
    """GetRoleOkResponseData

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
    """

    def __init__(
        self,
        parent_role_id: int = None,
        name: str = None,
        id_: int = None,
        active_flag: bool = None,
        assignment_count: str = None,
        sub_role_count: str = None,
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


@JsonMap({})
class Settings(BaseModel):
    """The settings for the role

    :param deal_default_visibility: The default visibility level of the deals for the role, defaults to None
    :type deal_default_visibility: float, optional
    :param lead_default_visibility: The default visibility level of the leads for the role, defaults to None
    :type lead_default_visibility: float, optional
    :param org_default_visibility: The default visibility level of the organizations for the role, defaults to None
    :type org_default_visibility: float, optional
    :param person_default_visibility: The default visibility level of the people for the role, defaults to None
    :type person_default_visibility: float, optional
    :param product_default_visibility: The default visibility level of the products for the role, defaults to None
    :type product_default_visibility: float, optional
    :param deal_access_level: The access level of the deals for the role (only for default role), defaults to None
    :type deal_access_level: float, optional
    :param org_access_level: The access level of the organizations for the role (only for default role), defaults to None
    :type org_access_level: float, optional
    :param person_access_level: The access level of the people for the role (only for default role), defaults to None
    :type person_access_level: float, optional
    :param product_access_level: The access level of the products for the role (only for default role), defaults to None
    :type product_access_level: float, optional
    """

    def __init__(
        self,
        deal_default_visibility: float = None,
        lead_default_visibility: float = None,
        org_default_visibility: float = None,
        person_default_visibility: float = None,
        product_default_visibility: float = None,
        deal_access_level: float = None,
        org_access_level: float = None,
        person_access_level: float = None,
        product_access_level: float = None,
    ):
        if deal_default_visibility is not None:
            self.deal_default_visibility = deal_default_visibility
        if lead_default_visibility is not None:
            self.lead_default_visibility = lead_default_visibility
        if org_default_visibility is not None:
            self.org_default_visibility = org_default_visibility
        if person_default_visibility is not None:
            self.person_default_visibility = person_default_visibility
        if product_default_visibility is not None:
            self.product_default_visibility = product_default_visibility
        if deal_access_level is not None:
            self.deal_access_level = deal_access_level
        if org_access_level is not None:
            self.org_access_level = org_access_level
        if person_access_level is not None:
            self.person_access_level = person_access_level
        if product_access_level is not None:
            self.product_access_level = product_access_level


@JsonMap({})
class GetRoleOkResponseAdditionalData(BaseModel):
    """The additional data in the role

    :param settings: The settings for the role, defaults to None
    :type settings: Settings, optional
    """

    def __init__(self, settings: Settings = None):
        if settings is not None:
            self.settings = self._define_object(settings, Settings)


@JsonMap({})
class GetRoleOkResponse(BaseModel):
    """GetRoleOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: GetRoleOkResponseData, optional
    :param additional_data: The additional data in the role, defaults to None
    :type additional_data: GetRoleOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: GetRoleOkResponseData = None,
        additional_data: GetRoleOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetRoleOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetRoleOkResponseAdditionalData
            )
