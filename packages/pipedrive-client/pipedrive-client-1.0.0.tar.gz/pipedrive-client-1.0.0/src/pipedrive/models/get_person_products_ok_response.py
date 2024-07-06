from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DealIdDeal(BaseModel):
    """DealIdDeal

    :param id_: The ID of the deal, defaults to None
    :type id_: int, optional
    :param company_id: The ID of the company, defaults to None
    :type company_id: int, optional
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
    :param first_add_time: The first creation date and time of the deal, defaults to None
    :type first_add_time: str, optional
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
    """

    def __init__(
        self,
        id_: int = None,
        company_id: int = None,
        creator_user_id: int = None,
        user_id: int = None,
        person_id: int = None,
        org_id: int = None,
        stage_id: int = None,
        title: str = None,
        value: float = None,
        currency: str = None,
        add_time: str = None,
        first_add_time: str = None,
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
    ):
        if id_ is not None:
            self.id_ = id_
        if company_id is not None:
            self.company_id = company_id
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
        if first_add_time is not None:
            self.first_add_time = first_add_time
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


class ProductVisibleTo2(Enum):
    """An enumeration representing different categories.

    :cvar _1: "1"
    :vartype _1: str
    :cvar _3: "3"
    :vartype _3: str
    :cvar _5: "5"
    :vartype _5: str
    :cvar _7: "7"
    :vartype _7: str
    """

    _1 = "1"
    _3 = "3"
    _5 = "5"
    _7 = "7"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ProductVisibleTo2._member_map_.values()))


@JsonMap({"id_": "id"})
class DealIdProduct(BaseModel):
    """DealIdProduct

    :param id_: The ID of the product, defaults to None
    :type id_: int, optional
    :param company_id: The ID of the company, defaults to None
    :type company_id: int, optional
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
    :param visible_to: visible_to, defaults to None
    :type visible_to: ProductVisibleTo2, optional
    :param owner_id: The ID of the user who will be marked as the owner of this product. When omitted, the authorized user ID will be used, defaults to None
    :type owner_id: int, optional
    :param files_count: The count of files, defaults to None
    :type files_count: int, optional
    :param add_time: The date and time when the product was added to the deal, defaults to None
    :type add_time: str, optional
    :param update_time: The date and time when the product was updated to the deal, defaults to None
    :type update_time: str, optional
    :param deal_id: The ID of the deal, defaults to None
    :type deal_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        company_id: int = None,
        name: str = None,
        code: str = None,
        description: str = None,
        unit: str = None,
        tax: float = None,
        category: str = None,
        active_flag: bool = None,
        selectable: bool = None,
        first_char: str = None,
        visible_to: ProductVisibleTo2 = None,
        owner_id: int = None,
        files_count: int = None,
        add_time: str = None,
        update_time: str = None,
        deal_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if company_id is not None:
            self.company_id = company_id
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
            self.visible_to = self._enum_matching(
                visible_to, ProductVisibleTo2.list(), "visible_to"
            )
        if owner_id is not None:
            self.owner_id = owner_id
        if files_count is not None:
            self.files_count = files_count
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if deal_id is not None:
            self.deal_id = deal_id


@JsonMap({})
class DataDealId(BaseModel):
    """DataDealId

    :param deal: deal, defaults to None
    :type deal: DealIdDeal, optional
    :param product: product, defaults to None
    :type product: DealIdProduct, optional
    """

    def __init__(self, deal: DealIdDeal = None, product: DealIdProduct = None):
        if deal is not None:
            self.deal = self._define_object(deal, DealIdDeal)
        if product is not None:
            self.product = self._define_object(product, DealIdProduct)


@JsonMap({"deal_id": "DEAL_ID"})
class GetPersonProductsOkResponseData(BaseModel):
    """GetPersonProductsOkResponseData

    :param deal_id: deal_id, defaults to None
    :type deal_id: DataDealId, optional
    """

    def __init__(self, deal_id: DataDealId = None):
        if deal_id is not None:
            self.deal_id = self._define_object(deal_id, DataDealId)


@JsonMap({})
class AdditionalDataPagination16(BaseModel):
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
class GetPersonProductsOkResponseAdditionalData(BaseModel):
    """GetPersonProductsOkResponseAdditionalData

    :param pagination: Pagination details of the list, defaults to None
    :type pagination: AdditionalDataPagination16, optional
    """

    def __init__(self, pagination: AdditionalDataPagination16 = None):
        if pagination is not None:
            self.pagination = self._define_object(
                pagination, AdditionalDataPagination16
            )


@JsonMap({})
class GetPersonProductsOkResponse(BaseModel):
    """GetPersonProductsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of deal products, defaults to None
    :type data: List[GetPersonProductsOkResponseData], optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: GetPersonProductsOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetPersonProductsOkResponseData] = None,
        additional_data: GetPersonProductsOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetPersonProductsOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetPersonProductsOkResponseAdditionalData
            )
