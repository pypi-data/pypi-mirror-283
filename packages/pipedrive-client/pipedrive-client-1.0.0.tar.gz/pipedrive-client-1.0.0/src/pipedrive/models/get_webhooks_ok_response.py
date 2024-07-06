from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class DataIsActive1(Enum):
    """An enumeration representing different categories.

    :cvar _0: 0
    :vartype _0: str
    :cvar _1: 1
    :vartype _1: str
    """

    _0 = 0
    _1 = 1

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, DataIsActive1._member_map_.values()))


class DataType4(Enum):
    """An enumeration representing different categories.

    :cvar GENERAL: "general"
    :vartype GENERAL: str
    :cvar APP: "app"
    :vartype APP: str
    """

    GENERAL = "general"
    APP = "app"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, DataType4._member_map_.values()))


@JsonMap({"id_": "id", "type_": "type"})
class GetWebhooksOkResponseData(BaseModel):
    """GetWebhooksOkResponseData

    :param id_: The ID of the Webhook, defaults to None
    :type id_: int, optional
    :param company_id: The ID of the company related to the Webhook, defaults to None
    :type company_id: int, optional
    :param owner_id: The ID of the user who owns the Webhook, defaults to None
    :type owner_id: int, optional
    :param user_id: The ID of the user related to the Webhook, defaults to None
    :type user_id: int, optional
    :param event_action: The Webhook action, defaults to None
    :type event_action: str, optional
    :param event_object: The Webhook object, defaults to None
    :type event_object: str, optional
    :param subscription_url: The subscription URL of the Webhook, defaults to None
    :type subscription_url: str, optional
    :param is_active: is_active, defaults to None
    :type is_active: DataIsActive1, optional
    :param add_time: The date when the Webhook was added, defaults to None
    :type add_time: str, optional
    :param remove_time: The date when the Webhook was removed (if removed), defaults to None
    :type remove_time: str, optional
    :param type_: The type of the Webhook, defaults to None
    :type type_: DataType4, optional
    :param http_auth_user: The username of the `subscription_url` of the Webhook, defaults to None
    :type http_auth_user: str, optional
    :param http_auth_password: The password of the `subscription_url` of the Webhook, defaults to None
    :type http_auth_password: str, optional
    :param additional_data: Any additional data related to the Webhook, defaults to None
    :type additional_data: dict, optional
    :param remove_reason: The removal reason of the Webhook (if removed), defaults to None
    :type remove_reason: str, optional
    :param last_delivery_time: The last delivery time of the Webhook, defaults to None
    :type last_delivery_time: str, optional
    :param last_http_status: The last delivery HTTP status of the Webhook, defaults to None
    :type last_http_status: int, optional
    :param admin_id: The ID of the admin of the Webhook, defaults to None
    :type admin_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        company_id: int = None,
        owner_id: int = None,
        user_id: int = None,
        event_action: str = None,
        event_object: str = None,
        subscription_url: str = None,
        is_active: DataIsActive1 = None,
        add_time: str = None,
        remove_time: str = None,
        type_: DataType4 = None,
        http_auth_user: str = None,
        http_auth_password: str = None,
        additional_data: dict = None,
        remove_reason: str = None,
        last_delivery_time: str = None,
        last_http_status: int = None,
        admin_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if company_id is not None:
            self.company_id = company_id
        if owner_id is not None:
            self.owner_id = owner_id
        if user_id is not None:
            self.user_id = user_id
        if event_action is not None:
            self.event_action = event_action
        if event_object is not None:
            self.event_object = event_object
        if subscription_url is not None:
            self.subscription_url = subscription_url
        if is_active is not None:
            self.is_active = self._enum_matching(
                is_active, DataIsActive1.list(), "is_active"
            )
        if add_time is not None:
            self.add_time = add_time
        if remove_time is not None:
            self.remove_time = remove_time
        if type_ is not None:
            self.type_ = self._enum_matching(type_, DataType4.list(), "type_")
        if http_auth_user is not None:
            self.http_auth_user = http_auth_user
        if http_auth_password is not None:
            self.http_auth_password = http_auth_password
        if additional_data is not None:
            self.additional_data = additional_data
        if remove_reason is not None:
            self.remove_reason = remove_reason
        if last_delivery_time is not None:
            self.last_delivery_time = last_delivery_time
        if last_http_status is not None:
            self.last_http_status = last_http_status
        if admin_id is not None:
            self.admin_id = admin_id


@JsonMap({})
class GetWebhooksOkResponse(BaseModel):
    """GetWebhooksOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param status: The status of the response, defaults to None
    :type status: str, optional
    :param data: The array of Webhooks, defaults to None
    :type data: List[GetWebhooksOkResponseData], optional
    """

    def __init__(
        self,
        success: bool = None,
        status: str = None,
        data: List[GetWebhooksOkResponseData] = None,
    ):
        if success is not None:
            self.success = success
        if status is not None:
            self.status = status
        if data is not None:
            self.data = self._define_list(data, GetWebhooksOkResponseData)
