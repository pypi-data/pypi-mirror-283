from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DataOwnerId6(BaseModel):
    """DataOwnerId6

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
class PictureIdPictures8(BaseModel):
    """PictureIdPictures8

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
class DataPictureId6(BaseModel):
    """DataPictureId6

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
    :type pictures: PictureIdPictures8, optional
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
        pictures: PictureIdPictures8 = None,
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
            self.pictures = self._define_object(pictures, PictureIdPictures8)


@JsonMap({"id_": "id"})
class GetOrganizationOkResponseData(BaseModel):
    """GetOrganizationOkResponseData

    :param id_: The ID of the organization, defaults to None
    :type id_: int, optional
    :param company_id: The ID of the company related to the organization, defaults to None
    :type company_id: int, optional
    :param owner_id: owner_id, defaults to None
    :type owner_id: DataOwnerId6, optional
    :param name: The name of the organization, defaults to None
    :type name: str, optional
    :param active_flag: Whether the organization is active or not, defaults to None
    :type active_flag: bool, optional
    :param picture_id: picture_id, defaults to None
    :type picture_id: DataPictureId6, optional
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
    :param edit_name: If the company ID of the organization and company ID of the request is same or not, defaults to None
    :type edit_name: bool, optional
    :param last_activity: Please refer to response schema of <a href="https://developers.pipedrive.com/docs/api/v1/Activities#getActivity">Activity</a>, defaults to None
    :type last_activity: dict, optional
    :param next_activity: Please refer to response schema of <a href="https://developers.pipedrive.com/docs/api/v1/Activities#getActivity">Activity</a>, defaults to None
    :type next_activity: dict, optional
    """

    def __init__(
        self,
        id_: int = None,
        company_id: int = None,
        owner_id: DataOwnerId6 = None,
        name: str = None,
        active_flag: bool = None,
        picture_id: DataPictureId6 = None,
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
        edit_name: bool = None,
        last_activity: dict = None,
        next_activity: dict = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if company_id is not None:
            self.company_id = company_id
        if owner_id is not None:
            self.owner_id = self._define_object(owner_id, DataOwnerId6)
        if name is not None:
            self.name = name
        if active_flag is not None:
            self.active_flag = active_flag
        if picture_id is not None:
            self.picture_id = self._define_object(picture_id, DataPictureId6)
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
        if edit_name is not None:
            self.edit_name = edit_name
        if last_activity is not None:
            self.last_activity = last_activity
        if next_activity is not None:
            self.next_activity = next_activity


@JsonMap({"id_": "id"})
class FollowerUserId(BaseModel):
    """FollowerUserId

    :param id_: The ID of the follower associated with the item, defaults to None
    :type id_: int, optional
    :param name: The name of the follower, defaults to None
    :type name: str, optional
    :param email: The email of the follower, defaults to None
    :type email: str, optional
    :param user_id: The user ID of the follower, defaults to None
    :type user_id: int, optional
    :param pic_hash: The follower picture hash, defaults to None
    :type pic_hash: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        email: str = None,
        user_id: int = None,
        pic_hash: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if user_id is not None:
            self.user_id = user_id
        if pic_hash is not None:
            self.pic_hash = pic_hash


@JsonMap({"follower_user_id": "FOLLOWER_USER_ID"})
class Followers(BaseModel):
    """The follower that is associated with the item

    :param follower_user_id: follower_user_id, defaults to None
    :type follower_user_id: FollowerUserId, optional
    """

    def __init__(self, follower_user_id: FollowerUserId = None):
        if follower_user_id is not None:
            self.follower_user_id = self._define_object(
                follower_user_id, FollowerUserId
            )


@JsonMap({})
class GetOrganizationOkResponseAdditionalData(BaseModel):
    """GetOrganizationOkResponseAdditionalData

    :param followers: The follower that is associated with the item, defaults to None
    :type followers: Followers, optional
    :param dropbox_email: Dropbox email for the organization, defaults to None
    :type dropbox_email: str, optional
    """

    def __init__(self, followers: Followers = None, dropbox_email: str = None):
        if followers is not None:
            self.followers = self._define_object(followers, Followers)
        if dropbox_email is not None:
            self.dropbox_email = dropbox_email


@JsonMap({"id_": "id"})
class OrganizationOrganizationId15(BaseModel):
    """OrganizationOrganizationId15

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
class RelatedObjectsOrganization15(BaseModel):
    """RelatedObjectsOrganization15

    :param organization_id: organization_id, defaults to None
    :type organization_id: OrganizationOrganizationId15, optional
    """

    def __init__(self, organization_id: OrganizationOrganizationId15 = None):
        if organization_id is not None:
            self.organization_id = self._define_object(
                organization_id, OrganizationOrganizationId15
            )


@JsonMap({"id_": "id"})
class UserUserId17(BaseModel):
    """UserUserId17

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
class RelatedObjectsUser17(BaseModel):
    """RelatedObjectsUser17

    :param user_id: user_id, defaults to None
    :type user_id: UserUserId17, optional
    """

    def __init__(self, user_id: UserUserId17 = None):
        if user_id is not None:
            self.user_id = self._define_object(user_id, UserUserId17)


@JsonMap({"_128": "128", "_512": "512"})
class PictureIdPictures9(BaseModel):
    """PictureIdPictures9

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
class PicturePictureId3(BaseModel):
    """PicturePictureId3

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
    :type pictures: PictureIdPictures9, optional
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
        pictures: PictureIdPictures9 = None,
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
            self.pictures = self._define_object(pictures, PictureIdPictures9)


@JsonMap({"picture_id": "PICTURE_ID"})
class RelatedObjectsPicture3(BaseModel):
    """The picture that is associated with the item

    :param picture_id: picture_id, defaults to None
    :type picture_id: PicturePictureId3, optional
    """

    def __init__(self, picture_id: PicturePictureId3 = None):
        if picture_id is not None:
            self.picture_id = self._define_object(picture_id, PicturePictureId3)


@JsonMap({})
class GetOrganizationOkResponseRelatedObjects(BaseModel):
    """GetOrganizationOkResponseRelatedObjects

    :param organization: organization, defaults to None
    :type organization: RelatedObjectsOrganization15, optional
    :param user: user, defaults to None
    :type user: RelatedObjectsUser17, optional
    :param picture: The picture that is associated with the item, defaults to None
    :type picture: RelatedObjectsPicture3, optional
    """

    def __init__(
        self,
        organization: RelatedObjectsOrganization15 = None,
        user: RelatedObjectsUser17 = None,
        picture: RelatedObjectsPicture3 = None,
    ):
        if organization is not None:
            self.organization = self._define_object(
                organization, RelatedObjectsOrganization15
            )
        if user is not None:
            self.user = self._define_object(user, RelatedObjectsUser17)
        if picture is not None:
            self.picture = self._define_object(picture, RelatedObjectsPicture3)


@JsonMap({})
class GetOrganizationOkResponse(BaseModel):
    """GetOrganizationOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: GetOrganizationOkResponseData, optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: GetOrganizationOkResponseAdditionalData, optional
    :param related_objects: related_objects, defaults to None
    :type related_objects: GetOrganizationOkResponseRelatedObjects, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: GetOrganizationOkResponseData = None,
        additional_data: GetOrganizationOkResponseAdditionalData = None,
        related_objects: GetOrganizationOkResponseRelatedObjects = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetOrganizationOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetOrganizationOkResponseAdditionalData
            )
        if related_objects is not None:
            self.related_objects = self._define_object(
                related_objects, GetOrganizationOkResponseRelatedObjects
            )
