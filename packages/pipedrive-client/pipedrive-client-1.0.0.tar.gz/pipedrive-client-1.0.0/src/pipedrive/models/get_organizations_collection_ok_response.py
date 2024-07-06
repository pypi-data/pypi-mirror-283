from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class GetOrganizationsCollectionOkResponseData(BaseModel):
    """GetOrganizationsCollectionOkResponseData

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
    :param id_: The ID of the organization, defaults to None
    :type id_: int, optional
    :param active_flag: Whether the organization is active or not, defaults to None
    :type active_flag: bool, optional
    :param owner_id: The ID of the owner, defaults to None
    :type owner_id: int, optional
    :param name: The name of the organization, defaults to None
    :type name: str, optional
    :param update_time: The last updated date and time of the organization. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type update_time: str, optional
    :param delete_time: The date and time this organization was deleted. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type delete_time: str, optional
    :param add_time: The date and time when the organization was added/created. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    :param visible_to: The visibility group ID of who can see the organization, defaults to None
    :type visible_to: str, optional
    :param label: The label assigned to the organization, defaults to None
    :type label: int, optional
    :param cc_email: The BCC email associated with the organization, defaults to None
    :type cc_email: str, optional
    """

    def __init__(
        self,
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
        id_: int = None,
        active_flag: bool = None,
        owner_id: int = None,
        name: str = None,
        update_time: str = None,
        delete_time: str = None,
        add_time: str = None,
        visible_to: str = None,
        label: int = None,
        cc_email: str = None,
    ):
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
        if id_ is not None:
            self.id_ = id_
        if active_flag is not None:
            self.active_flag = active_flag
        if owner_id is not None:
            self.owner_id = owner_id
        if name is not None:
            self.name = name
        if update_time is not None:
            self.update_time = update_time
        if delete_time is not None:
            self.delete_time = delete_time
        if add_time is not None:
            self.add_time = add_time
        if visible_to is not None:
            self.visible_to = visible_to
        if label is not None:
            self.label = label
        if cc_email is not None:
            self.cc_email = cc_email


@JsonMap({})
class GetOrganizationsCollectionOkResponseAdditionalData(BaseModel):
    """The additional data of the list

    :param next_cursor: The first item on the next page. The value of the `next_cursor` field will be `null` if you have reached the end of the dataset and there’s no more pages to be returned., defaults to None
    :type next_cursor: str, optional
    """

    def __init__(self, next_cursor: str = None):
        if next_cursor is not None:
            self.next_cursor = next_cursor


@JsonMap({})
class GetOrganizationsCollectionOkResponse(BaseModel):
    """GetOrganizationsCollectionOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetOrganizationsCollectionOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetOrganizationsCollectionOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetOrganizationsCollectionOkResponseData] = None,
        additional_data: GetOrganizationsCollectionOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(
                data, GetOrganizationsCollectionOkResponseData
            )
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetOrganizationsCollectionOkResponseAdditionalData
            )
