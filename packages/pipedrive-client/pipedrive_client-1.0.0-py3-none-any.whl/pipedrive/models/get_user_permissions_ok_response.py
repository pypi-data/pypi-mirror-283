from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GetUserPermissionsOkResponseData(BaseModel):
    """GetUserPermissionsOkResponseData

    :param can_add_custom_fields: If the user can add custom fields, defaults to None
    :type can_add_custom_fields: bool, optional
    :param can_add_products: If the user can add products, defaults to None
    :type can_add_products: bool, optional
    :param can_add_prospects_as_leads: If the user can add prospects as leads, defaults to None
    :type can_add_prospects_as_leads: bool, optional
    :param can_bulk_edit_items: If the user can bulk edit items, defaults to None
    :type can_bulk_edit_items: bool, optional
    :param can_change_visibility_of_items: If the user can change visibility of items, defaults to None
    :type can_change_visibility_of_items: bool, optional
    :param can_convert_deals_to_leads: If the user can convert deals to leads, defaults to None
    :type can_convert_deals_to_leads: bool, optional
    :param can_create_own_workflow: If the user can create workflows, defaults to None
    :type can_create_own_workflow: bool, optional
    :param can_delete_activities: If the user can delete activities, defaults to None
    :type can_delete_activities: bool, optional
    :param can_delete_custom_fields: If the user can delete custom fields, defaults to None
    :type can_delete_custom_fields: bool, optional
    :param can_delete_deals: If the user can delete deals, defaults to None
    :type can_delete_deals: bool, optional
    :param can_edit_custom_fields: If the user can edit custom fields, defaults to None
    :type can_edit_custom_fields: bool, optional
    :param can_edit_deals_closed_date: If the user can edit deals' closed date, defaults to None
    :type can_edit_deals_closed_date: bool, optional
    :param can_edit_products: If the user can edit products, defaults to None
    :type can_edit_products: bool, optional
    :param can_edit_shared_filters: If the user can edit shared filters, defaults to None
    :type can_edit_shared_filters: bool, optional
    :param can_export_data_from_lists: If the user can export data from item lists, defaults to None
    :type can_export_data_from_lists: bool, optional
    :param can_follow_other_users: If the user can follow other users, defaults to None
    :type can_follow_other_users: bool, optional
    :param can_merge_deals: If the user can merge deals, defaults to None
    :type can_merge_deals: bool, optional
    :param can_merge_organizations: If the user can merge organizations, defaults to None
    :type can_merge_organizations: bool, optional
    :param can_merge_people: If the user can merge people, defaults to None
    :type can_merge_people: bool, optional
    :param can_modify_labels: If the user can modify labels, defaults to None
    :type can_modify_labels: bool, optional
    :param can_see_company_wide_statistics: If the user can see company-wide statistics, defaults to None
    :type can_see_company_wide_statistics: bool, optional
    :param can_see_deals_list_summary: If the user can see the summary on the deals page, defaults to None
    :type can_see_deals_list_summary: bool, optional
    :param can_see_hidden_items_names: If the user can see the names of hidden items, defaults to None
    :type can_see_hidden_items_names: bool, optional
    :param can_see_other_users: If the user can see other users, defaults to None
    :type can_see_other_users: bool, optional
    :param can_see_other_users_statistics: If the user can see other users' statistics, defaults to None
    :type can_see_other_users_statistics: bool, optional
    :param can_see_security_dashboard: If the user can see security dashboard, defaults to None
    :type can_see_security_dashboard: bool, optional
    :param can_share_filters: If the user can share filters, defaults to None
    :type can_share_filters: bool, optional
    :param can_share_insights: If the user can share insights, defaults to None
    :type can_share_insights: bool, optional
    :param can_use_api: If the user can use API, defaults to None
    :type can_use_api: bool, optional
    :param can_use_email_tracking: If the user can use email tracking, defaults to None
    :type can_use_email_tracking: bool, optional
    :param can_use_import: If the user can use import, defaults to None
    :type can_use_import: bool, optional
    """

    def __init__(
        self,
        can_add_custom_fields: bool = None,
        can_add_products: bool = None,
        can_add_prospects_as_leads: bool = None,
        can_bulk_edit_items: bool = None,
        can_change_visibility_of_items: bool = None,
        can_convert_deals_to_leads: bool = None,
        can_create_own_workflow: bool = None,
        can_delete_activities: bool = None,
        can_delete_custom_fields: bool = None,
        can_delete_deals: bool = None,
        can_edit_custom_fields: bool = None,
        can_edit_deals_closed_date: bool = None,
        can_edit_products: bool = None,
        can_edit_shared_filters: bool = None,
        can_export_data_from_lists: bool = None,
        can_follow_other_users: bool = None,
        can_merge_deals: bool = None,
        can_merge_organizations: bool = None,
        can_merge_people: bool = None,
        can_modify_labels: bool = None,
        can_see_company_wide_statistics: bool = None,
        can_see_deals_list_summary: bool = None,
        can_see_hidden_items_names: bool = None,
        can_see_other_users: bool = None,
        can_see_other_users_statistics: bool = None,
        can_see_security_dashboard: bool = None,
        can_share_filters: bool = None,
        can_share_insights: bool = None,
        can_use_api: bool = None,
        can_use_email_tracking: bool = None,
        can_use_import: bool = None,
    ):
        if can_add_custom_fields is not None:
            self.can_add_custom_fields = can_add_custom_fields
        if can_add_products is not None:
            self.can_add_products = can_add_products
        if can_add_prospects_as_leads is not None:
            self.can_add_prospects_as_leads = can_add_prospects_as_leads
        if can_bulk_edit_items is not None:
            self.can_bulk_edit_items = can_bulk_edit_items
        if can_change_visibility_of_items is not None:
            self.can_change_visibility_of_items = can_change_visibility_of_items
        if can_convert_deals_to_leads is not None:
            self.can_convert_deals_to_leads = can_convert_deals_to_leads
        if can_create_own_workflow is not None:
            self.can_create_own_workflow = can_create_own_workflow
        if can_delete_activities is not None:
            self.can_delete_activities = can_delete_activities
        if can_delete_custom_fields is not None:
            self.can_delete_custom_fields = can_delete_custom_fields
        if can_delete_deals is not None:
            self.can_delete_deals = can_delete_deals
        if can_edit_custom_fields is not None:
            self.can_edit_custom_fields = can_edit_custom_fields
        if can_edit_deals_closed_date is not None:
            self.can_edit_deals_closed_date = can_edit_deals_closed_date
        if can_edit_products is not None:
            self.can_edit_products = can_edit_products
        if can_edit_shared_filters is not None:
            self.can_edit_shared_filters = can_edit_shared_filters
        if can_export_data_from_lists is not None:
            self.can_export_data_from_lists = can_export_data_from_lists
        if can_follow_other_users is not None:
            self.can_follow_other_users = can_follow_other_users
        if can_merge_deals is not None:
            self.can_merge_deals = can_merge_deals
        if can_merge_organizations is not None:
            self.can_merge_organizations = can_merge_organizations
        if can_merge_people is not None:
            self.can_merge_people = can_merge_people
        if can_modify_labels is not None:
            self.can_modify_labels = can_modify_labels
        if can_see_company_wide_statistics is not None:
            self.can_see_company_wide_statistics = can_see_company_wide_statistics
        if can_see_deals_list_summary is not None:
            self.can_see_deals_list_summary = can_see_deals_list_summary
        if can_see_hidden_items_names is not None:
            self.can_see_hidden_items_names = can_see_hidden_items_names
        if can_see_other_users is not None:
            self.can_see_other_users = can_see_other_users
        if can_see_other_users_statistics is not None:
            self.can_see_other_users_statistics = can_see_other_users_statistics
        if can_see_security_dashboard is not None:
            self.can_see_security_dashboard = can_see_security_dashboard
        if can_share_filters is not None:
            self.can_share_filters = can_share_filters
        if can_share_insights is not None:
            self.can_share_insights = can_share_insights
        if can_use_api is not None:
            self.can_use_api = can_use_api
        if can_use_email_tracking is not None:
            self.can_use_email_tracking = can_use_email_tracking
        if can_use_import is not None:
            self.can_use_import = can_use_import


@JsonMap({})
class GetUserPermissionsOkResponse(BaseModel):
    """GetUserPermissionsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: GetUserPermissionsOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: GetUserPermissionsOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetUserPermissionsOkResponseData)
