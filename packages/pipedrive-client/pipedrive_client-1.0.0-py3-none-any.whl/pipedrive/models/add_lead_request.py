from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AddLeadRequestValue(BaseModel):
    """The potential value of the lead represented by a JSON object: `{ "amount": 200, "currency": "EUR" }`. Both amount and currency are required.

    :param amount: amount
    :type amount: float
    :param currency: currency
    :type currency: str
    """

    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency


class AddLeadRequestVisibleTo(Enum):
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
            map(lambda x: x.value, AddLeadRequestVisibleTo._member_map_.values())
        )


@JsonMap({})
class AddLeadRequest(BaseModel):
    """AddLeadRequest

    :param title: The name of the lead
    :type title: str
    :param owner_id: The ID of the user which will be the owner of the created lead. If not provided, the user making the request will be used., defaults to None
    :type owner_id: int, optional
    :param label_ids: The IDs of the lead labels which will be associated with the lead, defaults to None
    :type label_ids: List[str], optional
    :param person_id: The ID of a person which this lead will be linked to. If the person does not exist yet, it needs to be created first. This property is required unless `organization_id` is specified., defaults to None
    :type person_id: int, optional
    :param organization_id: The ID of an organization which this lead will be linked to. If the organization does not exist yet, it needs to be created first. This property is required unless `person_id` is specified., defaults to None
    :type organization_id: int, optional
    :param value: The potential value of the lead represented by a JSON object: `{ "amount": 200, "currency": "EUR" }`. Both amount and currency are required., defaults to None
    :type value: AddLeadRequestValue, optional
    :param expected_close_date: The date of when the deal which will be created from the lead is expected to be closed. In ISO 8601 format: YYYY-MM-DD., defaults to None
    :type expected_close_date: str, optional
    :param visible_to: visible_to, defaults to None
    :type visible_to: AddLeadRequestVisibleTo, optional
    :param was_seen: A flag indicating whether the lead was seen by someone in the Pipedrive UI, defaults to None
    :type was_seen: bool, optional
    :param origin_id: The optional ID to further distinguish the origin of the lead - e.g. Which API integration created this lead. If omitted, `origin_id` will be set to null., defaults to None
    :type origin_id: str, optional
    :param channel: The ID of Marketing channel this lead was created from. Provided value must be one of the channels configured for your company. You can fetch allowed values with <a href="https://developers.pipedrive.com/docs/api/v1/DealFields#getDealField" target="_blank" rel="noopener noreferrer">GET /v1/dealFields</a>. If omitted, channel will be set to null., defaults to None
    :type channel: int, optional
    :param channel_id: The optional ID to further distinguish the Marketing channel. If omitted, `channel_id` will be set to null., defaults to None
    :type channel_id: str, optional
    """

    def __init__(
        self,
        title: str,
        owner_id: int = None,
        label_ids: List[str] = None,
        person_id: int = None,
        organization_id: int = None,
        value: AddLeadRequestValue = None,
        expected_close_date: str = None,
        visible_to: AddLeadRequestVisibleTo = None,
        was_seen: bool = None,
        origin_id: str = None,
        channel: int = None,
        channel_id: str = None,
    ):
        self.title = title
        if owner_id is not None:
            self.owner_id = owner_id
        if label_ids is not None:
            self.label_ids = label_ids
        if person_id is not None:
            self.person_id = person_id
        if organization_id is not None:
            self.organization_id = organization_id
        if value is not None:
            self.value = self._define_object(value, AddLeadRequestValue)
        if expected_close_date is not None:
            self.expected_close_date = expected_close_date
        if visible_to is not None:
            self.visible_to = self._enum_matching(
                visible_to, AddLeadRequestVisibleTo.list(), "visible_to"
            )
        if was_seen is not None:
            self.was_seen = was_seen
        if origin_id is not None:
            self.origin_id = origin_id
        if channel is not None:
            self.channel = channel
        if channel_id is not None:
            self.channel_id = channel_id
