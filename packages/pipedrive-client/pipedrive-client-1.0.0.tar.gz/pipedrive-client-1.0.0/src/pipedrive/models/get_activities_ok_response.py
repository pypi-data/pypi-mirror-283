from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id", "type_": "type"})
class GetActivitiesOkResponseData(BaseModel):
    """GetActivitiesOkResponseData

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


@JsonMap({})
class AdditionalDataPagination1(BaseModel):
    """Pagination details of the list

    :param start: Pagination start, defaults to None
    :type start: int, optional
    :param limit: Items shown per page, defaults to None
    :type limit: int, optional
    :param more_items_in_collection: Whether there are more list items in the collection than displayed, defaults to None
    :type more_items_in_collection: bool, optional
    :param next_start: Next pagination start, defaults to None
    :type next_start: int, optional
    """

    def __init__(
        self,
        start: int = None,
        limit: int = None,
        more_items_in_collection: bool = None,
        next_start: int = None,
    ):
        if start is not None:
            self.start = start
        if limit is not None:
            self.limit = limit
        if more_items_in_collection is not None:
            self.more_items_in_collection = more_items_in_collection
        if next_start is not None:
            self.next_start = next_start


@JsonMap({})
class GetActivitiesOkResponseAdditionalData(BaseModel):
    """GetActivitiesOkResponseAdditionalData

    :param pagination: Pagination details of the list, defaults to None
    :type pagination: AdditionalDataPagination1, optional
    """

    def __init__(self, pagination: AdditionalDataPagination1 = None):
        if pagination is not None:
            self.pagination = self._define_object(pagination, AdditionalDataPagination1)


@JsonMap({"id_": "id"})
class UserUserId1(BaseModel):
    """UserUserId1

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
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        email: str = None,
        has_pic: int = None,
        pic_hash: str = None,
        active_flag: bool = None,
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


@JsonMap({"user_id": "USER_ID"})
class RelatedObjectsUser1(BaseModel):
    """RelatedObjectsUser1

    :param user_id: user_id, defaults to None
    :type user_id: UserUserId1, optional
    """

    def __init__(self, user_id: UserUserId1 = None):
        if user_id is not None:
            self.user_id = self._define_object(user_id, UserUserId1)


@JsonMap({"id_": "id"})
class DealDealId1(BaseModel):
    """The ID of the deal which is associated with the item

    :param id_: The ID of the deal associated with the item, defaults to None
    :type id_: int, optional
    :param title: The title of the deal associated with the item, defaults to None
    :type title: str, optional
    :param status: The status of the deal associated with the item, defaults to None
    :type status: str, optional
    :param value: The value of the deal that is associated with the item, defaults to None
    :type value: float, optional
    :param currency: The currency of the deal value, defaults to None
    :type currency: str, optional
    :param stage_id: The ID of the stage the deal is currently at, defaults to None
    :type stage_id: int, optional
    :param pipeline_id: The ID of the pipeline the deal is in, defaults to None
    :type pipeline_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        title: str = None,
        status: str = None,
        value: float = None,
        currency: str = None,
        stage_id: int = None,
        pipeline_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if title is not None:
            self.title = title
        if status is not None:
            self.status = status
        if value is not None:
            self.value = value
        if currency is not None:
            self.currency = currency
        if stage_id is not None:
            self.stage_id = stage_id
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id


@JsonMap({"deal_id": "DEAL_ID"})
class RelatedObjectsDeal1(BaseModel):
    """RelatedObjectsDeal1

    :param deal_id: The ID of the deal which is associated with the item, defaults to None
    :type deal_id: DealDealId1, optional
    """

    def __init__(self, deal_id: DealDealId1 = None):
        if deal_id is not None:
            self.deal_id = self._define_object(deal_id, DealDealId1)


@JsonMap({})
class PersonIdEmail1(BaseModel):
    """PersonIdEmail1

    :param label: The type of the email, defaults to None
    :type label: str, optional
    :param value: The email of the associated person, defaults to None
    :type value: str, optional
    :param primary: Whether this is the primary email or not, defaults to None
    :type primary: bool, optional
    """

    def __init__(self, label: str = None, value: str = None, primary: bool = None):
        if label is not None:
            self.label = label
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary


@JsonMap({})
class PersonIdPhone1(BaseModel):
    """PersonIdPhone1

    :param label: The type of the phone number, defaults to None
    :type label: str, optional
    :param value: The phone number of the person associated with the item, defaults to None
    :type value: str, optional
    :param primary: Whether this is the primary phone number or not, defaults to None
    :type primary: bool, optional
    """

    def __init__(self, label: str = None, value: str = None, primary: bool = None):
        if label is not None:
            self.label = label
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary


@JsonMap({"id_": "id"})
class PersonPersonId1(BaseModel):
    """PersonPersonId1

    :param id_: The ID of the person associated with the item, defaults to None
    :type id_: int, optional
    :param name: The name of the person associated with the item, defaults to None
    :type name: str, optional
    :param email: The emails of the person associated with the item, defaults to None
    :type email: List[PersonIdEmail1], optional
    :param phone: The phone numbers of the person associated with the item, defaults to None
    :type phone: List[PersonIdPhone1], optional
    :param owner_id: The ID of the owner of the person that is associated with the item, defaults to None
    :type owner_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        email: List[PersonIdEmail1] = None,
        phone: List[PersonIdPhone1] = None,
        owner_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if email is not None:
            self.email = self._define_list(email, PersonIdEmail1)
        if phone is not None:
            self.phone = self._define_list(phone, PersonIdPhone1)
        if owner_id is not None:
            self.owner_id = owner_id


@JsonMap({"person_id": "PERSON_ID"})
class RelatedObjectsPerson1(BaseModel):
    """RelatedObjectsPerson1

    :param person_id: person_id, defaults to None
    :type person_id: PersonPersonId1, optional
    """

    def __init__(self, person_id: PersonPersonId1 = None):
        if person_id is not None:
            self.person_id = self._define_object(person_id, PersonPersonId1)


@JsonMap({"id_": "id"})
class OrganizationOrganizationId1(BaseModel):
    """OrganizationOrganizationId1

    :param id_: The ID of the organization associated with the item, defaults to None
    :type id_: int, optional
    :param name: The name of the organization associated with the item, defaults to None
    :type name: str, optional
    :param people_count: The number of people connected with the organization that is associated with the item, defaults to None
    :type people_count: int, optional
    :param owner_id: The ID of the owner of the organization that is associated with the item, defaults to None
    :type owner_id: int, optional
    :param address: The address of the organization, defaults to None
    :type address: str, optional
    :param cc_email: The BCC email of the organization associated with the item, defaults to None
    :type cc_email: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        people_count: int = None,
        owner_id: int = None,
        address: str = None,
        cc_email: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if people_count is not None:
            self.people_count = people_count
        if owner_id is not None:
            self.owner_id = owner_id
        if address is not None:
            self.address = address
        if cc_email is not None:
            self.cc_email = cc_email


@JsonMap({"organization_id": "ORGANIZATION_ID"})
class RelatedObjectsOrganization1(BaseModel):
    """RelatedObjectsOrganization1

    :param organization_id: organization_id, defaults to None
    :type organization_id: OrganizationOrganizationId1, optional
    """

    def __init__(self, organization_id: OrganizationOrganizationId1 = None):
        if organization_id is not None:
            self.organization_id = self._define_object(
                organization_id, OrganizationOrganizationId1
            )


@JsonMap({})
class GetActivitiesOkResponseRelatedObjects(BaseModel):
    """GetActivitiesOkResponseRelatedObjects

    :param user: user, defaults to None
    :type user: RelatedObjectsUser1, optional
    :param deal: deal, defaults to None
    :type deal: RelatedObjectsDeal1, optional
    :param person: person, defaults to None
    :type person: RelatedObjectsPerson1, optional
    :param organization: organization, defaults to None
    :type organization: RelatedObjectsOrganization1, optional
    """

    def __init__(
        self,
        user: RelatedObjectsUser1 = None,
        deal: RelatedObjectsDeal1 = None,
        person: RelatedObjectsPerson1 = None,
        organization: RelatedObjectsOrganization1 = None,
    ):
        if user is not None:
            self.user = self._define_object(user, RelatedObjectsUser1)
        if deal is not None:
            self.deal = self._define_object(deal, RelatedObjectsDeal1)
        if person is not None:
            self.person = self._define_object(person, RelatedObjectsPerson1)
        if organization is not None:
            self.organization = self._define_object(
                organization, RelatedObjectsOrganization1
            )


@JsonMap({})
class GetActivitiesOkResponse(BaseModel):
    """GetActivitiesOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetActivitiesOkResponseData], optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: GetActivitiesOkResponseAdditionalData, optional
    :param related_objects: related_objects, defaults to None
    :type related_objects: GetActivitiesOkResponseRelatedObjects, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetActivitiesOkResponseData] = None,
        additional_data: GetActivitiesOkResponseAdditionalData = None,
        related_objects: GetActivitiesOkResponseRelatedObjects = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetActivitiesOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetActivitiesOkResponseAdditionalData
            )
        if related_objects is not None:
            self.related_objects = self._define_object(
                related_objects, GetActivitiesOkResponseRelatedObjects
            )
