from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class DataOutcome3(Enum):
    """An enumeration representing different categories.

    :cvar CONNECTED: "connected"
    :vartype CONNECTED: str
    :cvar NO_ANSWER: "no_answer"
    :vartype NO_ANSWER: str
    :cvar LEFT_MESSAGE: "left_message"
    :vartype LEFT_MESSAGE: str
    :cvar LEFT_VOICEMAIL: "left_voicemail"
    :vartype LEFT_VOICEMAIL: str
    :cvar WRONG_NUMBER: "wrong_number"
    :vartype WRONG_NUMBER: str
    :cvar BUSY: "busy"
    :vartype BUSY: str
    """

    CONNECTED = "connected"
    NO_ANSWER = "no_answer"
    LEFT_MESSAGE = "left_message"
    LEFT_VOICEMAIL = "left_voicemail"
    WRONG_NUMBER = "wrong_number"
    BUSY = "busy"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, DataOutcome3._member_map_.values()))


@JsonMap({"id_": "id"})
class GetCallLogOkResponseData(BaseModel):
    """GetCallLogOkResponseData

    :param user_id: The ID of the owner of the call log. Please note that a user without account settings access cannot create call logs for other users., defaults to None
    :type user_id: int, optional
    :param activity_id: If specified, this activity will be converted into a call log, with the information provided. When this field is used, you don't need to specify `deal_id`, `person_id` or `org_id`, as they will be ignored in favor of the values already available in the activity. The `activity_id` must refer to a `call` type activity., defaults to None
    :type activity_id: int, optional
    :param subject: The name of the activity this call is attached to, defaults to None
    :type subject: str, optional
    :param duration: The duration of the call in seconds, defaults to None
    :type duration: str, optional
    :param outcome: Describes the outcome of the call
    :type outcome: DataOutcome3
    :param from_phone_number: The number that made the call, defaults to None
    :type from_phone_number: str, optional
    :param to_phone_number: The number called
    :type to_phone_number: str
    :param start_time: The date and time of the start of the call in UTC. Format: YYYY-MM-DD HH:MM:SS.
    :type start_time: str
    :param end_time: The date and time of the end of the call in UTC. Format: YYYY-MM-DD HH:MM:SS.
    :type end_time: str
    :param person_id: The ID of the person this call is associated with, defaults to None
    :type person_id: int, optional
    :param org_id: The ID of the organization this call is associated with, defaults to None
    :type org_id: int, optional
    :param deal_id: The ID of the deal this call is associated with. A call log can be associated with either a deal or a lead, but not both at once., defaults to None
    :type deal_id: int, optional
    :param lead_id: The ID of the lead in the UUID format this call is associated with. A call log can be associated with either a deal or a lead, but not both at once., defaults to None
    :type lead_id: str, optional
    :param note: The note for the call log in HTML format, defaults to None
    :type note: str, optional
    :param id_: The call log ID, generated when the call log was created, defaults to None
    :type id_: str, optional
    :param has_recording: If the call log has an audio recording attached, the value should be true, defaults to None
    :type has_recording: bool, optional
    :param company_id: The company ID of the owner of the call log, defaults to None
    :type company_id: int, optional
    """

    def __init__(
        self,
        outcome: DataOutcome3,
        to_phone_number: str,
        start_time: str,
        end_time: str,
        user_id: int = None,
        activity_id: int = None,
        subject: str = None,
        duration: str = None,
        from_phone_number: str = None,
        person_id: int = None,
        org_id: int = None,
        deal_id: int = None,
        lead_id: str = None,
        note: str = None,
        id_: str = None,
        has_recording: bool = None,
        company_id: int = None,
    ):
        if user_id is not None:
            self.user_id = user_id
        if activity_id is not None:
            self.activity_id = activity_id
        if subject is not None:
            self.subject = subject
        if duration is not None:
            self.duration = duration
        self.outcome = self._enum_matching(outcome, DataOutcome3.list(), "outcome")
        if from_phone_number is not None:
            self.from_phone_number = from_phone_number
        self.to_phone_number = to_phone_number
        self.start_time = start_time
        self.end_time = end_time
        if person_id is not None:
            self.person_id = person_id
        if org_id is not None:
            self.org_id = org_id
        if deal_id is not None:
            self.deal_id = deal_id
        if lead_id is not None:
            self.lead_id = lead_id
        if note is not None:
            self.note = note
        if id_ is not None:
            self.id_ = id_
        if has_recording is not None:
            self.has_recording = has_recording
        if company_id is not None:
            self.company_id = company_id


@JsonMap({})
class GetCallLogOkResponse(BaseModel):
    """GetCallLogOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: GetCallLogOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: GetCallLogOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetCallLogOkResponseData)
