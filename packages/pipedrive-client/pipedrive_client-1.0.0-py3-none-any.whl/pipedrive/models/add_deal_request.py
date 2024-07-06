from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class AddDealRequestStatus(Enum):
    """An enumeration representing different categories.

    :cvar OPEN: "open"
    :vartype OPEN: str
    :cvar WON: "won"
    :vartype WON: str
    :cvar LOST: "lost"
    :vartype LOST: str
    :cvar DELETED: "deleted"
    :vartype DELETED: str
    """

    OPEN = "open"
    WON = "won"
    LOST = "lost"
    DELETED = "deleted"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, AddDealRequestStatus._member_map_.values()))


class AddDealRequestVisibleTo(Enum):
    """An enumeration representing different categories.

    :cvar _1: "1"
    :vartype _1: str
    :cvar _3: "3"
    :vartype _3: str
    :cvar _5: "5"
    :vartype _5: str
    :cvar _7: "7"
    :vartype _7: str
    """

    _1 = "1"
    _3 = "3"
    _5 = "5"
    _7 = "7"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, AddDealRequestVisibleTo._member_map_.values())
        )


@JsonMap({})
class AddDealRequest(BaseModel):
    """AddDealRequest

    :param title: The title of the deal
    :type title: str
    :param value: The value of the deal. If omitted, value will be set to 0., defaults to None
    :type value: str, optional
    :param label: The array of the labels IDs., defaults to None
    :type label: List[int], optional
    :param currency: The currency of the deal. Accepts a 3-character currency code. If omitted, currency will be set to the default currency of the authorized user., defaults to None
    :type currency: str, optional
    :param user_id: The ID of the user which will be the owner of the created deal. If not provided, the user making the request will be used., defaults to None
    :type user_id: int, optional
    :param person_id: The ID of a person which this deal will be linked to. If the person does not exist yet, it needs to be created first. This property is required unless `org_id` is specified., defaults to None
    :type person_id: int, optional
    :param org_id: The ID of an organization which this deal will be linked to. If the organization does not exist yet, it needs to be created first. This property is required unless `person_id` is specified., defaults to None
    :type org_id: int, optional
    :param pipeline_id: The ID of the pipeline this deal will be added to. By default, the deal will be added to the first stage of the specified pipeline. Please note that `pipeline_id` and `stage_id` should not be used together as `pipeline_id` will be ignored., defaults to None
    :type pipeline_id: int, optional
    :param stage_id: The ID of the stage this deal will be added to. Please note that a pipeline will be assigned automatically based on the `stage_id`. If omitted, the deal will be placed in the first stage of the default pipeline., defaults to None
    :type stage_id: int, optional
    :param status: open = Open, won = Won, lost = Lost, deleted = Deleted. If omitted, status will be set to open., defaults to None
    :type status: AddDealRequestStatus, optional
    :param origin_id: The optional ID to further distinguish the origin of the deal - e.g. Which API integration created this deal. If omitted, `origin_id` will be set to null., defaults to None
    :type origin_id: str, optional
    :param channel: The ID of Marketing channel this deal was created from. Provided value must be one of the channels configured for your company. You can fetch allowed values with <a href="https://developers.pipedrive.com/docs/api/v1/DealFields#getDealField" target="_blank" rel="noopener noreferrer">GET /v1/dealFields</a>. If omitted, channel will be set to null., defaults to None
    :type channel: int, optional
    :param channel_id: The optional ID to further distinguish the Marketing channel. If omitted, `channel_id` will be set to null., defaults to None
    :type channel_id: str, optional
    :param add_time: The optional creation date & time of the deal in UTC. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    :param won_time: The optional date and time of changing the deal status as won in UTC. Format: YYYY-MM-DD HH:MM:SS. Can be set only when deal `status` is already Won. Can not be used together with `lost_time`., defaults to None
    :type won_time: str, optional
    :param lost_time: The optional date and time of changing the deal status as lost in UTC. Format: YYYY-MM-DD HH:MM:SS. Can be set only when deal `status` is already Lost. Can not be used together with `won_time`., defaults to None
    :type lost_time: str, optional
    :param close_time: The optional date and time of closing the deal in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type close_time: str, optional
    :param expected_close_date: The expected close date of the deal. In ISO 8601 format: YYYY-MM-DD., defaults to None
    :type expected_close_date: str, optional
    :param probability: The success probability percentage of the deal. Used/shown only when `deal_probability` for the pipeline of the deal is enabled., defaults to None
    :type probability: float, optional
    :param lost_reason: The optional message about why the deal was lost (to be used when status = lost), defaults to None
    :type lost_reason: str, optional
    :param visible_to: visible_to, defaults to None
    :type visible_to: AddDealRequestVisibleTo, optional
    """

    def __init__(
        self,
        title: str,
        value: str = None,
        label: List[int] = None,
        currency: str = None,
        user_id: int = None,
        person_id: int = None,
        org_id: int = None,
        pipeline_id: int = None,
        stage_id: int = None,
        status: AddDealRequestStatus = None,
        origin_id: str = None,
        channel: int = None,
        channel_id: str = None,
        add_time: str = None,
        won_time: str = None,
        lost_time: str = None,
        close_time: str = None,
        expected_close_date: str = None,
        probability: float = None,
        lost_reason: str = None,
        visible_to: AddDealRequestVisibleTo = None,
    ):
        self.title = title
        if value is not None:
            self.value = value
        if label is not None:
            self.label = label
        if currency is not None:
            self.currency = currency
        if user_id is not None:
            self.user_id = user_id
        if person_id is not None:
            self.person_id = person_id
        if org_id is not None:
            self.org_id = org_id
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if stage_id is not None:
            self.stage_id = stage_id
        if status is not None:
            self.status = self._enum_matching(
                status, AddDealRequestStatus.list(), "status"
            )
        if origin_id is not None:
            self.origin_id = origin_id
        if channel is not None:
            self.channel = channel
        if channel_id is not None:
            self.channel_id = channel_id
        if add_time is not None:
            self.add_time = add_time
        if won_time is not None:
            self.won_time = won_time
        if lost_time is not None:
            self.lost_time = lost_time
        if close_time is not None:
            self.close_time = close_time
        if expected_close_date is not None:
            self.expected_close_date = expected_close_date
        if probability is not None:
            self.probability = probability
        if lost_reason is not None:
            self.lost_reason = lost_reason
        if visible_to is not None:
            self.visible_to = self._enum_matching(
                visible_to, AddDealRequestVisibleTo.list(), "visible_to"
            )
