from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DataPhone1(BaseModel):
    """DataPhone1

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
class DataEmail1(BaseModel):
    """DataEmail1

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
class PictureIdPictures1(BaseModel):
    """PictureIdPictures1

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
class DataPictureId1(BaseModel):
    """DataPictureId1

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
    :type pictures: PictureIdPictures1, optional
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
        pictures: PictureIdPictures1 = None,
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
            self.pictures = self._define_object(pictures, PictureIdPictures1)


@JsonMap({"id_": "id"})
class DataOwnerId1(BaseModel):
    """DataOwnerId1

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


@JsonMap({})
class DataOrgId5(BaseModel):
    """DataOrgId5

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
    :param value: The ID of the organization, defaults to None
    :type value: int, optional
    :param active_flag: Whether the associated organization is active or not, defaults to None
    :type active_flag: bool, optional
    """

    def __init__(
        self,
        name: str = None,
        people_count: int = None,
        owner_id: int = None,
        address: str = None,
        cc_email: str = None,
        value: int = None,
        active_flag: bool = None,
    ):
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
        if value is not None:
            self.value = value
        if active_flag is not None:
            self.active_flag = active_flag


@JsonMap({"id_": "id"})
class GetDealParticipantsOkResponseData(BaseModel):
    """GetDealParticipantsOkResponseData

    :param id_: The ID of the person, defaults to None
    :type id_: int, optional
    :param company_id: The ID of the company related to the person, defaults to None
    :type company_id: int, optional
    :param active_flag: Whether the person is active or not, defaults to None
    :type active_flag: bool, optional
    :param phone: A phone number supplied as a string or an array of phone objects related to the person. The structure of the array is as follows: `[{ "value": "12345", "primary": "true", "label": "mobile" }]`. Please note that only `value` is required., defaults to None
    :type phone: List[DataPhone1], optional
    :param email: An email address as a string or an array of email objects related to the person. The structure of the array is as follows: `[{ "value": "mail@example.com", "primary": "true", "label": "main" } ]`. Please note that only `value` is required., defaults to None
    :type email: List[DataEmail1], optional
    :param first_char: The first letter of the name of the person, defaults to None
    :type first_char: str, optional
    :param add_time: The date and time when the person was added/created. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    :param update_time: The last updated date and time of the person. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type update_time: str, optional
    :param visible_to: The visibility group ID of who can see the person, defaults to None
    :type visible_to: str, optional
    :param picture_id: picture_id, defaults to None
    :type picture_id: DataPictureId1, optional
    :param label: The label assigned to the person, defaults to None
    :type label: int, optional
    :param org_name: The name of the organization associated with the person, defaults to None
    :type org_name: str, optional
    :param owner_name: The name of the owner associated with the person, defaults to None
    :type owner_name: str, optional
    :param cc_email: The BCC email associated with the person, defaults to None
    :type cc_email: str, optional
    :param owner_id: owner_id, defaults to None
    :type owner_id: DataOwnerId1, optional
    :param org_id: org_id, defaults to None
    :type org_id: DataOrgId5, optional
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
    """

    def __init__(
        self,
        id_: int = None,
        company_id: int = None,
        active_flag: bool = None,
        phone: List[DataPhone1] = None,
        email: List[DataEmail1] = None,
        first_char: str = None,
        add_time: str = None,
        update_time: str = None,
        visible_to: str = None,
        picture_id: DataPictureId1 = None,
        label: int = None,
        org_name: str = None,
        owner_name: str = None,
        cc_email: str = None,
        owner_id: DataOwnerId1 = None,
        org_id: DataOrgId5 = None,
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
    ):
        if id_ is not None:
            self.id_ = id_
        if company_id is not None:
            self.company_id = company_id
        if active_flag is not None:
            self.active_flag = active_flag
        if phone is not None:
            self.phone = self._define_list(phone, DataPhone1)
        if email is not None:
            self.email = self._define_list(email, DataEmail1)
        if first_char is not None:
            self.first_char = first_char
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if visible_to is not None:
            self.visible_to = visible_to
        if picture_id is not None:
            self.picture_id = self._define_object(picture_id, DataPictureId1)
        if label is not None:
            self.label = label
        if org_name is not None:
            self.org_name = org_name
        if owner_name is not None:
            self.owner_name = owner_name
        if cc_email is not None:
            self.cc_email = cc_email
        if owner_id is not None:
            self.owner_id = self._define_object(owner_id, DataOwnerId1)
        if org_id is not None:
            self.org_id = self._define_object(org_id, DataOrgId5)
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


@JsonMap({})
class GetDealParticipantsOkResponseAdditionalData(BaseModel):
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


@JsonMap({"id_": "id"})
class UserUserId11(BaseModel):
    """UserUserId11

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
class RelatedObjectsUser11(BaseModel):
    """RelatedObjectsUser11

    :param user_id: user_id, defaults to None
    :type user_id: UserUserId11, optional
    """

    def __init__(self, user_id: UserUserId11 = None):
        if user_id is not None:
            self.user_id = self._define_object(user_id, UserUserId11)


@JsonMap({"id_": "id"})
class OrganizationOrganizationId11(BaseModel):
    """OrganizationOrganizationId11

    :param active_flag: Whether the associated organization is active or not, defaults to None
    :type active_flag: bool, optional
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
        active_flag: bool = None,
        id_: int = None,
        name: str = None,
        people_count: int = None,
        owner_id: int = None,
        address: str = None,
        cc_email: str = None,
    ):
        if active_flag is not None:
            self.active_flag = active_flag
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
class RelatedObjectsOrganization11(BaseModel):
    """RelatedObjectsOrganization11

    :param organization_id: organization_id, defaults to None
    :type organization_id: OrganizationOrganizationId11, optional
    """

    def __init__(self, organization_id: OrganizationOrganizationId11 = None):
        if organization_id is not None:
            self.organization_id = self._define_object(
                organization_id, OrganizationOrganizationId11
            )


@JsonMap({})
class PersonIdEmail15(BaseModel):
    """PersonIdEmail15

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
class PersonIdPhone15(BaseModel):
    """PersonIdPhone15

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
class PersonPersonId11(BaseModel):
    """PersonPersonId11

    :param active_flag: Whether the associated person is active or not, defaults to None
    :type active_flag: bool, optional
    :param id_: The ID of the person associated with the item, defaults to None
    :type id_: int, optional
    :param name: The name of the person associated with the item, defaults to None
    :type name: str, optional
    :param email: The emails of the person associated with the item, defaults to None
    :type email: List[PersonIdEmail15], optional
    :param phone: The phone numbers of the person associated with the item, defaults to None
    :type phone: List[PersonIdPhone15], optional
    :param owner_id: The ID of the owner of the person that is associated with the item, defaults to None
    :type owner_id: int, optional
    """

    def __init__(
        self,
        active_flag: bool = None,
        id_: int = None,
        name: str = None,
        email: List[PersonIdEmail15] = None,
        phone: List[PersonIdPhone15] = None,
        owner_id: int = None,
    ):
        if active_flag is not None:
            self.active_flag = active_flag
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if email is not None:
            self.email = self._define_list(email, PersonIdEmail15)
        if phone is not None:
            self.phone = self._define_list(phone, PersonIdPhone15)
        if owner_id is not None:
            self.owner_id = owner_id


@JsonMap({"person_id": "PERSON_ID"})
class RelatedObjectsPerson11(BaseModel):
    """RelatedObjectsPerson11

    :param person_id: person_id, defaults to None
    :type person_id: PersonPersonId11, optional
    """

    def __init__(self, person_id: PersonPersonId11 = None):
        if person_id is not None:
            self.person_id = self._define_object(person_id, PersonPersonId11)


@JsonMap({})
class GetDealParticipantsOkResponseRelatedObjects(BaseModel):
    """GetDealParticipantsOkResponseRelatedObjects

    :param user: user, defaults to None
    :type user: RelatedObjectsUser11, optional
    :param organization: organization, defaults to None
    :type organization: RelatedObjectsOrganization11, optional
    :param person: person, defaults to None
    :type person: RelatedObjectsPerson11, optional
    """

    def __init__(
        self,
        user: RelatedObjectsUser11 = None,
        organization: RelatedObjectsOrganization11 = None,
        person: RelatedObjectsPerson11 = None,
    ):
        if user is not None:
            self.user = self._define_object(user, RelatedObjectsUser11)
        if organization is not None:
            self.organization = self._define_object(
                organization, RelatedObjectsOrganization11
            )
        if person is not None:
            self.person = self._define_object(person, RelatedObjectsPerson11)


@JsonMap({})
class GetDealParticipantsOkResponse(BaseModel):
    """GetDealParticipantsOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of participants, defaults to None
    :type data: List[GetDealParticipantsOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetDealParticipantsOkResponseAdditionalData, optional
    :param related_objects: related_objects, defaults to None
    :type related_objects: GetDealParticipantsOkResponseRelatedObjects, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetDealParticipantsOkResponseData] = None,
        additional_data: GetDealParticipantsOkResponseAdditionalData = None,
        related_objects: GetDealParticipantsOkResponseRelatedObjects = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetDealParticipantsOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetDealParticipantsOkResponseAdditionalData
            )
        if related_objects is not None:
            self.related_objects = self._define_object(
                related_objects, GetDealParticipantsOkResponseRelatedObjects
            )
