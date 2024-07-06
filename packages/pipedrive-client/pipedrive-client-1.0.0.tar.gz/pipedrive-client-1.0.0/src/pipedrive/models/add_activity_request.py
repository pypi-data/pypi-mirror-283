from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class AddActivityRequestDone(Enum):
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
            map(lambda x: x.value, AddActivityRequestDone._member_map_.values())
        )


@JsonMap({"type_": "type"})
class AddActivityRequest(BaseModel):
    """AddActivityRequest

    :param due_date: The due date of the activity. Format: YYYY-MM-DD, defaults to None
    :type due_date: str, optional
    :param due_time: The due time of the activity in UTC. Format: HH:MM, defaults to None
    :type due_time: str, optional
    :param duration: The duration of the activity. Format: HH:MM, defaults to None
    :type duration: str, optional
    :param deal_id: The ID of the deal this activity is associated with, defaults to None
    :type deal_id: int, optional
    :param lead_id: The ID of the lead in the UUID format this activity is associated with, defaults to None
    :type lead_id: str, optional
    :param person_id: The ID of the person this activity is associated with, defaults to None
    :type person_id: int, optional
    :param project_id: The ID of the project this activity is associated with, defaults to None
    :type project_id: int, optional
    :param org_id: The ID of the organization this activity is associated with, defaults to None
    :type org_id: int, optional
    :param location: The address of the activity., defaults to None
    :type location: str, optional
    :param public_description: Additional details about the activity that is synced to your external calendar. Unlike the note added to the activity, the description is publicly visible to any guests added to the activity., defaults to None
    :type public_description: str, optional
    :param note: The note of the activity (HTML format), defaults to None
    :type note: str, optional
    :param subject: The subject of the activity. When value for subject is not set, it will be given a default value `Call`., defaults to None
    :type subject: str, optional
    :param type_: The type of the activity. This is in correlation with the `key_string` parameter of ActivityTypes. When value for type is not set, it will be given a default value `Call`., defaults to None
    :type type_: str, optional
    :param user_id: The ID of the user whom the activity is assigned to. If omitted, the activity is assigned to the authorized user., defaults to None
    :type user_id: int, optional
    :param participants: List of multiple persons (participants) this activity is associated with. If omitted, single participant from `person_id` field is used. It requires a structure as follows: `[{"person_id":1,"primary_flag":true}]`, defaults to None
    :type participants: List[dict], optional
    :param busy_flag: Set the activity as 'Busy' or 'Free'. If the flag is set to `true`, your customers will not be able to book that time slot through any Scheduler links. The flag can also be unset by never setting it or overriding it with `null`. When the value of the flag is unset (`null`), the flag defaults to 'Busy' if it has a time set, and 'Free' if it is an all-day event without specified time., defaults to None
    :type busy_flag: bool, optional
    :param attendees: The attendees of the activity. This can be either your existing Pipedrive contacts or an external email address. It requires a structure as follows: `[{"email_address":"mail@example.org"}]` or `[{"person_id":1, "email_address":"mail@example.org"}]`, defaults to None
    :type attendees: List[dict], optional
    :param done: done, defaults to None
    :type done: AddActivityRequestDone, optional
    """

    def __init__(
        self,
        due_date: str = None,
        due_time: str = None,
        duration: str = None,
        deal_id: int = None,
        lead_id: str = None,
        person_id: int = None,
        project_id: int = None,
        org_id: int = None,
        location: str = None,
        public_description: str = None,
        note: str = None,
        subject: str = None,
        type_: str = None,
        user_id: int = None,
        participants: List[dict] = None,
        busy_flag: bool = None,
        attendees: List[dict] = None,
        done: AddActivityRequestDone = None,
    ):
        if due_date is not None:
            self.due_date = due_date
        if due_time is not None:
            self.due_time = due_time
        if duration is not None:
            self.duration = duration
        if deal_id is not None:
            self.deal_id = deal_id
        if lead_id is not None:
            self.lead_id = lead_id
        if person_id is not None:
            self.person_id = person_id
        if project_id is not None:
            self.project_id = project_id
        if org_id is not None:
            self.org_id = org_id
        if location is not None:
            self.location = location
        if public_description is not None:
            self.public_description = public_description
        if note is not None:
            self.note = note
        if subject is not None:
            self.subject = subject
        if type_ is not None:
            self.type_ = type_
        if user_id is not None:
            self.user_id = user_id
        if participants is not None:
            self.participants = participants
        if busy_flag is not None:
            self.busy_flag = busy_flag
        if attendees is not None:
            self.attendees = attendees
        if done is not None:
            self.done = self._enum_matching(done, AddActivityRequestDone.list(), "done")
