from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class EventAction(Enum):
    """An enumeration representing different categories.

    :cvar ADDED: "added"
    :vartype ADDED: str
    :cvar UPDATED: "updated"
    :vartype UPDATED: str
    :cvar MERGED: "merged"
    :vartype MERGED: str
    :cvar DELETED: "deleted"
    :vartype DELETED: str
    :cvar _: "*"
    :vartype _: str
    """

    ADDED = "added"
    UPDATED = "updated"
    MERGED = "merged"
    DELETED = "deleted"
    _ = "*"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, EventAction._member_map_.values()))


class EventObject(Enum):
    """An enumeration representing different categories.

    :cvar ACTIVITY: "activity"
    :vartype ACTIVITY: str
    :cvar ACTIVITYTYPE: "activityType"
    :vartype ACTIVITYTYPE: str
    :cvar DEAL: "deal"
    :vartype DEAL: str
    :cvar NOTE: "note"
    :vartype NOTE: str
    :cvar ORGANIZATION: "organization"
    :vartype ORGANIZATION: str
    :cvar PERSON: "person"
    :vartype PERSON: str
    :cvar PIPELINE: "pipeline"
    :vartype PIPELINE: str
    :cvar PRODUCT: "product"
    :vartype PRODUCT: str
    :cvar STAGE: "stage"
    :vartype STAGE: str
    :cvar USER: "user"
    :vartype USER: str
    :cvar _: "*"
    :vartype _: str
    """

    ACTIVITY = "activity"
    ACTIVITYTYPE = "activityType"
    DEAL = "deal"
    NOTE = "note"
    ORGANIZATION = "organization"
    PERSON = "person"
    PIPELINE = "pipeline"
    PRODUCT = "product"
    STAGE = "stage"
    USER = "user"
    _ = "*"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, EventObject._member_map_.values()))


class Version(Enum):
    """An enumeration representing different categories.

    :cvar _1_0: "1.0"
    :vartype _1_0: str
    :cvar _2_0: "2.0"
    :vartype _2_0: str
    """

    _1_0 = "1.0"
    _2_0 = "2.0"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Version._member_map_.values()))


@JsonMap({})
class AddWebhookRequest(BaseModel):
    """AddWebhookRequest

    :param subscription_url: A full, valid, publicly accessible URL which determines where to send the notifications. Please note that you cannot use Pipedrive API endpoints as the `subscription_url` and the chosen URL must not redirect to another link.
    :type subscription_url: str
    :param event_action: The type of action to receive notifications about. Wildcard will match all supported actions.
    :type event_action: EventAction
    :param event_object: The type of object to receive notifications about. Wildcard will match all supported objects.
    :type event_object: EventObject
    :param user_id: The ID of the user that this webhook will be authorized with. You have the option to use a different user's `user_id`. If it is not set, the current user's `user_id` will be used. As each webhook event is checked against a user's permissions, the webhook will only be sent if the user has access to the specified object(s). If you want to receive notifications for all events, please use a top-level admin user’s `user_id`., defaults to None
    :type user_id: int, optional
    :param http_auth_user: The HTTP basic auth username of the subscription URL endpoint (if required), defaults to None
    :type http_auth_user: str, optional
    :param http_auth_password: The HTTP basic auth password of the subscription URL endpoint (if required), defaults to None
    :type http_auth_password: str, optional
    :param version: The webhook's version, defaults to None
    :type version: Version, optional
    """

    def __init__(
        self,
        subscription_url: str,
        event_action: EventAction,
        event_object: EventObject,
        user_id: int = None,
        http_auth_user: str = None,
        http_auth_password: str = None,
        version: Version = None,
    ):
        self.subscription_url = subscription_url
        self.event_action = self._enum_matching(
            event_action, EventAction.list(), "event_action"
        )
        self.event_object = self._enum_matching(
            event_object, EventObject.list(), "event_object"
        )
        if user_id is not None:
            self.user_id = user_id
        if http_auth_user is not None:
            self.http_auth_user = http_auth_user
        if http_auth_password is not None:
            self.http_auth_password = http_auth_password
        if version is not None:
            self.version = self._enum_matching(version, Version.list(), "version")
