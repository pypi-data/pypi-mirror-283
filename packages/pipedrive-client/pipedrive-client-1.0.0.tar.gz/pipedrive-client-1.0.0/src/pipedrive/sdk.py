from .services.oauth import OauthService
from .services.activities import ActivitiesService
from .services.activity_fields import ActivityFieldsService
from .services.activity_types import ActivityTypesService
from .services.billing import BillingService
from .services.call_logs import CallLogsService
from .services.channels import ChannelsService
from .services.currencies import CurrenciesService
from .services.deals import DealsService
from .services.deal_fields import DealFieldsService
from .services.files import FilesService
from .services.filters import FiltersService
from .services.goals import GoalsService
from .services.item_search import ItemSearchService
from .services.leads import LeadsService
from .services.lead_labels import LeadLabelsService
from .services.lead_sources import LeadSourcesService
from .services.legacy_teams import LegacyTeamsService
from .services.mailbox import MailboxService
from .services.meetings import MeetingsService
from .services.notes import NotesService
from .services.note_fields import NoteFieldsService
from .services.organizations import OrganizationsService
from .services.organization_fields import OrganizationFieldsService
from .services.organization_relationships import OrganizationRelationshipsService
from .services.permission_sets import PermissionSetsService
from .services.persons import PersonsService
from .services.person_fields import PersonFieldsService
from .services.pipelines import PipelinesService
from .services.products import ProductsService
from .services.product_fields import ProductFieldsService
from .services.projects import ProjectsService
from .services.project_templates import ProjectTemplatesService
from .services.recents import RecentsService
from .services.roles import RolesService
from .services.stages import StagesService
from .services.subscriptions import SubscriptionsService
from .services.tasks import TasksService
from .services.users import UsersService
from .services.user_connections import UserConnectionsService
from .services.user_settings import UserSettingsService
from .services.webhooks import WebhooksService
from .net.environment import Environment


class Pipedrive:
    def __init__(
        self, access_token: str = None, base_url: str = Environment.DEFAULT.value
    ):
        """
        Initializes Pipedrive the SDK class.
        """
        self.oauth = OauthService(base_url=base_url)
        self.activities = ActivitiesService(base_url=base_url)
        self.activity_fields = ActivityFieldsService(base_url=base_url)
        self.activity_types = ActivityTypesService(base_url=base_url)
        self.billing = BillingService(base_url=base_url)
        self.call_logs = CallLogsService(base_url=base_url)
        self.channels = ChannelsService(base_url=base_url)
        self.currencies = CurrenciesService(base_url=base_url)
        self.deals = DealsService(base_url=base_url)
        self.deal_fields = DealFieldsService(base_url=base_url)
        self.files = FilesService(base_url=base_url)
        self.filters = FiltersService(base_url=base_url)
        self.goals = GoalsService(base_url=base_url)
        self.item_search = ItemSearchService(base_url=base_url)
        self.leads = LeadsService(base_url=base_url)
        self.lead_labels = LeadLabelsService(base_url=base_url)
        self.lead_sources = LeadSourcesService(base_url=base_url)
        self.legacy_teams = LegacyTeamsService(base_url=base_url)
        self.mailbox = MailboxService(base_url=base_url)
        self.meetings = MeetingsService(base_url=base_url)
        self.notes = NotesService(base_url=base_url)
        self.note_fields = NoteFieldsService(base_url=base_url)
        self.organizations = OrganizationsService(base_url=base_url)
        self.organization_fields = OrganizationFieldsService(base_url=base_url)
        self.organization_relationships = OrganizationRelationshipsService(
            base_url=base_url
        )
        self.permission_sets = PermissionSetsService(base_url=base_url)
        self.persons = PersonsService(base_url=base_url)
        self.person_fields = PersonFieldsService(base_url=base_url)
        self.pipelines = PipelinesService(base_url=base_url)
        self.products = ProductsService(base_url=base_url)
        self.product_fields = ProductFieldsService(base_url=base_url)
        self.projects = ProjectsService(base_url=base_url)
        self.project_templates = ProjectTemplatesService(base_url=base_url)
        self.recents = RecentsService(base_url=base_url)
        self.roles = RolesService(base_url=base_url)
        self.stages = StagesService(base_url=base_url)
        self.subscriptions = SubscriptionsService(base_url=base_url)
        self.tasks = TasksService(base_url=base_url)
        self.users = UsersService(base_url=base_url)
        self.user_connections = UserConnectionsService(base_url=base_url)
        self.user_settings = UserSettingsService(base_url=base_url)
        self.webhooks = WebhooksService(base_url=base_url)
        self.set_access_token(access_token)

    def set_base_url(self, base_url):
        """
        Sets the base URL for the entire SDK.
        """
        self.oauth.set_base_url(base_url)
        self.activities.set_base_url(base_url)
        self.activity_fields.set_base_url(base_url)
        self.activity_types.set_base_url(base_url)
        self.billing.set_base_url(base_url)
        self.call_logs.set_base_url(base_url)
        self.channels.set_base_url(base_url)
        self.currencies.set_base_url(base_url)
        self.deals.set_base_url(base_url)
        self.deal_fields.set_base_url(base_url)
        self.files.set_base_url(base_url)
        self.filters.set_base_url(base_url)
        self.goals.set_base_url(base_url)
        self.item_search.set_base_url(base_url)
        self.leads.set_base_url(base_url)
        self.lead_labels.set_base_url(base_url)
        self.lead_sources.set_base_url(base_url)
        self.legacy_teams.set_base_url(base_url)
        self.mailbox.set_base_url(base_url)
        self.meetings.set_base_url(base_url)
        self.notes.set_base_url(base_url)
        self.note_fields.set_base_url(base_url)
        self.organizations.set_base_url(base_url)
        self.organization_fields.set_base_url(base_url)
        self.organization_relationships.set_base_url(base_url)
        self.permission_sets.set_base_url(base_url)
        self.persons.set_base_url(base_url)
        self.person_fields.set_base_url(base_url)
        self.pipelines.set_base_url(base_url)
        self.products.set_base_url(base_url)
        self.product_fields.set_base_url(base_url)
        self.projects.set_base_url(base_url)
        self.project_templates.set_base_url(base_url)
        self.recents.set_base_url(base_url)
        self.roles.set_base_url(base_url)
        self.stages.set_base_url(base_url)
        self.subscriptions.set_base_url(base_url)
        self.tasks.set_base_url(base_url)
        self.users.set_base_url(base_url)
        self.user_connections.set_base_url(base_url)
        self.user_settings.set_base_url(base_url)
        self.webhooks.set_base_url(base_url)

        return self

    def set_access_token(self, access_token: str):
        """
        Sets the access token for the entire SDK.
        """
        self.oauth.set_access_token(access_token)
        self.activities.set_access_token(access_token)
        self.activity_fields.set_access_token(access_token)
        self.activity_types.set_access_token(access_token)
        self.billing.set_access_token(access_token)
        self.call_logs.set_access_token(access_token)
        self.channels.set_access_token(access_token)
        self.currencies.set_access_token(access_token)
        self.deals.set_access_token(access_token)
        self.deal_fields.set_access_token(access_token)
        self.files.set_access_token(access_token)
        self.filters.set_access_token(access_token)
        self.goals.set_access_token(access_token)
        self.item_search.set_access_token(access_token)
        self.leads.set_access_token(access_token)
        self.lead_labels.set_access_token(access_token)
        self.lead_sources.set_access_token(access_token)
        self.legacy_teams.set_access_token(access_token)
        self.mailbox.set_access_token(access_token)
        self.meetings.set_access_token(access_token)
        self.notes.set_access_token(access_token)
        self.note_fields.set_access_token(access_token)
        self.organizations.set_access_token(access_token)
        self.organization_fields.set_access_token(access_token)
        self.organization_relationships.set_access_token(access_token)
        self.permission_sets.set_access_token(access_token)
        self.persons.set_access_token(access_token)
        self.person_fields.set_access_token(access_token)
        self.pipelines.set_access_token(access_token)
        self.products.set_access_token(access_token)
        self.product_fields.set_access_token(access_token)
        self.projects.set_access_token(access_token)
        self.project_templates.set_access_token(access_token)
        self.recents.set_access_token(access_token)
        self.roles.set_access_token(access_token)
        self.stages.set_access_token(access_token)
        self.subscriptions.set_access_token(access_token)
        self.tasks.set_access_token(access_token)
        self.users.set_access_token(access_token)
        self.user_connections.set_access_token(access_token)
        self.user_settings.set_access_token(access_token)
        self.webhooks.set_access_token(access_token)

        return self


# c029837e0e474b76bc487506e8799df5e3335891efe4fb02bda7a1441840310c
