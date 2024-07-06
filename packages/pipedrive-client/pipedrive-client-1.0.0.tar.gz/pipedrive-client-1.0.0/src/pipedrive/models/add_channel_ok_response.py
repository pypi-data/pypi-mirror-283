from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class DataProviderType(Enum):
    """An enumeration representing different categories.

    :cvar FACEBOOK: "facebook"
    :vartype FACEBOOK: str
    :cvar WHATSAPP: "whatsapp"
    :vartype WHATSAPP: str
    :cvar OTHER: "other"
    :vartype OTHER: str
    """

    FACEBOOK = "facebook"
    WHATSAPP = "whatsapp"
    OTHER = "other"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, DataProviderType._member_map_.values()))


@JsonMap({"id_": "id"})
class AddChannelOkResponseData(BaseModel):
    """AddChannelOkResponseData

    :param id_: The unique channel ID used internally in omnichannel-api and the frontend of the extension, defaults to None
    :type id_: str, optional
    :param name: The name of the channel, defaults to None
    :type name: str, optional
    :param avatar_url: The URL for an icon that represents your channel, defaults to None
    :type avatar_url: str, optional
    :param provider_channel_id: The channel ID you specified while creating the channel, defaults to None
    :type provider_channel_id: str, optional
    :param marketplace_client_id: The client_id of your app in Pipedrive marketplace, defaults to None
    :type marketplace_client_id: str, optional
    :param pd_company_id: The ID of the user's company in Pipedrive, defaults to None
    :type pd_company_id: int, optional
    :param pd_user_id: The ID of the user in Pipedrive, defaults to None
    :type pd_user_id: int, optional
    :param created_at: The date and time when your channel was created in the API, defaults to None
    :type created_at: str, optional
    :param provider_type: Value of the provider_type sent to this endpoint, defaults to None
    :type provider_type: DataProviderType, optional
    :param template_support: Value of the template_support sent to this endpoint, defaults to None
    :type template_support: bool, optional
    """

    def __init__(
        self,
        id_: str = None,
        name: str = None,
        avatar_url: str = None,
        provider_channel_id: str = None,
        marketplace_client_id: str = None,
        pd_company_id: int = None,
        pd_user_id: int = None,
        created_at: str = None,
        provider_type: DataProviderType = None,
        template_support: bool = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if avatar_url is not None:
            self.avatar_url = avatar_url
        if provider_channel_id is not None:
            self.provider_channel_id = provider_channel_id
        if marketplace_client_id is not None:
            self.marketplace_client_id = marketplace_client_id
        if pd_company_id is not None:
            self.pd_company_id = pd_company_id
        if pd_user_id is not None:
            self.pd_user_id = pd_user_id
        if created_at is not None:
            self.created_at = created_at
        if provider_type is not None:
            self.provider_type = self._enum_matching(
                provider_type, DataProviderType.list(), "provider_type"
            )
        if template_support is not None:
            self.template_support = template_support


@JsonMap({})
class AddChannelOkResponse(BaseModel):
    """AddChannelOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: AddChannelOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: AddChannelOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, AddChannelOkResponseData)
