from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DataPhone10(BaseModel):
    """DataPhone10

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
class DataEmail10(BaseModel):
    """DataEmail10

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
class PictureIdPictures19(BaseModel):
    """PictureIdPictures19

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
class DataPictureId13(BaseModel):
    """DataPictureId13

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
    :type pictures: PictureIdPictures19, optional
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
        pictures: PictureIdPictures19 = None,
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
            self.pictures = self._define_object(pictures, PictureIdPictures19)


@JsonMap({"id_": "id"})
class MergePersonsOkResponseData(BaseModel):
    """MergePersonsOkResponseData

    :param id_: The ID of the person, defaults to None
    :type id_: int, optional
    :param company_id: The ID of the company related to the person, defaults to None
    :type company_id: int, optional
    :param active_flag: Whether the person is active or not, defaults to None
    :type active_flag: bool, optional
    :param phone: A phone number supplied as a string or an array of phone objects related to the person. The structure of the array is as follows: `[{ "value": "12345", "primary": "true", "label": "mobile" }]`. Please note that only `value` is required., defaults to None
    :type phone: List[DataPhone10], optional
    :param email: An email address as a string or an array of email objects related to the person. The structure of the array is as follows: `[{ "value": "mail@example.com", "primary": "true", "label": "main" } ]`. Please note that only `value` is required., defaults to None
    :type email: List[DataEmail10], optional
    :param first_char: The first letter of the name of the person, defaults to None
    :type first_char: str, optional
    :param add_time: The date and time when the person was added/created. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    :param update_time: The last updated date and time of the person. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type update_time: str, optional
    :param visible_to: The visibility group ID of who can see the person, defaults to None
    :type visible_to: str, optional
    :param picture_id: picture_id, defaults to None
    :type picture_id: DataPictureId13, optional
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
        phone: List[DataPhone10] = None,
        email: List[DataEmail10] = None,
        first_char: str = None,
        add_time: str = None,
        update_time: str = None,
        visible_to: str = None,
        picture_id: DataPictureId13 = None,
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
            self.phone = self._define_list(phone, DataPhone10)
        if email is not None:
            self.email = self._define_list(email, DataEmail10)
        if first_char is not None:
            self.first_char = first_char
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if visible_to is not None:
            self.visible_to = visible_to
        if picture_id is not None:
            self.picture_id = self._define_object(picture_id, DataPictureId13)
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


@JsonMap({})
class MergePersonsOkResponse(BaseModel):
    """MergePersonsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: MergePersonsOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: MergePersonsOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, MergePersonsOkResponseData)
