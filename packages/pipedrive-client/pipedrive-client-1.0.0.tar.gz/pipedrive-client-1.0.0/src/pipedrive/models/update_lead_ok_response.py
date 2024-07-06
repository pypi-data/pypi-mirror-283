from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DataValue4(BaseModel):
    """The potential value of the lead represented by a JSON object: `{ "amount": 200, "currency": "EUR" }`. Both amount and currency are required.

    :param amount: amount
    :type amount: float
    :param currency: currency
    :type currency: str
    """

    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency


class DataVisibleTo4(Enum):
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
        return list(map(lambda x: x.value, DataVisibleTo4._member_map_.values()))


@JsonMap({"id_": "id"})
class UpdateLeadOkResponseData(BaseModel):
    """UpdateLeadOkResponseData

    :param id_: The unique ID of the lead in the UUID format, defaults to None
    :type id_: str, optional
    :param title: The title of the lead, defaults to None
    :type title: str, optional
    :param owner_id: The ID of the user who owns the lead, defaults to None
    :type owner_id: int, optional
    :param creator_id: The ID of the user who created the lead, defaults to None
    :type creator_id: int, optional
    :param label_ids: The IDs of the lead labels which are associated with the lead, defaults to None
    :type label_ids: List[str], optional
    :param person_id: The ID of a person which this lead is linked to, defaults to None
    :type person_id: int, optional
    :param organization_id: The ID of an organization which this lead is linked to, defaults to None
    :type organization_id: int, optional
    :param source_name: Defines where the lead comes from. Will be `API` if the lead was created through the Public API and will be `Manually created` if the lead was created manually through the UI. , defaults to None
    :type source_name: str, optional
    :param origin: The way this Lead was created. `origin` field is set by Pipedrive when Lead is created and cannot be changed., defaults to None
    :type origin: str, optional
    :param origin_id: The optional ID to further distinguish the origin of the lead - e.g. Which API integration created this Lead., defaults to None
    :type origin_id: str, optional
    :param channel: The ID of your Marketing channel this Lead was created from. Recognized Marketing channels can be configured in your <a href="https://app.pipedrive.com/settings/fields" target="_blank" rel="noopener noreferrer">Company settings</a>., defaults to None
    :type channel: int, optional
    :param channel_id: The optional ID to further distinguish the Marketing channel., defaults to None
    :type channel_id: str, optional
    :param is_archived: A flag indicating whether the lead is archived or not, defaults to None
    :type is_archived: bool, optional
    :param was_seen: A flag indicating whether the lead was seen by someone in the Pipedrive UI, defaults to None
    :type was_seen: bool, optional
    :param value: The potential value of the lead represented by a JSON object: `{ "amount": 200, "currency": "EUR" }`. Both amount and currency are required., defaults to None
    :type value: DataValue4, optional
    :param expected_close_date: The date of when the deal which will be created from the lead is expected to be closed. In ISO 8601 format: YYYY-MM-DD., defaults to None
    :type expected_close_date: str, optional
    :param next_activity_id: The ID of the next activity associated with the lead, defaults to None
    :type next_activity_id: int, optional
    :param add_time: The date and time of when the lead was created. In ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ., defaults to None
    :type add_time: str, optional
    :param update_time: The date and time of when the lead was last updated. In ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ., defaults to None
    :type update_time: str, optional
    :param visible_to: visible_to, defaults to None
    :type visible_to: DataVisibleTo4, optional
    :param cc_email: The BCC email of the lead, defaults to None
    :type cc_email: str, optional
    """

    def __init__(
        self,
        id_: str = None,
        title: str = None,
        owner_id: int = None,
        creator_id: int = None,
        label_ids: List[str] = None,
        person_id: int = None,
        organization_id: int = None,
        source_name: str = None,
        origin: str = None,
        origin_id: str = None,
        channel: int = None,
        channel_id: str = None,
        is_archived: bool = None,
        was_seen: bool = None,
        value: DataValue4 = None,
        expected_close_date: str = None,
        next_activity_id: int = None,
        add_time: str = None,
        update_time: str = None,
        visible_to: DataVisibleTo4 = None,
        cc_email: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if title is not None:
            self.title = title
        if owner_id is not None:
            self.owner_id = owner_id
        if creator_id is not None:
            self.creator_id = creator_id
        if label_ids is not None:
            self.label_ids = label_ids
        if person_id is not None:
            self.person_id = person_id
        if organization_id is not None:
            self.organization_id = organization_id
        if source_name is not None:
            self.source_name = source_name
        if origin is not None:
            self.origin = origin
        if origin_id is not None:
            self.origin_id = origin_id
        if channel is not None:
            self.channel = channel
        if channel_id is not None:
            self.channel_id = channel_id
        if is_archived is not None:
            self.is_archived = is_archived
        if was_seen is not None:
            self.was_seen = was_seen
        if value is not None:
            self.value = self._define_object(value, DataValue4)
        if expected_close_date is not None:
            self.expected_close_date = expected_close_date
        if next_activity_id is not None:
            self.next_activity_id = next_activity_id
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if visible_to is not None:
            self.visible_to = self._enum_matching(
                visible_to, DataVisibleTo4.list(), "visible_to"
            )
        if cc_email is not None:
            self.cc_email = cc_email


@JsonMap({})
class UpdateLeadOkResponse(BaseModel):
    """UpdateLeadOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: UpdateLeadOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: UpdateLeadOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, UpdateLeadOkResponseData)
