from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GetUserRoleSettingsOkResponseData(BaseModel):
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
class GetUserRoleSettingsOkResponse(BaseModel):
    """GetUserRoleSettingsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The settings for the role, defaults to None
    :type data: GetUserRoleSettingsOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: GetUserRoleSettingsOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetUserRoleSettingsOkResponseData)
