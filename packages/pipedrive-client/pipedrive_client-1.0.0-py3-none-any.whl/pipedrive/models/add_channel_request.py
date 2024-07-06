from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class AddChannelRequestProviderType(Enum):
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
        return list(
            map(lambda x: x.value, AddChannelRequestProviderType._member_map_.values())
        )


@JsonMap({})
class AddChannelRequest(BaseModel):
    """AddChannelRequest

    :param name: The name of the channel
    :type name: str
    :param provider_channel_id: The channel ID
    :type provider_channel_id: str
    :param avatar_url: The URL for an icon that represents your channel, defaults to None
    :type avatar_url: str, optional
    :param template_support: If true, enables templates logic on UI. Requires getTemplates endpoint implemented. Find out more [here](https://pipedrive.readme.io/docs/implementing-messaging-app-extension)., defaults to None
    :type template_support: bool, optional
    :param provider_type: It controls the icons (like the icon next to the conversation), defaults to None
    :type provider_type: AddChannelRequestProviderType, optional
    """

    def __init__(
        self,
        name: str,
        provider_channel_id: str,
        avatar_url: str = None,
        template_support: bool = None,
        provider_type: AddChannelRequestProviderType = None,
    ):
        self.name = name
        self.provider_channel_id = provider_channel_id
        if avatar_url is not None:
            self.avatar_url = avatar_url
        if template_support is not None:
            self.template_support = template_support
        if provider_type is not None:
            self.provider_type = self._enum_matching(
                provider_type, AddChannelRequestProviderType.list(), "provider_type"
            )
