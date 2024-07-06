from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class UpdateNoteRequestPinnedToLeadFlag(Enum):
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
        return list(
            map(
                lambda x: x.value,
                UpdateNoteRequestPinnedToLeadFlag._member_map_.values(),
            )
        )


class UpdateNoteRequestPinnedToDealFlag(Enum):
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
        return list(
            map(
                lambda x: x.value,
                UpdateNoteRequestPinnedToDealFlag._member_map_.values(),
            )
        )


class UpdateNoteRequestPinnedToOrganizationFlag(Enum):
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
        return list(
            map(
                lambda x: x.value,
                UpdateNoteRequestPinnedToOrganizationFlag._member_map_.values(),
            )
        )


class UpdateNoteRequestPinnedToPersonFlag(Enum):
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
        return list(
            map(
                lambda x: x.value,
                UpdateNoteRequestPinnedToPersonFlag._member_map_.values(),
            )
        )


@JsonMap({})
class UpdateNoteRequest(BaseModel):
    """UpdateNoteRequest

    :param content: The content of the note in HTML format. Subject to sanitization on the back-end., defaults to None
    :type content: str, optional
    :param lead_id: The ID of the lead the note will be attached to, defaults to None
    :type lead_id: str, optional
    :param deal_id: The ID of the deal the note will be attached to, defaults to None
    :type deal_id: int, optional
    :param person_id: The ID of the person the note will be attached to, defaults to None
    :type person_id: int, optional
    :param org_id: The ID of the organization the note will be attached to, defaults to None
    :type org_id: int, optional
    :param user_id: The ID of the user who will be marked as the author of the note. Only an admin can change the author., defaults to None
    :type user_id: int, optional
    :param add_time: The optional creation date & time of the note in UTC. Can be set in the past or in the future. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    :param pinned_to_lead_flag: pinned_to_lead_flag, defaults to None
    :type pinned_to_lead_flag: UpdateNoteRequestPinnedToLeadFlag, optional
    :param pinned_to_deal_flag: pinned_to_deal_flag, defaults to None
    :type pinned_to_deal_flag: UpdateNoteRequestPinnedToDealFlag, optional
    :param pinned_to_organization_flag: pinned_to_organization_flag, defaults to None
    :type pinned_to_organization_flag: UpdateNoteRequestPinnedToOrganizationFlag, optional
    :param pinned_to_person_flag: pinned_to_person_flag, defaults to None
    :type pinned_to_person_flag: UpdateNoteRequestPinnedToPersonFlag, optional
    """

    def __init__(
        self,
        content: str = None,
        lead_id: str = None,
        deal_id: int = None,
        person_id: int = None,
        org_id: int = None,
        user_id: int = None,
        add_time: str = None,
        pinned_to_lead_flag: UpdateNoteRequestPinnedToLeadFlag = None,
        pinned_to_deal_flag: UpdateNoteRequestPinnedToDealFlag = None,
        pinned_to_organization_flag: UpdateNoteRequestPinnedToOrganizationFlag = None,
        pinned_to_person_flag: UpdateNoteRequestPinnedToPersonFlag = None,
    ):
        if content is not None:
            self.content = content
        if lead_id is not None:
            self.lead_id = lead_id
        if deal_id is not None:
            self.deal_id = deal_id
        if person_id is not None:
            self.person_id = person_id
        if org_id is not None:
            self.org_id = org_id
        if user_id is not None:
            self.user_id = user_id
        if add_time is not None:
            self.add_time = add_time
        if pinned_to_lead_flag is not None:
            self.pinned_to_lead_flag = self._enum_matching(
                pinned_to_lead_flag,
                UpdateNoteRequestPinnedToLeadFlag.list(),
                "pinned_to_lead_flag",
            )
        if pinned_to_deal_flag is not None:
            self.pinned_to_deal_flag = self._enum_matching(
                pinned_to_deal_flag,
                UpdateNoteRequestPinnedToDealFlag.list(),
                "pinned_to_deal_flag",
            )
        if pinned_to_organization_flag is not None:
            self.pinned_to_organization_flag = self._enum_matching(
                pinned_to_organization_flag,
                UpdateNoteRequestPinnedToOrganizationFlag.list(),
                "pinned_to_organization_flag",
            )
        if pinned_to_person_flag is not None:
            self.pinned_to_person_flag = self._enum_matching(
                pinned_to_person_flag,
                UpdateNoteRequestPinnedToPersonFlag.list(),
                "pinned_to_person_flag",
            )
