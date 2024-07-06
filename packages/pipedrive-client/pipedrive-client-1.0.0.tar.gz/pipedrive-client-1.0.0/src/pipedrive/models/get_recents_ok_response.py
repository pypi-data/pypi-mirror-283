from enum import Enum
from typing import Union
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .base import OneOfBaseModel


class Data1Item(Enum):
    """An enumeration representing different categories.

    :cvar ACTIVITY: "activity"
    :vartype ACTIVITY: str
    """

    ACTIVITY = "activity"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Data1Item._member_map_.values()))


@JsonMap({"id_": "id", "type_": "type"})
class Data1Data(BaseModel):
    """Data1Data

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
    :param id_: The ID of the activity, generated when the activity was created, defaults to None
    :type id_: int, optional
    :param note: The note of the activity (HTML format), defaults to None
    :type note: str, optional
    :param done: Whether the activity is done or not, defaults to None
    :type done: bool, optional
    :param subject: The subject of the activity, defaults to None
    :type subject: str, optional
    :param type_: The type of the activity. This is in correlation with the `key_string` parameter of ActivityTypes., defaults to None
    :type type_: str, optional
    :param user_id: The ID of the user whom the activity is assigned to, defaults to None
    :type user_id: int, optional
    :param participants: List of multiple persons (participants) this activity is associated with, defaults to None
    :type participants: List[dict], optional
    :param busy_flag: Marks if the activity is set as 'Busy' or 'Free'. If the flag is set to `true`, your customers will not be able to book that time slot through any Scheduler links. The flag can also be unset. When the value of the flag is unset (`null`), the flag defaults to 'Busy' if it has a time set, and 'Free' if it is an all-day event without specified time., defaults to None
    :type busy_flag: bool, optional
    :param attendees: The attendees of the activity. This can be either your existing Pipedrive contacts or an external email address., defaults to None
    :type attendees: List[dict], optional
    :param company_id: The user's company ID, defaults to None
    :type company_id: int, optional
    :param reference_type: If the activity references some other object, it is indicated here. For example, value `Salesphone` refers to activities created with Caller., defaults to None
    :type reference_type: str, optional
    :param reference_id: Together with the `reference_type`, gives the ID of the other object, defaults to None
    :type reference_id: int, optional
    :param conference_meeting_client: The ID of the Marketplace app, which is connected to this activity, defaults to None
    :type conference_meeting_client: str, optional
    :param conference_meeting_url: The link to join the meeting which is associated with this activity, defaults to None
    :type conference_meeting_url: str, optional
    :param conference_meeting_id: The meeting ID of the meeting provider (Zoom, MS Teams etc.) that is associated with this activity, defaults to None
    :type conference_meeting_id: str, optional
    :param add_time: The creation date and time of the activity in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param marked_as_done_time: The date and time this activity was marked as done. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type marked_as_done_time: str, optional
    :param last_notification_time: The date and time of latest notifications sent about this activity to the participants or the attendees of this activity, defaults to None
    :type last_notification_time: str, optional
    :param last_notification_user_id: The ID of the user who triggered the sending of the latest notifications about this activity to the participants or the attendees of this activity, defaults to None
    :type last_notification_user_id: int, optional
    :param notification_language_id: The ID of the language the notifications are sent in, defaults to None
    :type notification_language_id: int, optional
    :param active_flag: Whether the activity is active or not, defaults to None
    :type active_flag: bool, optional
    :param update_time: The last update date and time of the activity. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    :param update_user_id: The ID of the user who was the last to update this activity, defaults to None
    :type update_user_id: int, optional
    :param gcal_event_id: For the activity which syncs to Google calendar, this is the Google event ID. NB! This field is related to old Google calendar sync and will be deprecated soon., defaults to None
    :type gcal_event_id: str, optional
    :param google_calendar_id: The Google calendar ID that this activity syncs to. NB! This field is related to old Google calendar sync and will be deprecated soon., defaults to None
    :type google_calendar_id: str, optional
    :param google_calendar_etag: The Google calendar API etag (version) that is used for syncing this activity. NB! This field is related to old Google calendar sync and will be deprecated soon., defaults to None
    :type google_calendar_etag: str, optional
    :param calendar_sync_include_context: For activities that sync to an external calendar, this setting indicates if the activity syncs with context (what are the deals, persons, organizations this activity is related to), defaults to None
    :type calendar_sync_include_context: str, optional
    :param source_timezone: The timezone the activity was created in an external calendar, defaults to None
    :type source_timezone: str, optional
    :param rec_rule: The rule for the recurrence of the activity. Is important for activities synced into Pipedrive from an external calendar. Example: "RRULE:FREQ=WEEKLY;BYDAY=WE", defaults to None
    :type rec_rule: str, optional
    :param rec_rule_extension: Additional rules for the recurrence of the activity, extend the `rec_rule`. Is important for activities synced into Pipedrive from an external calendar., defaults to None
    :type rec_rule_extension: str, optional
    :param rec_master_activity_id: The ID of parent activity for a recurrent activity if the current activity is an exception to recurrence rules, defaults to None
    :type rec_master_activity_id: int, optional
    :param series: The list of recurring activity instances. It is in a structure as follows: `[{due_date: "2020-06-24", due_time: "10:00:00"}]`, defaults to None
    :type series: List[dict], optional
    :param created_by_user_id: The ID of the user who created the activity, defaults to None
    :type created_by_user_id: int, optional
    :param location_subpremise: A subfield of the location field. Indicates apartment/suite number., defaults to None
    :type location_subpremise: str, optional
    :param location_street_number: A subfield of the location field. Indicates house number., defaults to None
    :type location_street_number: str, optional
    :param location_route: A subfield of the location field. Indicates street name., defaults to None
    :type location_route: str, optional
    :param location_sublocality: A subfield of the location field. Indicates district/sublocality., defaults to None
    :type location_sublocality: str, optional
    :param location_locality: A subfield of the location field. Indicates city/town/village/locality., defaults to None
    :type location_locality: str, optional
    :param location_admin_area_level_1: A subfield of the location field. Indicates state/county., defaults to None
    :type location_admin_area_level_1: str, optional
    :param location_admin_area_level_2: A subfield of the location field. Indicates region., defaults to None
    :type location_admin_area_level_2: str, optional
    :param location_country: A subfield of the location field. Indicates country., defaults to None
    :type location_country: str, optional
    :param location_postal_code: A subfield of the location field. Indicates ZIP/postal code., defaults to None
    :type location_postal_code: str, optional
    :param location_formatted_address: A subfield of the location field. Indicates full/combined address., defaults to None
    :type location_formatted_address: str, optional
    :param org_name: The name of the organization this activity is associated with, defaults to None
    :type org_name: str, optional
    :param person_name: The name of the person this activity is associated with, defaults to None
    :type person_name: str, optional
    :param deal_title: The name of the deal this activity is associated with, defaults to None
    :type deal_title: str, optional
    :param owner_name: The name of the user this activity is owned by, defaults to None
    :type owner_name: str, optional
    :param person_dropbox_bcc: The BCC email address of the person, defaults to None
    :type person_dropbox_bcc: str, optional
    :param deal_dropbox_bcc: The BCC email address of the deal, defaults to None
    :type deal_dropbox_bcc: str, optional
    :param assigned_to_user_id: The ID of the user to whom the activity is assigned to. Equal to `user_id`., defaults to None
    :type assigned_to_user_id: int, optional
    :param file: The file that is attached to this activity. For example, this can be a reference to an audio note file generated with Pipedrive mobile app., defaults to None
    :type file: dict, optional
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
        id_: int = None,
        note: str = None,
        done: bool = None,
        subject: str = None,
        type_: str = None,
        user_id: int = None,
        participants: List[dict] = None,
        busy_flag: bool = None,
        attendees: List[dict] = None,
        company_id: int = None,
        reference_type: str = None,
        reference_id: int = None,
        conference_meeting_client: str = None,
        conference_meeting_url: str = None,
        conference_meeting_id: str = None,
        add_time: str = None,
        marked_as_done_time: str = None,
        last_notification_time: str = None,
        last_notification_user_id: int = None,
        notification_language_id: int = None,
        active_flag: bool = None,
        update_time: str = None,
        update_user_id: int = None,
        gcal_event_id: str = None,
        google_calendar_id: str = None,
        google_calendar_etag: str = None,
        calendar_sync_include_context: str = None,
        source_timezone: str = None,
        rec_rule: str = None,
        rec_rule_extension: str = None,
        rec_master_activity_id: int = None,
        series: List[dict] = None,
        created_by_user_id: int = None,
        location_subpremise: str = None,
        location_street_number: str = None,
        location_route: str = None,
        location_sublocality: str = None,
        location_locality: str = None,
        location_admin_area_level_1: str = None,
        location_admin_area_level_2: str = None,
        location_country: str = None,
        location_postal_code: str = None,
        location_formatted_address: str = None,
        org_name: str = None,
        person_name: str = None,
        deal_title: str = None,
        owner_name: str = None,
        person_dropbox_bcc: str = None,
        deal_dropbox_bcc: str = None,
        assigned_to_user_id: int = None,
        file: dict = None,
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
        if id_ is not None:
            self.id_ = id_
        if note is not None:
            self.note = note
        if done is not None:
            self.done = done
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
        if company_id is not None:
            self.company_id = company_id
        if reference_type is not None:
            self.reference_type = reference_type
        if reference_id is not None:
            self.reference_id = reference_id
        if conference_meeting_client is not None:
            self.conference_meeting_client = conference_meeting_client
        if conference_meeting_url is not None:
            self.conference_meeting_url = conference_meeting_url
        if conference_meeting_id is not None:
            self.conference_meeting_id = conference_meeting_id
        if add_time is not None:
            self.add_time = add_time
        if marked_as_done_time is not None:
            self.marked_as_done_time = marked_as_done_time
        if last_notification_time is not None:
            self.last_notification_time = last_notification_time
        if last_notification_user_id is not None:
            self.last_notification_user_id = last_notification_user_id
        if notification_language_id is not None:
            self.notification_language_id = notification_language_id
        if active_flag is not None:
            self.active_flag = active_flag
        if update_time is not None:
            self.update_time = update_time
        if update_user_id is not None:
            self.update_user_id = update_user_id
        if gcal_event_id is not None:
            self.gcal_event_id = gcal_event_id
        if google_calendar_id is not None:
            self.google_calendar_id = google_calendar_id
        if google_calendar_etag is not None:
            self.google_calendar_etag = google_calendar_etag
        if calendar_sync_include_context is not None:
            self.calendar_sync_include_context = calendar_sync_include_context
        if source_timezone is not None:
            self.source_timezone = source_timezone
        if rec_rule is not None:
            self.rec_rule = rec_rule
        if rec_rule_extension is not None:
            self.rec_rule_extension = rec_rule_extension
        if rec_master_activity_id is not None:
            self.rec_master_activity_id = rec_master_activity_id
        if series is not None:
            self.series = series
        if created_by_user_id is not None:
            self.created_by_user_id = created_by_user_id
        if location_subpremise is not None:
            self.location_subpremise = location_subpremise
        if location_street_number is not None:
            self.location_street_number = location_street_number
        if location_route is not None:
            self.location_route = location_route
        if location_sublocality is not None:
            self.location_sublocality = location_sublocality
        if location_locality is not None:
            self.location_locality = location_locality
        if location_admin_area_level_1 is not None:
            self.location_admin_area_level_1 = location_admin_area_level_1
        if location_admin_area_level_2 is not None:
            self.location_admin_area_level_2 = location_admin_area_level_2
        if location_country is not None:
            self.location_country = location_country
        if location_postal_code is not None:
            self.location_postal_code = location_postal_code
        if location_formatted_address is not None:
            self.location_formatted_address = location_formatted_address
        if org_name is not None:
            self.org_name = org_name
        if person_name is not None:
            self.person_name = person_name
        if deal_title is not None:
            self.deal_title = deal_title
        if owner_name is not None:
            self.owner_name = owner_name
        if person_dropbox_bcc is not None:
            self.person_dropbox_bcc = person_dropbox_bcc
        if deal_dropbox_bcc is not None:
            self.deal_dropbox_bcc = deal_dropbox_bcc
        if assigned_to_user_id is not None:
            self.assigned_to_user_id = assigned_to_user_id
        if file is not None:
            self.file = file


@JsonMap({"id_": "id"})
class Data1(BaseModel):
    """Data1

    :param item: item, defaults to None
    :type item: Data1Item, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param data: data, defaults to None
    :type data: Data1Data, optional
    """

    def __init__(self, item: Data1Item = None, id_: int = None, data: Data1Data = None):
        if item is not None:
            self.item = self._enum_matching(item, Data1Item.list(), "item")
        if id_ is not None:
            self.id_ = id_
        if data is not None:
            self.data = self._define_object(data, Data1Data)


class Data2Item(Enum):
    """An enumeration representing different categories.

    :cvar ACTIVITYTYPE: "activityType"
    :vartype ACTIVITYTYPE: str
    """

    ACTIVITYTYPE = "activityType"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Data2Item._member_map_.values()))


class DataIconKey5(Enum):
    """An enumeration representing different categories.

    :cvar TASK: "task"
    :vartype TASK: str
    :cvar EMAIL: "email"
    :vartype EMAIL: str
    :cvar MEETING: "meeting"
    :vartype MEETING: str
    :cvar DEADLINE: "deadline"
    :vartype DEADLINE: str
    :cvar CALL: "call"
    :vartype CALL: str
    :cvar LUNCH: "lunch"
    :vartype LUNCH: str
    :cvar CALENDAR: "calendar"
    :vartype CALENDAR: str
    :cvar DOWNARROW: "downarrow"
    :vartype DOWNARROW: str
    :cvar DOCUMENT: "document"
    :vartype DOCUMENT: str
    :cvar SMARTPHONE: "smartphone"
    :vartype SMARTPHONE: str
    :cvar CAMERA: "camera"
    :vartype CAMERA: str
    :cvar SCISSORS: "scissors"
    :vartype SCISSORS: str
    :cvar COGS: "cogs"
    :vartype COGS: str
    :cvar BUBBLE: "bubble"
    :vartype BUBBLE: str
    :cvar UPARROW: "uparrow"
    :vartype UPARROW: str
    :cvar CHECKBOX: "checkbox"
    :vartype CHECKBOX: str
    :cvar SIGNPOST: "signpost"
    :vartype SIGNPOST: str
    :cvar SHUFFLE: "shuffle"
    :vartype SHUFFLE: str
    :cvar ADDRESSBOOK: "addressbook"
    :vartype ADDRESSBOOK: str
    :cvar LINEGRAPH: "linegraph"
    :vartype LINEGRAPH: str
    :cvar PICTURE: "picture"
    :vartype PICTURE: str
    :cvar CAR: "car"
    :vartype CAR: str
    :cvar WORLD: "world"
    :vartype WORLD: str
    :cvar SEARCH: "search"
    :vartype SEARCH: str
    :cvar CLIP: "clip"
    :vartype CLIP: str
    :cvar SOUND: "sound"
    :vartype SOUND: str
    :cvar BRUSH: "brush"
    :vartype BRUSH: str
    :cvar KEY: "key"
    :vartype KEY: str
    :cvar PADLOCK: "padlock"
    :vartype PADLOCK: str
    :cvar PRICETAG: "pricetag"
    :vartype PRICETAG: str
    :cvar SUITCASE: "suitcase"
    :vartype SUITCASE: str
    :cvar FINISH: "finish"
    :vartype FINISH: str
    :cvar PLANE: "plane"
    :vartype PLANE: str
    :cvar LOOP: "loop"
    :vartype LOOP: str
    :cvar WIFI: "wifi"
    :vartype WIFI: str
    :cvar TRUCK: "truck"
    :vartype TRUCK: str
    :cvar CART: "cart"
    :vartype CART: str
    :cvar BULB: "bulb"
    :vartype BULB: str
    :cvar BELL: "bell"
    :vartype BELL: str
    :cvar PRESENTATION: "presentation"
    :vartype PRESENTATION: str
    """

    TASK = "task"
    EMAIL = "email"
    MEETING = "meeting"
    DEADLINE = "deadline"
    CALL = "call"
    LUNCH = "lunch"
    CALENDAR = "calendar"
    DOWNARROW = "downarrow"
    DOCUMENT = "document"
    SMARTPHONE = "smartphone"
    CAMERA = "camera"
    SCISSORS = "scissors"
    COGS = "cogs"
    BUBBLE = "bubble"
    UPARROW = "uparrow"
    CHECKBOX = "checkbox"
    SIGNPOST = "signpost"
    SHUFFLE = "shuffle"
    ADDRESSBOOK = "addressbook"
    LINEGRAPH = "linegraph"
    PICTURE = "picture"
    CAR = "car"
    WORLD = "world"
    SEARCH = "search"
    CLIP = "clip"
    SOUND = "sound"
    BRUSH = "brush"
    KEY = "key"
    PADLOCK = "padlock"
    PRICETAG = "pricetag"
    SUITCASE = "suitcase"
    FINISH = "finish"
    PLANE = "plane"
    LOOP = "loop"
    WIFI = "wifi"
    TRUCK = "truck"
    CART = "cart"
    BULB = "bulb"
    BELL = "bell"
    PRESENTATION = "presentation"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, DataIconKey5._member_map_.values()))


@JsonMap({"id_": "id"})
class Data2Data(BaseModel):
    """Data2Data

    :param id_: The ID of the activity type, defaults to None
    :type id_: int, optional
    :param name: The name of the activity type, defaults to None
    :type name: str, optional
    :param icon_key: Icon graphic to use for representing this activity type, defaults to None
    :type icon_key: DataIconKey5, optional
    :param color: A designated color for the activity type in 6-character HEX format (e.g. `FFFFFF` for white, `000000` for black), defaults to None
    :type color: str, optional
    :param order_nr: An order number for the activity type. Order numbers should be used to order the types in the activity type selections., defaults to None
    :type order_nr: int, optional
    :param key_string: A string that is generated by the API based on the given name of the activity type upon creation, defaults to None
    :type key_string: str, optional
    :param active_flag: The active flag of the activity type, defaults to None
    :type active_flag: bool, optional
    :param is_custom_flag: Whether the activity type is a custom one or not, defaults to None
    :type is_custom_flag: bool, optional
    :param add_time: The creation time of the activity type, defaults to None
    :type add_time: str, optional
    :param update_time: The update time of the activity type, defaults to None
    :type update_time: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        icon_key: DataIconKey5 = None,
        color: str = None,
        order_nr: int = None,
        key_string: str = None,
        active_flag: bool = None,
        is_custom_flag: bool = None,
        add_time: str = None,
        update_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if icon_key is not None:
            self.icon_key = self._enum_matching(
                icon_key, DataIconKey5.list(), "icon_key"
            )
        if color is not None:
            self.color = color
        if order_nr is not None:
            self.order_nr = order_nr
        if key_string is not None:
            self.key_string = key_string
        if active_flag is not None:
            self.active_flag = active_flag
        if is_custom_flag is not None:
            self.is_custom_flag = is_custom_flag
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time


@JsonMap({"id_": "id"})
class Data2(BaseModel):
    """Data2

    :param item: item, defaults to None
    :type item: Data2Item, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param data: data, defaults to None
    :type data: Data2Data, optional
    """

    def __init__(self, item: Data2Item = None, id_: int = None, data: Data2Data = None):
        if item is not None:
            self.item = self._enum_matching(item, Data2Item.list(), "item")
        if id_ is not None:
            self.id_ = id_
        if data is not None:
            self.data = self._define_object(data, Data2Data)


class Data3Item(Enum):
    """An enumeration representing different categories.

    :cvar DEAL: "deal"
    :vartype DEAL: str
    """

    DEAL = "deal"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Data3Item._member_map_.values()))


@JsonMap({"id_": "id"})
class Data3Data(BaseModel):
    """Data3Data

    :param id_: The ID of the deal, defaults to None
    :type id_: int, optional
    :param creator_user_id: The ID of the deal creator, defaults to None
    :type creator_user_id: int, optional
    :param user_id: The ID of the user, defaults to None
    :type user_id: int, optional
    :param person_id: The ID of the person associated with the deal, defaults to None
    :type person_id: int, optional
    :param org_id: The ID of the organization associated with the deal, defaults to None
    :type org_id: int, optional
    :param stage_id: The ID of the deal stage, defaults to None
    :type stage_id: int, optional
    :param title: The title of the deal, defaults to None
    :type title: str, optional
    :param value: The value of the deal, defaults to None
    :type value: float, optional
    :param currency: The currency associated with the deal, defaults to None
    :type currency: str, optional
    :param add_time: The creation date and time of the deal, defaults to None
    :type add_time: str, optional
    :param update_time: The last updated date and time of the deal, defaults to None
    :type update_time: str, optional
    :param stage_change_time: The last updated date and time of the deal stage, defaults to None
    :type stage_change_time: str, optional
    :param active: Whether the deal is active or not, defaults to None
    :type active: bool, optional
    :param deleted: Whether the deal is deleted or not, defaults to None
    :type deleted: bool, optional
    :param status: The status of the deal, defaults to None
    :type status: str, optional
    :param probability: The success probability percentage of the deal, defaults to None
    :type probability: float, optional
    :param next_activity_date: The date of the next activity associated with the deal, defaults to None
    :type next_activity_date: str, optional
    :param next_activity_time: The time of the next activity associated with the deal, defaults to None
    :type next_activity_time: str, optional
    :param next_activity_id: The ID of the next activity associated with the deal, defaults to None
    :type next_activity_id: int, optional
    :param last_activity_id: The ID of the last activity associated with the deal, defaults to None
    :type last_activity_id: int, optional
    :param last_activity_date: The date of the last activity associated with the deal, defaults to None
    :type last_activity_date: str, optional
    :param lost_reason: The reason for losing the deal, defaults to None
    :type lost_reason: str, optional
    :param visible_to: The visibility of the deal, defaults to None
    :type visible_to: str, optional
    :param close_time: The date and time of closing the deal, defaults to None
    :type close_time: str, optional
    :param pipeline_id: The ID of the pipeline associated with the deal, defaults to None
    :type pipeline_id: int, optional
    :param won_time: The date and time of changing the deal status as won, defaults to None
    :type won_time: str, optional
    :param first_won_time: The date and time of the first time changing the deal status as won, defaults to None
    :type first_won_time: str, optional
    :param lost_time: The date and time of changing the deal status as lost, defaults to None
    :type lost_time: str, optional
    :param products_count: The number of products associated with the deal, defaults to None
    :type products_count: int, optional
    :param files_count: The number of files associated with the deal, defaults to None
    :type files_count: int, optional
    :param notes_count: The number of notes associated with the deal, defaults to None
    :type notes_count: int, optional
    :param followers_count: The number of followers associated with the deal, defaults to None
    :type followers_count: int, optional
    :param email_messages_count: The number of emails associated with the deal, defaults to None
    :type email_messages_count: int, optional
    :param activities_count: The number of activities associated with the deal, defaults to None
    :type activities_count: int, optional
    :param done_activities_count: The number of completed activities associated with the deal, defaults to None
    :type done_activities_count: int, optional
    :param undone_activities_count: The number of incomplete activities associated with the deal, defaults to None
    :type undone_activities_count: int, optional
    :param participants_count: The number of participants associated with the deal, defaults to None
    :type participants_count: int, optional
    :param expected_close_date: The expected close date of the deal, defaults to None
    :type expected_close_date: str, optional
    :param last_incoming_mail_time: The date and time of the last incoming email associated with the deal, defaults to None
    :type last_incoming_mail_time: str, optional
    :param last_outgoing_mail_time: The date and time of the last outgoing email associated with the deal, defaults to None
    :type last_outgoing_mail_time: str, optional
    :param label: The label or multiple labels assigned to the deal, defaults to None
    :type label: str, optional
    :param stage_order_nr: The order number of the deal stage associated with the deal, defaults to None
    :type stage_order_nr: int, optional
    :param person_name: The name of the person associated with the deal, defaults to None
    :type person_name: str, optional
    :param org_name: The name of the organization associated with the deal, defaults to None
    :type org_name: str, optional
    :param next_activity_subject: The subject of the next activity associated with the deal, defaults to None
    :type next_activity_subject: str, optional
    :param next_activity_type: The type of the next activity associated with the deal, defaults to None
    :type next_activity_type: str, optional
    :param next_activity_duration: The duration of the next activity associated with the deal, defaults to None
    :type next_activity_duration: str, optional
    :param next_activity_note: The note of the next activity associated with the deal, defaults to None
    :type next_activity_note: str, optional
    :param formatted_value: The deal value formatted with selected currency. E.g. US$500, defaults to None
    :type formatted_value: str, optional
    :param weighted_value: Probability times deal value. Probability can either be deal probability or if not set, then stage probability., defaults to None
    :type weighted_value: float, optional
    :param formatted_weighted_value: The weighted_value formatted with selected currency. E.g. US$500, defaults to None
    :type formatted_weighted_value: str, optional
    :param weighted_value_currency: The currency associated with the deal, defaults to None
    :type weighted_value_currency: str, optional
    :param rotten_time: The date and time of changing the deal status as rotten, defaults to None
    :type rotten_time: str, optional
    :param owner_name: The name of the deal owner, defaults to None
    :type owner_name: str, optional
    :param cc_email: The BCC email of the deal, defaults to None
    :type cc_email: str, optional
    :param org_hidden: If the organization that is associated with the deal is hidden or not, defaults to None
    :type org_hidden: bool, optional
    :param person_hidden: If the person that is associated with the deal is hidden or not, defaults to None
    :type person_hidden: bool, optional
    :param origin: The way this Deal was created. `origin` field is set by Pipedrive when Deal is created and cannot be changed., defaults to None
    :type origin: str, optional
    :param origin_id: The optional ID to further distinguish the origin of the deal - e.g. Which API integration created this Deal., defaults to None
    :type origin_id: str, optional
    :param channel: The ID of your Marketing channel this Deal was created from. Recognized Marketing channels can be configured in your <a href="https://app.pipedrive.com/settings/fields" target="_blank" rel="noopener noreferrer">Company settings</a>., defaults to None
    :type channel: int, optional
    :param channel_id: The optional ID to further distinguish the Marketing channel., defaults to None
    :type channel_id: str, optional
    :param arr: Only available in Advanced and above plans The Annual Recurring Revenue of the deal Null if there are no products attached to the deal , defaults to None
    :type arr: float, optional
    :param mrr: Only available in Advanced and above plans The Monthly Recurring Revenue of the deal Null if there are no products attached to the deal , defaults to None
    :type mrr: float, optional
    :param acv: Only available in Advanced and above plans The Annual Contract Value of the deal Null if there are no products attached to the deal , defaults to None
    :type acv: float, optional
    :param arr_currency: Only available in Advanced and above plans The Currency for Annual Recurring Revenue of the deal If the `arr` is null, this will also be null , defaults to None
    :type arr_currency: str, optional
    :param mrr_currency: Only available in Advanced and above plans The Currency for Monthly Recurring Revenue of the deal If the `mrr` is null, this will also be null , defaults to None
    :type mrr_currency: str, optional
    :param acv_currency: Only available in Advanced and above plans The Currency for Annual Contract Value of the deal If the `acv` is null, this will also be null , defaults to None
    :type acv_currency: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        creator_user_id: int = None,
        user_id: int = None,
        person_id: int = None,
        org_id: int = None,
        stage_id: int = None,
        title: str = None,
        value: float = None,
        currency: str = None,
        add_time: str = None,
        update_time: str = None,
        stage_change_time: str = None,
        active: bool = None,
        deleted: bool = None,
        status: str = None,
        probability: float = None,
        next_activity_date: str = None,
        next_activity_time: str = None,
        next_activity_id: int = None,
        last_activity_id: int = None,
        last_activity_date: str = None,
        lost_reason: str = None,
        visible_to: str = None,
        close_time: str = None,
        pipeline_id: int = None,
        won_time: str = None,
        first_won_time: str = None,
        lost_time: str = None,
        products_count: int = None,
        files_count: int = None,
        notes_count: int = None,
        followers_count: int = None,
        email_messages_count: int = None,
        activities_count: int = None,
        done_activities_count: int = None,
        undone_activities_count: int = None,
        participants_count: int = None,
        expected_close_date: str = None,
        last_incoming_mail_time: str = None,
        last_outgoing_mail_time: str = None,
        label: str = None,
        stage_order_nr: int = None,
        person_name: str = None,
        org_name: str = None,
        next_activity_subject: str = None,
        next_activity_type: str = None,
        next_activity_duration: str = None,
        next_activity_note: str = None,
        formatted_value: str = None,
        weighted_value: float = None,
        formatted_weighted_value: str = None,
        weighted_value_currency: str = None,
        rotten_time: str = None,
        owner_name: str = None,
        cc_email: str = None,
        org_hidden: bool = None,
        person_hidden: bool = None,
        origin: str = None,
        origin_id: str = None,
        channel: int = None,
        channel_id: str = None,
        arr: float = None,
        mrr: float = None,
        acv: float = None,
        arr_currency: str = None,
        mrr_currency: str = None,
        acv_currency: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if creator_user_id is not None:
            self.creator_user_id = creator_user_id
        if user_id is not None:
            self.user_id = user_id
        if person_id is not None:
            self.person_id = person_id
        if org_id is not None:
            self.org_id = org_id
        if stage_id is not None:
            self.stage_id = stage_id
        if title is not None:
            self.title = title
        if value is not None:
            self.value = value
        if currency is not None:
            self.currency = currency
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if stage_change_time is not None:
            self.stage_change_time = stage_change_time
        if active is not None:
            self.active = active
        if deleted is not None:
            self.deleted = deleted
        if status is not None:
            self.status = status
        if probability is not None:
            self.probability = probability
        if next_activity_date is not None:
            self.next_activity_date = next_activity_date
        if next_activity_time is not None:
            self.next_activity_time = next_activity_time
        if next_activity_id is not None:
            self.next_activity_id = next_activity_id
        if last_activity_id is not None:
            self.last_activity_id = last_activity_id
        if last_activity_date is not None:
            self.last_activity_date = last_activity_date
        if lost_reason is not None:
            self.lost_reason = lost_reason
        if visible_to is not None:
            self.visible_to = visible_to
        if close_time is not None:
            self.close_time = close_time
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if won_time is not None:
            self.won_time = won_time
        if first_won_time is not None:
            self.first_won_time = first_won_time
        if lost_time is not None:
            self.lost_time = lost_time
        if products_count is not None:
            self.products_count = products_count
        if files_count is not None:
            self.files_count = files_count
        if notes_count is not None:
            self.notes_count = notes_count
        if followers_count is not None:
            self.followers_count = followers_count
        if email_messages_count is not None:
            self.email_messages_count = email_messages_count
        if activities_count is not None:
            self.activities_count = activities_count
        if done_activities_count is not None:
            self.done_activities_count = done_activities_count
        if undone_activities_count is not None:
            self.undone_activities_count = undone_activities_count
        if participants_count is not None:
            self.participants_count = participants_count
        if expected_close_date is not None:
            self.expected_close_date = expected_close_date
        if last_incoming_mail_time is not None:
            self.last_incoming_mail_time = last_incoming_mail_time
        if last_outgoing_mail_time is not None:
            self.last_outgoing_mail_time = last_outgoing_mail_time
        if label is not None:
            self.label = label
        if stage_order_nr is not None:
            self.stage_order_nr = stage_order_nr
        if person_name is not None:
            self.person_name = person_name
        if org_name is not None:
            self.org_name = org_name
        if next_activity_subject is not None:
            self.next_activity_subject = next_activity_subject
        if next_activity_type is not None:
            self.next_activity_type = next_activity_type
        if next_activity_duration is not None:
            self.next_activity_duration = next_activity_duration
        if next_activity_note is not None:
            self.next_activity_note = next_activity_note
        if formatted_value is not None:
            self.formatted_value = formatted_value
        if weighted_value is not None:
            self.weighted_value = weighted_value
        if formatted_weighted_value is not None:
            self.formatted_weighted_value = formatted_weighted_value
        if weighted_value_currency is not None:
            self.weighted_value_currency = weighted_value_currency
        if rotten_time is not None:
            self.rotten_time = rotten_time
        if owner_name is not None:
            self.owner_name = owner_name
        if cc_email is not None:
            self.cc_email = cc_email
        if org_hidden is not None:
            self.org_hidden = org_hidden
        if person_hidden is not None:
            self.person_hidden = person_hidden
        if origin is not None:
            self.origin = origin
        if origin_id is not None:
            self.origin_id = origin_id
        if channel is not None:
            self.channel = channel
        if channel_id is not None:
            self.channel_id = channel_id
        if arr is not None:
            self.arr = arr
        if mrr is not None:
            self.mrr = mrr
        if acv is not None:
            self.acv = acv
        if arr_currency is not None:
            self.arr_currency = arr_currency
        if mrr_currency is not None:
            self.mrr_currency = mrr_currency
        if acv_currency is not None:
            self.acv_currency = acv_currency


@JsonMap({"id_": "id"})
class Data3(BaseModel):
    """Data3

    :param item: item, defaults to None
    :type item: Data3Item, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param data: data, defaults to None
    :type data: Data3Data, optional
    """

    def __init__(self, item: Data3Item = None, id_: int = None, data: Data3Data = None):
        if item is not None:
            self.item = self._enum_matching(item, Data3Item.list(), "item")
        if id_ is not None:
            self.id_ = id_
        if data is not None:
            self.data = self._define_object(data, Data3Data)


class Data4Item(Enum):
    """An enumeration representing different categories.

    :cvar FILE: "file"
    :vartype FILE: str
    """

    FILE = "file"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Data4Item._member_map_.values()))


@JsonMap({"id_": "id"})
class Data4Data(BaseModel):
    """The file data

    :param id_: The ID of the file, defaults to None
    :type id_: int, optional
    :param user_id: The ID of the user to associate the file with, defaults to None
    :type user_id: int, optional
    :param deal_id: The ID of the deal to associate the file with, defaults to None
    :type deal_id: int, optional
    :param person_id: The ID of the person to associate the file with, defaults to None
    :type person_id: int, optional
    :param org_id: The ID of the organization to associate the file with, defaults to None
    :type org_id: int, optional
    :param product_id: The ID of the product to associate the file with, defaults to None
    :type product_id: int, optional
    :param activity_id: The ID of the activity to associate the file with, defaults to None
    :type activity_id: int, optional
    :param lead_id: The ID of the lead to associate the file with, defaults to None
    :type lead_id: str, optional
    :param add_time: The date and time when the file was added/created. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    :param update_time: The last updated date and time of the file. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type update_time: str, optional
    :param file_name: The original name of the file, defaults to None
    :type file_name: str, optional
    :param file_size: The size of the file, defaults to None
    :type file_size: int, optional
    :param active_flag: Whether the user is active or not. false = Not activated, true = Activated, defaults to None
    :type active_flag: bool, optional
    :param inline_flag: Whether the file was uploaded as inline or not, defaults to None
    :type inline_flag: bool, optional
    :param remote_location: The location type to send the file to. Only googledrive is supported at the moment., defaults to None
    :type remote_location: str, optional
    :param remote_id: The ID of the remote item, defaults to None
    :type remote_id: str, optional
    :param cid: The ID of the inline attachment, defaults to None
    :type cid: str, optional
    :param s3_bucket: The location of the cloud storage, defaults to None
    :type s3_bucket: str, optional
    :param mail_message_id: The ID of the mail message to associate the file with, defaults to None
    :type mail_message_id: str, optional
    :param mail_template_id: The ID of the mail template to associate the file with, defaults to None
    :type mail_template_id: str, optional
    :param deal_name: The name of the deal associated with the dile, defaults to None
    :type deal_name: str, optional
    :param person_name: The name of the person associated with the file, defaults to None
    :type person_name: str, optional
    :param org_name: The name of the organization associated with the file, defaults to None
    :type org_name: str, optional
    :param product_name: The name of the product associated with the file, defaults to None
    :type product_name: str, optional
    :param lead_name: The name of the lead associated with the file, defaults to None
    :type lead_name: str, optional
    :param url: The URL of the download file, defaults to None
    :type url: str, optional
    :param name: The visible name of the file, defaults to None
    :type name: str, optional
    :param description: The description of the file, defaults to None
    :type description: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        user_id: int = None,
        deal_id: int = None,
        person_id: int = None,
        org_id: int = None,
        product_id: int = None,
        activity_id: int = None,
        lead_id: str = None,
        add_time: str = None,
        update_time: str = None,
        file_name: str = None,
        file_size: int = None,
        active_flag: bool = None,
        inline_flag: bool = None,
        remote_location: str = None,
        remote_id: str = None,
        cid: str = None,
        s3_bucket: str = None,
        mail_message_id: str = None,
        mail_template_id: str = None,
        deal_name: str = None,
        person_name: str = None,
        org_name: str = None,
        product_name: str = None,
        lead_name: str = None,
        url: str = None,
        name: str = None,
        description: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if user_id is not None:
            self.user_id = user_id
        if deal_id is not None:
            self.deal_id = deal_id
        if person_id is not None:
            self.person_id = person_id
        if org_id is not None:
            self.org_id = org_id
        if product_id is not None:
            self.product_id = product_id
        if activity_id is not None:
            self.activity_id = activity_id
        if lead_id is not None:
            self.lead_id = lead_id
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if file_name is not None:
            self.file_name = file_name
        if file_size is not None:
            self.file_size = file_size
        if active_flag is not None:
            self.active_flag = active_flag
        if inline_flag is not None:
            self.inline_flag = inline_flag
        if remote_location is not None:
            self.remote_location = remote_location
        if remote_id is not None:
            self.remote_id = remote_id
        if cid is not None:
            self.cid = cid
        if s3_bucket is not None:
            self.s3_bucket = s3_bucket
        if mail_message_id is not None:
            self.mail_message_id = mail_message_id
        if mail_template_id is not None:
            self.mail_template_id = mail_template_id
        if deal_name is not None:
            self.deal_name = deal_name
        if person_name is not None:
            self.person_name = person_name
        if org_name is not None:
            self.org_name = org_name
        if product_name is not None:
            self.product_name = product_name
        if lead_name is not None:
            self.lead_name = lead_name
        if url is not None:
            self.url = url
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description


@JsonMap({"id_": "id"})
class Data4(BaseModel):
    """Data4

    :param item: item, defaults to None
    :type item: Data4Item, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param data: The file data, defaults to None
    :type data: Data4Data, optional
    """

    def __init__(self, item: Data4Item = None, id_: int = None, data: Data4Data = None):
        if item is not None:
            self.item = self._enum_matching(item, Data4Item.list(), "item")
        if id_ is not None:
            self.id_ = id_
        if data is not None:
            self.data = self._define_object(data, Data4Data)


class Data5Item(Enum):
    """An enumeration representing different categories.

    :cvar FILTER: "filter"
    :vartype FILTER: str
    """

    FILTER = "filter"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Data5Item._member_map_.values()))


@JsonMap({"id_": "id", "type_": "type"})
class Data5Data(BaseModel):
    """The filter object

    :param id_: The ID of the filter, defaults to None
    :type id_: int, optional
    :param name: The name of the filter, defaults to None
    :type name: str, optional
    :param active_flag: The active flag of the filter, defaults to None
    :type active_flag: bool, optional
    :param type_: The type of the item, defaults to None
    :type type_: str, optional
    :param user_id: The owner of the filter, defaults to None
    :type user_id: int, optional
    :param add_time: The date and time when the filter was added, defaults to None
    :type add_time: str, optional
    :param update_time: The date and time when the filter was updated, defaults to None
    :type update_time: str, optional
    :param visible_to: The visibility group ID of who can see then filter, defaults to None
    :type visible_to: int, optional
    :param custom_view_id: Used by Pipedrive webapp, defaults to None
    :type custom_view_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        active_flag: bool = None,
        type_: str = None,
        user_id: int = None,
        add_time: str = None,
        update_time: str = None,
        visible_to: int = None,
        custom_view_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if active_flag is not None:
            self.active_flag = active_flag
        if type_ is not None:
            self.type_ = type_
        if user_id is not None:
            self.user_id = user_id
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if visible_to is not None:
            self.visible_to = visible_to
        if custom_view_id is not None:
            self.custom_view_id = custom_view_id


@JsonMap({"id_": "id"})
class Data5(BaseModel):
    """Data5

    :param item: item, defaults to None
    :type item: Data5Item, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param data: The filter object, defaults to None
    :type data: Data5Data, optional
    """

    def __init__(self, item: Data5Item = None, id_: int = None, data: Data5Data = None):
        if item is not None:
            self.item = self._enum_matching(item, Data5Item.list(), "item")
        if id_ is not None:
            self.id_ = id_
        if data is not None:
            self.data = self._define_object(data, Data5Data)


class Data6Item(Enum):
    """An enumeration representing different categories.

    :cvar NOTE: "note"
    :vartype NOTE: str
    """

    NOTE = "note"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Data6Item._member_map_.values()))


@JsonMap({})
class DataDeal5(BaseModel):
    """The deal this note is attached to

    :param title: The title of the deal this note is attached to, defaults to None
    :type title: str, optional
    """

    def __init__(self, title: str = None):
        if title is not None:
            self.title = title


@JsonMap({})
class DataOrganization5(BaseModel):
    """The organization the note is attached to

    :param name: The name of the organization the note is attached to, defaults to None
    :type name: str, optional
    """

    def __init__(self, name: str = None):
        if name is not None:
            self.name = name


@JsonMap({})
class DataPerson5(BaseModel):
    """The person the note is attached to

    :param name: The name of the person the note is attached to, defaults to None
    :type name: str, optional
    """

    def __init__(self, name: str = None):
        if name is not None:
            self.name = name


@JsonMap({})
class DataUser5(BaseModel):
    """The user who created the note

    :param email: The email of the note creator, defaults to None
    :type email: str, optional
    :param icon_url: The URL of the note creator avatar picture, defaults to None
    :type icon_url: str, optional
    :param is_you: Whether the note is created by you or not, defaults to None
    :type is_you: bool, optional
    :param name: The name of the note creator, defaults to None
    :type name: str, optional
    """

    def __init__(
        self,
        email: str = None,
        icon_url: str = None,
        is_you: bool = None,
        name: str = None,
    ):
        if email is not None:
            self.email = email
        if icon_url is not None:
            self.icon_url = icon_url
        if is_you is not None:
            self.is_you = is_you
        if name is not None:
            self.name = name


@JsonMap({"id_": "id"})
class Data6Data(BaseModel):
    """Data6Data

    :param id_: The ID of the note, defaults to None
    :type id_: int, optional
    :param active_flag: Whether the note is active or deleted, defaults to None
    :type active_flag: bool, optional
    :param add_time: The creation date and time of the note, defaults to None
    :type add_time: str, optional
    :param content: The content of the note in HTML format. Subject to sanitization on the back-end., defaults to None
    :type content: str, optional
    :param deal: The deal this note is attached to, defaults to None
    :type deal: DataDeal5, optional
    :param lead_id: The ID of the lead the note is attached to, defaults to None
    :type lead_id: str, optional
    :param deal_id: The ID of the deal the note is attached to, defaults to None
    :type deal_id: int, optional
    :param last_update_user_id: The ID of the user who last updated the note, defaults to None
    :type last_update_user_id: int, optional
    :param org_id: The ID of the organization the note is attached to, defaults to None
    :type org_id: int, optional
    :param organization: The organization the note is attached to, defaults to None
    :type organization: DataOrganization5, optional
    :param person: The person the note is attached to, defaults to None
    :type person: DataPerson5, optional
    :param person_id: The ID of the person the note is attached to, defaults to None
    :type person_id: int, optional
    :param pinned_to_deal_flag: If true, the results are filtered by note to deal pinning state, defaults to None
    :type pinned_to_deal_flag: bool, optional
    :param pinned_to_organization_flag: If true, the results are filtered by note to organization pinning state, defaults to None
    :type pinned_to_organization_flag: bool, optional
    :param pinned_to_person_flag: If true, the results are filtered by note to person pinning state, defaults to None
    :type pinned_to_person_flag: bool, optional
    :param update_time: The last updated date and time of the note, defaults to None
    :type update_time: str, optional
    :param user: The user who created the note, defaults to None
    :type user: DataUser5, optional
    :param user_id: The ID of the note creator, defaults to None
    :type user_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        active_flag: bool = None,
        add_time: str = None,
        content: str = None,
        deal: DataDeal5 = None,
        lead_id: str = None,
        deal_id: int = None,
        last_update_user_id: int = None,
        org_id: int = None,
        organization: DataOrganization5 = None,
        person: DataPerson5 = None,
        person_id: int = None,
        pinned_to_deal_flag: bool = None,
        pinned_to_organization_flag: bool = None,
        pinned_to_person_flag: bool = None,
        update_time: str = None,
        user: DataUser5 = None,
        user_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if active_flag is not None:
            self.active_flag = active_flag
        if add_time is not None:
            self.add_time = add_time
        if content is not None:
            self.content = content
        if deal is not None:
            self.deal = self._define_object(deal, DataDeal5)
        if lead_id is not None:
            self.lead_id = lead_id
        if deal_id is not None:
            self.deal_id = deal_id
        if last_update_user_id is not None:
            self.last_update_user_id = last_update_user_id
        if org_id is not None:
            self.org_id = org_id
        if organization is not None:
            self.organization = self._define_object(organization, DataOrganization5)
        if person is not None:
            self.person = self._define_object(person, DataPerson5)
        if person_id is not None:
            self.person_id = person_id
        if pinned_to_deal_flag is not None:
            self.pinned_to_deal_flag = pinned_to_deal_flag
        if pinned_to_organization_flag is not None:
            self.pinned_to_organization_flag = pinned_to_organization_flag
        if pinned_to_person_flag is not None:
            self.pinned_to_person_flag = pinned_to_person_flag
        if update_time is not None:
            self.update_time = update_time
        if user is not None:
            self.user = self._define_object(user, DataUser5)
        if user_id is not None:
            self.user_id = user_id


@JsonMap({"id_": "id"})
class Data6(BaseModel):
    """Data6

    :param item: item, defaults to None
    :type item: Data6Item, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param data: data, defaults to None
    :type data: Data6Data, optional
    """

    def __init__(self, item: Data6Item = None, id_: int = None, data: Data6Data = None):
        if item is not None:
            self.item = self._enum_matching(item, Data6Item.list(), "item")
        if id_ is not None:
            self.id_ = id_
        if data is not None:
            self.data = self._define_object(data, Data6Data)


class Data7Item(Enum):
    """An enumeration representing different categories.

    :cvar PERSON: "person"
    :vartype PERSON: str
    """

    PERSON = "person"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Data7Item._member_map_.values()))


@JsonMap({})
class DataPhone11(BaseModel):
    """DataPhone11

    :param value: The phone number, defaults to None
    :type value: str, optional
    :param primary: Boolean that indicates if phone number is primary for the person or not, defaults to None
    :type primary: bool, optional
    :param label: The label that indicates the type of the phone number. (Possible values - work, home, mobile or other), defaults to None
    :type label: str, optional
    """

    def __init__(self, value: str = None, primary: bool = None, label: str = None):
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary
        if label is not None:
            self.label = label


@JsonMap({})
class DataEmail11(BaseModel):
    """DataEmail11

    :param value: Email, defaults to None
    :type value: str, optional
    :param primary: Boolean that indicates if email is primary for the person or not, defaults to None
    :type primary: bool, optional
    :param label: The label that indicates the type of the email. (Possible values - work, home or other), defaults to None
    :type label: str, optional
    """

    def __init__(self, value: str = None, primary: bool = None, label: str = None):
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary
        if label is not None:
            self.label = label


@JsonMap({"_128": "128", "_512": "512"})
class PictureIdPictures21(BaseModel):
    """PictureIdPictures21

    :param _128: The URL of the 128*128 picture, defaults to None
    :type _128: str, optional
    :param _512: The URL of the 512*512 picture, defaults to None
    :type _512: str, optional
    """

    def __init__(self, _128: str = None, _512: str = None):
        if _128 is not None:
            self._128 = _128
        if _512 is not None:
            self._512 = _512


@JsonMap({"id_": "id"})
class DataPictureId15(BaseModel):
    """DataPictureId15

    :param id_: The ID of the picture associated with the item, defaults to None
    :type id_: int, optional
    :param item_type: The type of item the picture is related to, defaults to None
    :type item_type: str, optional
    :param item_id: The ID of related item, defaults to None
    :type item_id: int, optional
    :param active_flag: Whether the associated picture is active or not, defaults to None
    :type active_flag: bool, optional
    :param add_time: The add time of the picture, defaults to None
    :type add_time: str, optional
    :param update_time: The update time of the picture, defaults to None
    :type update_time: str, optional
    :param added_by_user_id: The ID of the user who added the picture, defaults to None
    :type added_by_user_id: int, optional
    :param pictures: pictures, defaults to None
    :type pictures: PictureIdPictures21, optional
    """

    def __init__(
        self,
        id_: int = None,
        item_type: str = None,
        item_id: int = None,
        active_flag: bool = None,
        add_time: str = None,
        update_time: str = None,
        added_by_user_id: int = None,
        pictures: PictureIdPictures21 = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if item_type is not None:
            self.item_type = item_type
        if item_id is not None:
            self.item_id = item_id
        if active_flag is not None:
            self.active_flag = active_flag
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if added_by_user_id is not None:
            self.added_by_user_id = added_by_user_id
        if pictures is not None:
            self.pictures = self._define_object(pictures, PictureIdPictures21)


@JsonMap({"id_": "id"})
class Data7Data(BaseModel):
    """Data7Data

    :param id_: The ID of the person, defaults to None
    :type id_: int, optional
    :param company_id: The ID of the company related to the person, defaults to None
    :type company_id: int, optional
    :param active_flag: Whether the person is active or not, defaults to None
    :type active_flag: bool, optional
    :param phone: A phone number supplied as a string or an array of phone objects related to the person. The structure of the array is as follows: `[{ "value": "12345", "primary": "true", "label": "mobile" }]`. Please note that only `value` is required., defaults to None
    :type phone: List[DataPhone11], optional
    :param email: An email address as a string or an array of email objects related to the person. The structure of the array is as follows: `[{ "value": "mail@example.com", "primary": "true", "label": "main" } ]`. Please note that only `value` is required., defaults to None
    :type email: List[DataEmail11], optional
    :param first_char: The first letter of the name of the person, defaults to None
    :type first_char: str, optional
    :param add_time: The date and time when the person was added/created. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    :param update_time: The last updated date and time of the person. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type update_time: str, optional
    :param visible_to: The visibility group ID of who can see the person, defaults to None
    :type visible_to: str, optional
    :param picture_id: picture_id, defaults to None
    :type picture_id: DataPictureId15, optional
    :param label: The label assigned to the person, defaults to None
    :type label: int, optional
    :param org_name: The name of the organization associated with the person, defaults to None
    :type org_name: str, optional
    :param owner_name: The name of the owner associated with the person, defaults to None
    :type owner_name: str, optional
    :param cc_email: The BCC email associated with the person, defaults to None
    :type cc_email: str, optional
    :param owner_id: The ID of the owner related to the person, defaults to None
    :type owner_id: int, optional
    :param org_id: The ID of the organization related to the person, defaults to None
    :type org_id: int, optional
    :param merge_what_id: The ID of the person with what the main person was merged, defaults to None
    :type merge_what_id: int, optional
    :param name: The name of the person, defaults to None
    :type name: str, optional
    :param first_name: The first name of the person, defaults to None
    :type first_name: str, optional
    :param last_name: The last name of the person, defaults to None
    :type last_name: str, optional
    :param email_messages_count: The count of email messages related to the person, defaults to None
    :type email_messages_count: int, optional
    :param activities_count: The count of activities related to the person, defaults to None
    :type activities_count: int, optional
    :param done_activities_count: The count of done activities related to the person, defaults to None
    :type done_activities_count: int, optional
    :param undone_activities_count: The count of undone activities related to the person, defaults to None
    :type undone_activities_count: int, optional
    :param files_count: The count of files related to the person, defaults to None
    :type files_count: int, optional
    :param notes_count: The count of notes related to the person, defaults to None
    :type notes_count: int, optional
    :param followers_count: The count of followers related to the person, defaults to None
    :type followers_count: int, optional
    :param last_incoming_mail_time: The date and time of the last incoming email associated with the person, defaults to None
    :type last_incoming_mail_time: str, optional
    :param last_outgoing_mail_time: The date and time of the last outgoing email associated with the person, defaults to None
    :type last_outgoing_mail_time: str, optional
    :param open_deals_count: The count of open deals related with the item, defaults to None
    :type open_deals_count: int, optional
    :param related_open_deals_count: The count of related open deals related with the item, defaults to None
    :type related_open_deals_count: int, optional
    :param closed_deals_count: The count of closed deals related with the item, defaults to None
    :type closed_deals_count: int, optional
    :param related_closed_deals_count: The count of related closed deals related with the item, defaults to None
    :type related_closed_deals_count: int, optional
    :param won_deals_count: The count of won deals related with the item, defaults to None
    :type won_deals_count: int, optional
    :param related_won_deals_count: The count of related won deals related with the item, defaults to None
    :type related_won_deals_count: int, optional
    :param lost_deals_count: The count of lost deals related with the item, defaults to None
    :type lost_deals_count: int, optional
    :param related_lost_deals_count: The count of related lost deals related with the item, defaults to None
    :type related_lost_deals_count: int, optional
    :param next_activity_date: The date of the next activity associated with the deal, defaults to None
    :type next_activity_date: str, optional
    :param next_activity_time: The time of the next activity associated with the deal, defaults to None
    :type next_activity_time: str, optional
    :param next_activity_id: The ID of the next activity associated with the deal, defaults to None
    :type next_activity_id: int, optional
    :param last_activity_id: The ID of the last activity associated with the deal, defaults to None
    :type last_activity_id: int, optional
    :param last_activity_date: The date of the last activity associated with the deal, defaults to None
    :type last_activity_date: str, optional
    :param participant_open_deals_count: The count of open participant deals related with the item, defaults to None
    :type participant_open_deals_count: int, optional
    :param participant_closed_deals_count: The count of closed participant deals related with the item, defaults to None
    :type participant_closed_deals_count: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        company_id: int = None,
        active_flag: bool = None,
        phone: List[DataPhone11] = None,
        email: List[DataEmail11] = None,
        first_char: str = None,
        add_time: str = None,
        update_time: str = None,
        visible_to: str = None,
        picture_id: DataPictureId15 = None,
        label: int = None,
        org_name: str = None,
        owner_name: str = None,
        cc_email: str = None,
        owner_id: int = None,
        org_id: int = None,
        merge_what_id: int = None,
        name: str = None,
        first_name: str = None,
        last_name: str = None,
        email_messages_count: int = None,
        activities_count: int = None,
        done_activities_count: int = None,
        undone_activities_count: int = None,
        files_count: int = None,
        notes_count: int = None,
        followers_count: int = None,
        last_incoming_mail_time: str = None,
        last_outgoing_mail_time: str = None,
        open_deals_count: int = None,
        related_open_deals_count: int = None,
        closed_deals_count: int = None,
        related_closed_deals_count: int = None,
        won_deals_count: int = None,
        related_won_deals_count: int = None,
        lost_deals_count: int = None,
        related_lost_deals_count: int = None,
        next_activity_date: str = None,
        next_activity_time: str = None,
        next_activity_id: int = None,
        last_activity_id: int = None,
        last_activity_date: str = None,
        participant_open_deals_count: int = None,
        participant_closed_deals_count: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if company_id is not None:
            self.company_id = company_id
        if active_flag is not None:
            self.active_flag = active_flag
        if phone is not None:
            self.phone = self._define_list(phone, DataPhone11)
        if email is not None:
            self.email = self._define_list(email, DataEmail11)
        if first_char is not None:
            self.first_char = first_char
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if visible_to is not None:
            self.visible_to = visible_to
        if picture_id is not None:
            self.picture_id = self._define_object(picture_id, DataPictureId15)
        if label is not None:
            self.label = label
        if org_name is not None:
            self.org_name = org_name
        if owner_name is not None:
            self.owner_name = owner_name
        if cc_email is not None:
            self.cc_email = cc_email
        if owner_id is not None:
            self.owner_id = owner_id
        if org_id is not None:
            self.org_id = org_id
        if merge_what_id is not None:
            self.merge_what_id = merge_what_id
        if name is not None:
            self.name = name
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if email_messages_count is not None:
            self.email_messages_count = email_messages_count
        if activities_count is not None:
            self.activities_count = activities_count
        if done_activities_count is not None:
            self.done_activities_count = done_activities_count
        if undone_activities_count is not None:
            self.undone_activities_count = undone_activities_count
        if files_count is not None:
            self.files_count = files_count
        if notes_count is not None:
            self.notes_count = notes_count
        if followers_count is not None:
            self.followers_count = followers_count
        if last_incoming_mail_time is not None:
            self.last_incoming_mail_time = last_incoming_mail_time
        if last_outgoing_mail_time is not None:
            self.last_outgoing_mail_time = last_outgoing_mail_time
        if open_deals_count is not None:
            self.open_deals_count = open_deals_count
        if related_open_deals_count is not None:
            self.related_open_deals_count = related_open_deals_count
        if closed_deals_count is not None:
            self.closed_deals_count = closed_deals_count
        if related_closed_deals_count is not None:
            self.related_closed_deals_count = related_closed_deals_count
        if won_deals_count is not None:
            self.won_deals_count = won_deals_count
        if related_won_deals_count is not None:
            self.related_won_deals_count = related_won_deals_count
        if lost_deals_count is not None:
            self.lost_deals_count = lost_deals_count
        if related_lost_deals_count is not None:
            self.related_lost_deals_count = related_lost_deals_count
        if next_activity_date is not None:
            self.next_activity_date = next_activity_date
        if next_activity_time is not None:
            self.next_activity_time = next_activity_time
        if next_activity_id is not None:
            self.next_activity_id = next_activity_id
        if last_activity_id is not None:
            self.last_activity_id = last_activity_id
        if last_activity_date is not None:
            self.last_activity_date = last_activity_date
        if participant_open_deals_count is not None:
            self.participant_open_deals_count = participant_open_deals_count
        if participant_closed_deals_count is not None:
            self.participant_closed_deals_count = participant_closed_deals_count


@JsonMap({"id_": "id"})
class Data7(BaseModel):
    """Data7

    :param item: item, defaults to None
    :type item: Data7Item, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param data: data, defaults to None
    :type data: Data7Data, optional
    """

    def __init__(self, item: Data7Item = None, id_: int = None, data: Data7Data = None):
        if item is not None:
            self.item = self._enum_matching(item, Data7Item.list(), "item")
        if id_ is not None:
            self.id_ = id_
        if data is not None:
            self.data = self._define_object(data, Data7Data)


class Data8Item(Enum):
    """An enumeration representing different categories.

    :cvar ORGANIZATION: "organization"
    :vartype ORGANIZATION: str
    """

    ORGANIZATION = "organization"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Data8Item._member_map_.values()))


@JsonMap({"id_": "id"})
class DataOwnerId13(BaseModel):
    """DataOwnerId13

    :param id_: The ID of the user, defaults to None
    :type id_: int, optional
    :param name: The name of the user, defaults to None
    :type name: str, optional
    :param email: The email of the user, defaults to None
    :type email: str, optional
    :param has_pic: Whether the user has picture or not. 0 = No picture, 1 = Has picture., defaults to None
    :type has_pic: int, optional
    :param pic_hash: The user picture hash, defaults to None
    :type pic_hash: str, optional
    :param active_flag: Whether the user is active or not, defaults to None
    :type active_flag: bool, optional
    :param value: The ID of the owner, defaults to None
    :type value: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        email: str = None,
        has_pic: int = None,
        pic_hash: str = None,
        active_flag: bool = None,
        value: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if has_pic is not None:
            self.has_pic = has_pic
        if pic_hash is not None:
            self.pic_hash = pic_hash
        if active_flag is not None:
            self.active_flag = active_flag
        if value is not None:
            self.value = value


@JsonMap({"_128": "128", "_512": "512"})
class PictureIdPictures22(BaseModel):
    """PictureIdPictures22

    :param _128: The URL of the 128*128 picture, defaults to None
    :type _128: str, optional
    :param _512: The URL of the 512*512 picture, defaults to None
    :type _512: str, optional
    """

    def __init__(self, _128: str = None, _512: str = None):
        if _128 is not None:
            self._128 = _128
        if _512 is not None:
            self._512 = _512


@JsonMap({})
class DataPictureId16(BaseModel):
    """DataPictureId16

    :param value: The ID of the picture associated with the item, defaults to None
    :type value: int, optional
    :param item_type: The type of item the picture is related to, defaults to None
    :type item_type: str, optional
    :param item_id: The ID of related item, defaults to None
    :type item_id: int, optional
    :param active_flag: Whether the associated picture is active or not, defaults to None
    :type active_flag: bool, optional
    :param add_time: The add time of the picture, defaults to None
    :type add_time: str, optional
    :param update_time: The update time of the picture, defaults to None
    :type update_time: str, optional
    :param added_by_user_id: The ID of the user who added the picture, defaults to None
    :type added_by_user_id: int, optional
    :param pictures: pictures, defaults to None
    :type pictures: PictureIdPictures22, optional
    """

    def __init__(
        self,
        value: int = None,
        item_type: str = None,
        item_id: int = None,
        active_flag: bool = None,
        add_time: str = None,
        update_time: str = None,
        added_by_user_id: int = None,
        pictures: PictureIdPictures22 = None,
    ):
        if value is not None:
            self.value = value
        if item_type is not None:
            self.item_type = item_type
        if item_id is not None:
            self.item_id = item_id
        if active_flag is not None:
            self.active_flag = active_flag
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if added_by_user_id is not None:
            self.added_by_user_id = added_by_user_id
        if pictures is not None:
            self.pictures = self._define_object(pictures, PictureIdPictures22)


@JsonMap({"id_": "id"})
class Data8Data(BaseModel):
    """Data8Data

    :param id_: The ID of the organization, defaults to None
    :type id_: int, optional
    :param company_id: The ID of the company related to the organization, defaults to None
    :type company_id: int, optional
    :param owner_id: owner_id, defaults to None
    :type owner_id: DataOwnerId13, optional
    :param name: The name of the organization, defaults to None
    :type name: str, optional
    :param active_flag: Whether the organization is active or not, defaults to None
    :type active_flag: bool, optional
    :param picture_id: picture_id, defaults to None
    :type picture_id: DataPictureId16, optional
    :param country_code: The country code of the organization, defaults to None
    :type country_code: str, optional
    :param first_char: The first character of the organization name, defaults to None
    :type first_char: str, optional
    :param add_time: The creation date and time of the organization, defaults to None
    :type add_time: str, optional
    :param update_time: The last updated date and time of the organization, defaults to None
    :type update_time: str, optional
    :param visible_to: The visibility group ID of who can see the organization, defaults to None
    :type visible_to: str, optional
    :param label: The label assigned to the organization, defaults to None
    :type label: int, optional
    :param owner_name: The name of the organization owner, defaults to None
    :type owner_name: str, optional
    :param cc_email: The BCC email associated with the organization, defaults to None
    :type cc_email: str, optional
    :param email_messages_count: The count of email messages related to the organization, defaults to None
    :type email_messages_count: int, optional
    :param people_count: The count of persons related to the organization, defaults to None
    :type people_count: int, optional
    :param activities_count: The count of activities related to the organization, defaults to None
    :type activities_count: int, optional
    :param done_activities_count: The count of done activities related to the organization, defaults to None
    :type done_activities_count: int, optional
    :param undone_activities_count: The count of undone activities related to the organization, defaults to None
    :type undone_activities_count: int, optional
    :param files_count: The count of files related to the organization, defaults to None
    :type files_count: int, optional
    :param notes_count: The count of notes related to the organization, defaults to None
    :type notes_count: int, optional
    :param followers_count: The count of followers related to the organization, defaults to None
    :type followers_count: int, optional
    :param address: The full address of the organization, defaults to None
    :type address: str, optional
    :param address_subpremise: The sub-premise of the organization location, defaults to None
    :type address_subpremise: str, optional
    :param address_street_number: The street number of the organization location, defaults to None
    :type address_street_number: str, optional
    :param address_route: The route of the organization location, defaults to None
    :type address_route: str, optional
    :param address_sublocality: The sub-locality of the organization location, defaults to None
    :type address_sublocality: str, optional
    :param address_locality: The locality of the organization location, defaults to None
    :type address_locality: str, optional
    :param address_admin_area_level_1: The level 1 admin area of the organization location, defaults to None
    :type address_admin_area_level_1: str, optional
    :param address_admin_area_level_2: The level 2 admin area of the organization location, defaults to None
    :type address_admin_area_level_2: str, optional
    :param address_country: The country of the organization location, defaults to None
    :type address_country: str, optional
    :param address_postal_code: The postal code of the organization location, defaults to None
    :type address_postal_code: str, optional
    :param address_formatted_address: The formatted organization location, defaults to None
    :type address_formatted_address: str, optional
    :param open_deals_count: The count of open deals related with the item, defaults to None
    :type open_deals_count: int, optional
    :param related_open_deals_count: The count of related open deals related with the item, defaults to None
    :type related_open_deals_count: int, optional
    :param closed_deals_count: The count of closed deals related with the item, defaults to None
    :type closed_deals_count: int, optional
    :param related_closed_deals_count: The count of related closed deals related with the item, defaults to None
    :type related_closed_deals_count: int, optional
    :param won_deals_count: The count of won deals related with the item, defaults to None
    :type won_deals_count: int, optional
    :param related_won_deals_count: The count of related won deals related with the item, defaults to None
    :type related_won_deals_count: int, optional
    :param lost_deals_count: The count of lost deals related with the item, defaults to None
    :type lost_deals_count: int, optional
    :param related_lost_deals_count: The count of related lost deals related with the item, defaults to None
    :type related_lost_deals_count: int, optional
    :param next_activity_date: The date of the next activity associated with the deal, defaults to None
    :type next_activity_date: str, optional
    :param next_activity_time: The time of the next activity associated with the deal, defaults to None
    :type next_activity_time: str, optional
    :param next_activity_id: The ID of the next activity associated with the deal, defaults to None
    :type next_activity_id: int, optional
    :param last_activity_id: The ID of the last activity associated with the deal, defaults to None
    :type last_activity_id: int, optional
    :param last_activity_date: The date of the last activity associated with the deal, defaults to None
    :type last_activity_date: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        company_id: int = None,
        owner_id: DataOwnerId13 = None,
        name: str = None,
        active_flag: bool = None,
        picture_id: DataPictureId16 = None,
        country_code: str = None,
        first_char: str = None,
        add_time: str = None,
        update_time: str = None,
        visible_to: str = None,
        label: int = None,
        owner_name: str = None,
        cc_email: str = None,
        email_messages_count: int = None,
        people_count: int = None,
        activities_count: int = None,
        done_activities_count: int = None,
        undone_activities_count: int = None,
        files_count: int = None,
        notes_count: int = None,
        followers_count: int = None,
        address: str = None,
        address_subpremise: str = None,
        address_street_number: str = None,
        address_route: str = None,
        address_sublocality: str = None,
        address_locality: str = None,
        address_admin_area_level_1: str = None,
        address_admin_area_level_2: str = None,
        address_country: str = None,
        address_postal_code: str = None,
        address_formatted_address: str = None,
        open_deals_count: int = None,
        related_open_deals_count: int = None,
        closed_deals_count: int = None,
        related_closed_deals_count: int = None,
        won_deals_count: int = None,
        related_won_deals_count: int = None,
        lost_deals_count: int = None,
        related_lost_deals_count: int = None,
        next_activity_date: str = None,
        next_activity_time: str = None,
        next_activity_id: int = None,
        last_activity_id: int = None,
        last_activity_date: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if company_id is not None:
            self.company_id = company_id
        if owner_id is not None:
            self.owner_id = self._define_object(owner_id, DataOwnerId13)
        if name is not None:
            self.name = name
        if active_flag is not None:
            self.active_flag = active_flag
        if picture_id is not None:
            self.picture_id = self._define_object(picture_id, DataPictureId16)
        if country_code is not None:
            self.country_code = country_code
        if first_char is not None:
            self.first_char = first_char
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if visible_to is not None:
            self.visible_to = visible_to
        if label is not None:
            self.label = label
        if owner_name is not None:
            self.owner_name = owner_name
        if cc_email is not None:
            self.cc_email = cc_email
        if email_messages_count is not None:
            self.email_messages_count = email_messages_count
        if people_count is not None:
            self.people_count = people_count
        if activities_count is not None:
            self.activities_count = activities_count
        if done_activities_count is not None:
            self.done_activities_count = done_activities_count
        if undone_activities_count is not None:
            self.undone_activities_count = undone_activities_count
        if files_count is not None:
            self.files_count = files_count
        if notes_count is not None:
            self.notes_count = notes_count
        if followers_count is not None:
            self.followers_count = followers_count
        if address is not None:
            self.address = address
        if address_subpremise is not None:
            self.address_subpremise = address_subpremise
        if address_street_number is not None:
            self.address_street_number = address_street_number
        if address_route is not None:
            self.address_route = address_route
        if address_sublocality is not None:
            self.address_sublocality = address_sublocality
        if address_locality is not None:
            self.address_locality = address_locality
        if address_admin_area_level_1 is not None:
            self.address_admin_area_level_1 = address_admin_area_level_1
        if address_admin_area_level_2 is not None:
            self.address_admin_area_level_2 = address_admin_area_level_2
        if address_country is not None:
            self.address_country = address_country
        if address_postal_code is not None:
            self.address_postal_code = address_postal_code
        if address_formatted_address is not None:
            self.address_formatted_address = address_formatted_address
        if open_deals_count is not None:
            self.open_deals_count = open_deals_count
        if related_open_deals_count is not None:
            self.related_open_deals_count = related_open_deals_count
        if closed_deals_count is not None:
            self.closed_deals_count = closed_deals_count
        if related_closed_deals_count is not None:
            self.related_closed_deals_count = related_closed_deals_count
        if won_deals_count is not None:
            self.won_deals_count = won_deals_count
        if related_won_deals_count is not None:
            self.related_won_deals_count = related_won_deals_count
        if lost_deals_count is not None:
            self.lost_deals_count = lost_deals_count
        if related_lost_deals_count is not None:
            self.related_lost_deals_count = related_lost_deals_count
        if next_activity_date is not None:
            self.next_activity_date = next_activity_date
        if next_activity_time is not None:
            self.next_activity_time = next_activity_time
        if next_activity_id is not None:
            self.next_activity_id = next_activity_id
        if last_activity_id is not None:
            self.last_activity_id = last_activity_id
        if last_activity_date is not None:
            self.last_activity_date = last_activity_date


@JsonMap({"id_": "id"})
class Data8(BaseModel):
    """Data8

    :param item: item, defaults to None
    :type item: Data8Item, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param data: data, defaults to None
    :type data: Data8Data, optional
    """

    def __init__(self, item: Data8Item = None, id_: int = None, data: Data8Data = None):
        if item is not None:
            self.item = self._enum_matching(item, Data8Item.list(), "item")
        if id_ is not None:
            self.id_ = id_
        if data is not None:
            self.data = self._define_object(data, Data8Data)


class Data9Item(Enum):
    """An enumeration representing different categories.

    :cvar PIPELINE: "pipeline"
    :vartype PIPELINE: str
    """

    PIPELINE = "pipeline"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Data9Item._member_map_.values()))


@JsonMap({"id_": "id"})
class Data9Data(BaseModel):
    """Data9Data

    :param id_: The ID of the pipeline, defaults to None
    :type id_: int, optional
    :param name: The name of the pipeline, defaults to None
    :type name: str, optional
    :param url_title: The pipeline title displayed in the URL, defaults to None
    :type url_title: str, optional
    :param order_nr: Defines the order of pipelines. First order (`order_nr=0`) is the default pipeline., defaults to None
    :type order_nr: int, optional
    :param active: Whether this pipeline will be made inactive (hidden) or active, defaults to None
    :type active: bool, optional
    :param deal_probability: Whether deal probability is disabled or enabled for this pipeline, defaults to None
    :type deal_probability: bool, optional
    :param add_time: The pipeline creation time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param update_time: The pipeline update time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        url_title: str = None,
        order_nr: int = None,
        active: bool = None,
        deal_probability: bool = None,
        add_time: str = None,
        update_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if url_title is not None:
            self.url_title = url_title
        if order_nr is not None:
            self.order_nr = order_nr
        if active is not None:
            self.active = active
        if deal_probability is not None:
            self.deal_probability = deal_probability
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time


@JsonMap({"id_": "id"})
class Data9(BaseModel):
    """Data9

    :param item: item, defaults to None
    :type item: Data9Item, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param data: data, defaults to None
    :type data: Data9Data, optional
    """

    def __init__(self, item: Data9Item = None, id_: int = None, data: Data9Data = None):
        if item is not None:
            self.item = self._enum_matching(item, Data9Item.list(), "item")
        if id_ is not None:
            self.id_ = id_
        if data is not None:
            self.data = self._define_object(data, Data9Data)


class Data10Item(Enum):
    """An enumeration representing different categories.

    :cvar PRODUCT: "product"
    :vartype PRODUCT: str
    """

    PRODUCT = "product"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Data10Item._member_map_.values()))


@JsonMap({"id_": "id"})
class Data10Data(BaseModel):
    """Data10Data

    :param id_: The ID of the product, defaults to None
    :type id_: int, optional
    :param name: The name of the product, defaults to None
    :type name: str, optional
    :param code: The product code, defaults to None
    :type code: str, optional
    :param description: The description of the product, defaults to None
    :type description: str, optional
    :param unit: The unit in which this product is sold, defaults to None
    :type unit: str, optional
    :param tax: The tax percentage, defaults to None
    :type tax: float, optional
    :param category: The category of the product, defaults to None
    :type category: str, optional
    :param active_flag: Whether this product will be made active or not, defaults to None
    :type active_flag: bool, optional
    :param selectable: Whether this product can be selected in deals or not, defaults to None
    :type selectable: bool, optional
    :param first_char: The first letter of the product name, defaults to None
    :type first_char: str, optional
    :param visible_to: The visibility of the product. If omitted, the visibility will be set to the default visibility setting of this item type for the authorized user., defaults to None
    :type visible_to: int, optional
    :param owner_id: The ID of the user who will be marked as the owner of this product. When omitted, authorized user ID will be used., defaults to None
    :type owner_id: int, optional
    :param files_count: The count of files, defaults to None
    :type files_count: int, optional
    :param add_time: The date and time when the product was added to the deal, defaults to None
    :type add_time: str, optional
    :param update_time: The date and time when the product was updated to the deal, defaults to None
    :type update_time: str, optional
    :param prices: Array of objects, each containing: `currency` (string), `price` (number), `cost` (number, optional), `overhead_cost` (number, optional). Note that there can only be one price per product per currency. When `prices` is omitted altogether, a default price of 0 and a default currency based on the company's currency will be assigned., defaults to None
    :type prices: List[dict], optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        code: str = None,
        description: str = None,
        unit: str = None,
        tax: float = None,
        category: str = None,
        active_flag: bool = None,
        selectable: bool = None,
        first_char: str = None,
        visible_to: int = None,
        owner_id: int = None,
        files_count: int = None,
        add_time: str = None,
        update_time: str = None,
        prices: List[dict] = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if code is not None:
            self.code = code
        if description is not None:
            self.description = description
        if unit is not None:
            self.unit = unit
        if tax is not None:
            self.tax = tax
        if category is not None:
            self.category = category
        if active_flag is not None:
            self.active_flag = active_flag
        if selectable is not None:
            self.selectable = selectable
        if first_char is not None:
            self.first_char = first_char
        if visible_to is not None:
            self.visible_to = visible_to
        if owner_id is not None:
            self.owner_id = owner_id
        if files_count is not None:
            self.files_count = files_count
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if prices is not None:
            self.prices = prices


@JsonMap({"id_": "id"})
class Data10(BaseModel):
    """Data10

    :param item: item, defaults to None
    :type item: Data10Item, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param data: data, defaults to None
    :type data: Data10Data, optional
    """

    def __init__(
        self, item: Data10Item = None, id_: int = None, data: Data10Data = None
    ):
        if item is not None:
            self.item = self._enum_matching(item, Data10Item.list(), "item")
        if id_ is not None:
            self.id_ = id_
        if data is not None:
            self.data = self._define_object(data, Data10Data)


class Data11Item(Enum):
    """An enumeration representing different categories.

    :cvar STAGE: "stage"
    :vartype STAGE: str
    """

    STAGE = "stage"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Data11Item._member_map_.values()))


@JsonMap({"id_": "id"})
class Data11Data(BaseModel):
    """Data11Data

    :param id_: The ID of the stage, defaults to None
    :type id_: int, optional
    :param order_nr: Defines the order of the stage, defaults to None
    :type order_nr: int, optional
    :param name: The name of the stage, defaults to None
    :type name: str, optional
    :param active_flag: Whether the stage is active or deleted, defaults to None
    :type active_flag: bool, optional
    :param deal_probability: The success probability percentage of the deal. Used/shown when the deal weighted values are used., defaults to None
    :type deal_probability: int, optional
    :param pipeline_id: The ID of the pipeline to add the stage to, defaults to None
    :type pipeline_id: int, optional
    :param rotten_flag: Whether deals in this stage can become rotten, defaults to None
    :type rotten_flag: bool, optional
    :param rotten_days: The number of days the deals not updated in this stage would become rotten. Applies only if the `rotten_flag` is set., defaults to None
    :type rotten_days: int, optional
    :param add_time: The stage creation time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param update_time: The stage update time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        order_nr: int = None,
        name: str = None,
        active_flag: bool = None,
        deal_probability: int = None,
        pipeline_id: int = None,
        rotten_flag: bool = None,
        rotten_days: int = None,
        add_time: str = None,
        update_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if order_nr is not None:
            self.order_nr = order_nr
        if name is not None:
            self.name = name
        if active_flag is not None:
            self.active_flag = active_flag
        if deal_probability is not None:
            self.deal_probability = deal_probability
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if rotten_flag is not None:
            self.rotten_flag = rotten_flag
        if rotten_days is not None:
            self.rotten_days = rotten_days
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time


@JsonMap({"id_": "id"})
class Data11(BaseModel):
    """Data11

    :param item: item, defaults to None
    :type item: Data11Item, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param data: data, defaults to None
    :type data: Data11Data, optional
    """

    def __init__(
        self, item: Data11Item = None, id_: int = None, data: Data11Data = None
    ):
        if item is not None:
            self.item = self._enum_matching(item, Data11Item.list(), "item")
        if id_ is not None:
            self.id_ = id_
        if data is not None:
            self.data = self._define_object(data, Data11Data)


class Data12Item(Enum):
    """An enumeration representing different categories.

    :cvar USER: "user"
    :vartype USER: str
    """

    USER = "user"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Data12Item._member_map_.values()))


class AccessApp1(Enum):
    """An enumeration representing different categories.

    :cvar SALES: "sales"
    :vartype SALES: str
    :cvar PROJECTS: "projects"
    :vartype PROJECTS: str
    :cvar CAMPAIGNS: "campaigns"
    :vartype CAMPAIGNS: str
    :cvar GLOBAL: "global"
    :vartype GLOBAL: str
    :cvar ACCOUNT_SETTINGS: "account_settings"
    :vartype ACCOUNT_SETTINGS: str
    """

    SALES = "sales"
    PROJECTS = "projects"
    CAMPAIGNS = "campaigns"
    GLOBAL = "global"
    ACCOUNT_SETTINGS = "account_settings"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, AccessApp1._member_map_.values()))


@JsonMap({})
class DataAccess1(BaseModel):
    """DataAccess1

    :param app: app, defaults to None
    :type app: AccessApp1, optional
    :param admin: admin, defaults to None
    :type admin: bool, optional
    :param permission_set_id: permission_set_id, defaults to None
    :type permission_set_id: str, optional
    """

    def __init__(
        self, app: AccessApp1 = None, admin: bool = None, permission_set_id: str = None
    ):
        if app is not None:
            self.app = self._enum_matching(app, AccessApp1.list(), "app")
        if admin is not None:
            self.admin = admin
        if permission_set_id is not None:
            self.permission_set_id = permission_set_id


@JsonMap({"id_": "id"})
class Data12Data(BaseModel):
    """Data12Data

    :param id_: The user ID, defaults to None
    :type id_: int, optional
    :param name: The user name, defaults to None
    :type name: str, optional
    :param default_currency: The user default currency, defaults to None
    :type default_currency: str, optional
    :param locale: The user locale, defaults to None
    :type locale: str, optional
    :param lang: The user language ID, defaults to None
    :type lang: int, optional
    :param email: The user email, defaults to None
    :type email: str, optional
    :param phone: The user phone, defaults to None
    :type phone: str, optional
    :param activated: Boolean that indicates whether the user is activated, defaults to None
    :type activated: bool, optional
    :param last_login: The last login date and time of the user. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type last_login: str, optional
    :param created: The creation date and time of the user. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type created: str, optional
    :param modified: The last modification date and time of the user. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type modified: str, optional
    :param has_created_company: Boolean that indicates whether the user has created a company, defaults to None
    :type has_created_company: bool, optional
    :param access: access, defaults to None
    :type access: List[DataAccess1], optional
    :param active_flag: Boolean that indicates whether the user is activated, defaults to None
    :type active_flag: bool, optional
    :param timezone_name: The user timezone name, defaults to None
    :type timezone_name: str, optional
    :param timezone_offset: The user timezone offset, defaults to None
    :type timezone_offset: str, optional
    :param role_id: The ID of the user role, defaults to None
    :type role_id: int, optional
    :param icon_url: The user icon URL, defaults to None
    :type icon_url: str, optional
    :param is_you: Boolean that indicates if the requested user is the same which is logged in (in this case, always true), defaults to None
    :type is_you: bool, optional
    :param is_deleted: Boolean that indicates whether the user is deleted from the company, defaults to None
    :type is_deleted: bool, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        default_currency: str = None,
        locale: str = None,
        lang: int = None,
        email: str = None,
        phone: str = None,
        activated: bool = None,
        last_login: str = None,
        created: str = None,
        modified: str = None,
        has_created_company: bool = None,
        access: List[DataAccess1] = None,
        active_flag: bool = None,
        timezone_name: str = None,
        timezone_offset: str = None,
        role_id: int = None,
        icon_url: str = None,
        is_you: bool = None,
        is_deleted: bool = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if default_currency is not None:
            self.default_currency = default_currency
        if locale is not None:
            self.locale = locale
        if lang is not None:
            self.lang = lang
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if activated is not None:
            self.activated = activated
        if last_login is not None:
            self.last_login = last_login
        if created is not None:
            self.created = created
        if modified is not None:
            self.modified = modified
        if has_created_company is not None:
            self.has_created_company = has_created_company
        if access is not None:
            self.access = self._define_list(access, DataAccess1)
        if active_flag is not None:
            self.active_flag = active_flag
        if timezone_name is not None:
            self.timezone_name = timezone_name
        if timezone_offset is not None:
            self.timezone_offset = timezone_offset
        if role_id is not None:
            self.role_id = role_id
        if icon_url is not None:
            self.icon_url = icon_url
        if is_you is not None:
            self.is_you = is_you
        if is_deleted is not None:
            self.is_deleted = is_deleted


@JsonMap({"id_": "id"})
class Data12(BaseModel):
    """Data12

    :param item: item, defaults to None
    :type item: Data12Item, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param data: data, defaults to None
    :type data: Data12Data, optional
    """

    def __init__(
        self, item: Data12Item = None, id_: int = None, data: Data12Data = None
    ):
        if item is not None:
            self.item = self._enum_matching(item, Data12Item.list(), "item")
        if id_ is not None:
            self.id_ = id_
        if data is not None:
            self.data = self._define_object(data, Data12Data)


class GetRecentsOkResponseDataGuard(OneOfBaseModel):
    class_list = {
        "Data1": Data1,
        "Data2": Data2,
        "Data3": Data3,
        "Data4": Data4,
        "Data5": Data5,
        "Data6": Data6,
        "Data7": Data7,
        "Data8": Data8,
        "Data9": Data9,
        "Data10": Data10,
        "Data11": Data11,
        "Data12": Data12,
    }


GetRecentsOkResponseData = Union[
    Data1,
    Data2,
    Data3,
    Data4,
    Data5,
    Data6,
    Data7,
    Data8,
    Data9,
    Data10,
    Data11,
    Data12,
]


@JsonMap({})
class AdditionalDataPagination18(BaseModel):
    """The additional data of the list

    :param start: Pagination start, defaults to None
    :type start: int, optional
    :param limit: Items shown per page, defaults to None
    :type limit: int, optional
    :param more_items_in_collection: If there are more list items in the collection than displayed or not, defaults to None
    :type more_items_in_collection: bool, optional
    """

    def __init__(
        self,
        start: int = None,
        limit: int = None,
        more_items_in_collection: bool = None,
    ):
        if start is not None:
            self.start = start
        if limit is not None:
            self.limit = limit
        if more_items_in_collection is not None:
            self.more_items_in_collection = more_items_in_collection


@JsonMap({})
class GetRecentsOkResponseAdditionalData(BaseModel):
    """GetRecentsOkResponseAdditionalData

    :param since_timestamp: The timestamp in UTC. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type since_timestamp: str, optional
    :param last_timestamp_on_page: The timestamp in UTC. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type last_timestamp_on_page: str, optional
    :param pagination: The additional data of the list, defaults to None
    :type pagination: AdditionalDataPagination18, optional
    """

    def __init__(
        self,
        since_timestamp: str = None,
        last_timestamp_on_page: str = None,
        pagination: AdditionalDataPagination18 = None,
    ):
        if since_timestamp is not None:
            self.since_timestamp = since_timestamp
        if last_timestamp_on_page is not None:
            self.last_timestamp_on_page = last_timestamp_on_page
        if pagination is not None:
            self.pagination = self._define_object(
                pagination, AdditionalDataPagination18
            )


@JsonMap({})
class GetRecentsOkResponse(BaseModel):
    """GetRecentsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetRecentsOkResponseData], optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: GetRecentsOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetRecentsOkResponseData] = None,
        additional_data: GetRecentsOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetRecentsOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetRecentsOkResponseAdditionalData
            )
