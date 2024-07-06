from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GetUserSettingsOkResponseData(BaseModel):
    """GetUserSettingsOkResponseData

    :param marketplace_team: If the vendors are allowed to be part of the Marketplace team or not, defaults to None
    :type marketplace_team: bool, optional
    :param list_limit: The number of results shown in list by default, defaults to None
    :type list_limit: float, optional
    :param beta_app: Whether beta app is enabled, defaults to None
    :type beta_app: bool, optional
    :param prevent_salesphone_callto_override: Prevent salesphone call to override, defaults to None
    :type prevent_salesphone_callto_override: bool, optional
    :param file_upload_destination: The destination of file upload, defaults to None
    :type file_upload_destination: str, optional
    :param callto_link_syntax: The call to link syntax, defaults to None
    :type callto_link_syntax: str, optional
    :param autofill_deal_expected_close_date: Whether the expected close date of the deal is filled automatically or not, defaults to None
    :type autofill_deal_expected_close_date: bool, optional
    :param person_duplicate_condition: Allow the vendors to duplicate a person, defaults to None
    :type person_duplicate_condition: str, optional
    """

    def __init__(
        self,
        marketplace_team: bool = None,
        list_limit: float = None,
        beta_app: bool = None,
        prevent_salesphone_callto_override: bool = None,
        file_upload_destination: str = None,
        callto_link_syntax: str = None,
        autofill_deal_expected_close_date: bool = None,
        person_duplicate_condition: str = None,
    ):
        if marketplace_team is not None:
            self.marketplace_team = marketplace_team
        if list_limit is not None:
            self.list_limit = list_limit
        if beta_app is not None:
            self.beta_app = beta_app
        if prevent_salesphone_callto_override is not None:
            self.prevent_salesphone_callto_override = prevent_salesphone_callto_override
        if file_upload_destination is not None:
            self.file_upload_destination = file_upload_destination
        if callto_link_syntax is not None:
            self.callto_link_syntax = callto_link_syntax
        if autofill_deal_expected_close_date is not None:
            self.autofill_deal_expected_close_date = autofill_deal_expected_close_date
        if person_duplicate_condition is not None:
            self.person_duplicate_condition = person_duplicate_condition


@JsonMap({})
class GetUserSettingsOkResponse(BaseModel):
    """GetUserSettingsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: GetUserSettingsOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: GetUserSettingsOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetUserSettingsOkResponseData)
