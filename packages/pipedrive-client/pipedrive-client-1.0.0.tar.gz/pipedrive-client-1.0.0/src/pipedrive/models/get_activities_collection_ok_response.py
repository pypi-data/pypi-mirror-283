from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id", "type_": "type"})
class GetActivitiesCollectionOkResponseData(BaseModel):
    """GetActivitiesCollectionOkResponseData

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
    :param done: Whether the activity is done or not, defaults to None
    :type done: bool, optional
    :param subject: The subject of the activity, defaults to None
    :type subject: str, optional
    :param type_: The type of the activity. This is in correlation with the `key_string` parameter of ActivityTypes., defaults to None
    :type type_: str, optional
    :param user_id: The ID of the user whom the activity is assigned to, defaults to None
    :type user_id: int, optional
    :param busy_flag: Marks if the activity is set as 'Busy' or 'Free'. If the flag is set to `true`, your customers will not be able to book that time slot through any Scheduler links. The flag can also be unset. When the value of the flag is unset (`null`), the flag defaults to 'Busy' if it has a time set, and 'Free' if it is an all-day event without specified time., defaults to None
    :type busy_flag: bool, optional
    :param company_id: The user's company ID, defaults to None
    :type company_id: int, optional
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
    :param active_flag: Whether the activity is active or not, defaults to None
    :type active_flag: bool, optional
    :param update_time: The last update date and time of the activity. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    :param update_user_id: The ID of the user who was the last to update this activity, defaults to None
    :type update_user_id: int, optional
    :param source_timezone: The timezone the activity was created in an external calendar, defaults to None
    :type source_timezone: str, optional
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
        done: bool = None,
        subject: str = None,
        type_: str = None,
        user_id: int = None,
        busy_flag: bool = None,
        company_id: int = None,
        conference_meeting_client: str = None,
        conference_meeting_url: str = None,
        conference_meeting_id: str = None,
        add_time: str = None,
        marked_as_done_time: str = None,
        active_flag: bool = None,
        update_time: str = None,
        update_user_id: int = None,
        source_timezone: str = None,
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
        if done is not None:
            self.done = done
        if subject is not None:
            self.subject = subject
        if type_ is not None:
            self.type_ = type_
        if user_id is not None:
            self.user_id = user_id
        if busy_flag is not None:
            self.busy_flag = busy_flag
        if company_id is not None:
            self.company_id = company_id
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
        if active_flag is not None:
            self.active_flag = active_flag
        if update_time is not None:
            self.update_time = update_time
        if update_user_id is not None:
            self.update_user_id = update_user_id
        if source_timezone is not None:
            self.source_timezone = source_timezone
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


@JsonMap({})
class GetActivitiesCollectionOkResponseAdditionalData(BaseModel):
    """The additional data of the list

    :param next_cursor: The first item on the next page. The value of the `next_cursor` field will be `null` if you have reached the end of the dataset and there’s no more pages to be returned., defaults to None
    :type next_cursor: str, optional
    """

    def __init__(self, next_cursor: str = None):
        if next_cursor is not None:
            self.next_cursor = next_cursor


@JsonMap({})
class GetActivitiesCollectionOkResponse(BaseModel):
    """GetActivitiesCollectionOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetActivitiesCollectionOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetActivitiesCollectionOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetActivitiesCollectionOkResponseData] = None,
        additional_data: GetActivitiesCollectionOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetActivitiesCollectionOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetActivitiesCollectionOkResponseAdditionalData
            )
