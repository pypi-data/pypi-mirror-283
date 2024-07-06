from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_project_request import UpdateProjectRequest
from ..models.update_project_ok_response import UpdateProjectOkResponse
from ..models.put_project_plan_task_request import PutProjectPlanTaskRequest
from ..models.put_project_plan_task_ok_response import PutProjectPlanTaskOkResponse
from ..models.put_project_plan_activity_request import PutProjectPlanActivityRequest
from ..models.put_project_plan_activity_ok_response import (
    PutProjectPlanActivityOkResponse,
)
from ..models.get_projects_phases_ok_response import GetProjectsPhasesOkResponse
from ..models.get_projects_ok_response import GetProjectsOkResponse
from ..models.get_projects_boards_ok_response import GetProjectsBoardsOkResponse
from ..models.get_project_tasks_ok_response import GetProjectTasksOkResponse
from ..models.get_project_plan_ok_response import GetProjectPlanOkResponse
from ..models.get_project_ok_response import GetProjectOkResponse
from ..models.get_project_groups_ok_response import GetProjectGroupsOkResponse
from ..models.get_project_activities_ok_response import GetProjectActivitiesOkResponse
from ..models.delete_project_ok_response import DeleteProjectOkResponse
from ..models.archive_project_ok_response import ArchiveProjectOkResponse
from ..models.add_project_request import AddProjectRequest
from ..models.add_project_created_response import AddProjectCreatedResponse


class ProjectsService(BaseService):

    @cast_models
    def get_projects(
        self,
        cursor: str = None,
        limit: int = None,
        filter_id: int = None,
        status: str = None,
        phase_id: int = None,
        include_archived: bool = None,
    ) -> GetProjectsOkResponse:
        """Returns all projects. This is a cursor-paginated endpoint. For more information, please refer to our documentation on <a href="https://pipedrive.readme.io/docs/core-api-concepts-pagination" target="_blank" rel="noopener noreferrer">pagination</a>.

        :param cursor: For pagination, the marker (an opaque string value) representing the first item on the next page, defaults to None
        :type cursor: str, optional
        :param limit: For pagination, the limit of entries to be returned. If not provided, 100 items will be returned., defaults to None
        :type limit: int, optional
        :param filter_id: The ID of the filter to use, defaults to None
        :type filter_id: int, optional
        :param status: If supplied, includes only projects with the specified statuses. Possible values are `open`, `completed`, `canceled` and `deleted`. By default `deleted` projects are not returned., defaults to None
        :type status: str, optional
        :param phase_id: If supplied, only projects in specified phase are returned, defaults to None
        :type phase_id: int, optional
        :param include_archived: If supplied with `true` then archived projects are also included in the response. By default only not archived projects are returned., defaults to None
        :type include_archived: bool, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of projects.
        :rtype: GetProjectsOkResponse
        """

        Validator(str).is_optional().validate(cursor)
        Validator(int).is_optional().validate(limit)
        Validator(int).is_optional().validate(filter_id)
        Validator(str).is_optional().validate(status)
        Validator(int).is_optional().validate(phase_id)
        Validator(bool).is_optional().validate(include_archived)

        serialized_request = (
            Serializer(f"{self.base_url}/projects", self.get_default_headers())
            .add_query("cursor", cursor)
            .add_query("limit", limit)
            .add_query("filter_id", filter_id)
            .add_query("status", status)
            .add_query("phase_id", phase_id)
            .add_query("include_archived", include_archived)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProjectsOkResponse._unmap(response)

    @cast_models
    def add_project(
        self, request_body: AddProjectRequest = None
    ) -> AddProjectCreatedResponse:
        """Adds a new project. Note that you can supply additional custom fields along with the request that are not described here. These custom fields are different for each Pipedrive account and can be recognized by long hashes as keys.

        :param request_body: The request body., defaults to None
        :type request_body: AddProjectRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Created project.
        :rtype: AddProjectCreatedResponse
        """

        Validator(AddProjectRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/projects", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddProjectCreatedResponse._unmap(response)

    @cast_models
    def get_project(self, id_: int) -> GetProjectOkResponse:
        """Returns the details of a specific project. Also note that custom fields appear as long hashes in the resulting data. These hashes can be mapped against the `key` value of project fields.

        :param id_: The ID of the project
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get a project.
        :rtype: GetProjectOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/projects/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProjectOkResponse._unmap(response)

    @cast_models
    def update_project(
        self, id_: int, request_body: UpdateProjectRequest = None
    ) -> UpdateProjectOkResponse:
        """Updates a project.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateProjectRequest, optional
        :param id_: The ID of the project
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Updated project.
        :rtype: UpdateProjectOkResponse
        """

        Validator(UpdateProjectRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/projects/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateProjectOkResponse._unmap(response)

    @cast_models
    def delete_project(self, id_: int) -> DeleteProjectOkResponse:
        """Marks a project as deleted.

        :param id_: The ID of the project
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete a project.
        :rtype: DeleteProjectOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/projects/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteProjectOkResponse._unmap(response)

    @cast_models
    def archive_project(self, id_: int) -> ArchiveProjectOkResponse:
        """Archives a project.

        :param id_: The ID of the project
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Updated project.
        :rtype: ArchiveProjectOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/projects/{{id}}/archive", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)

        return ArchiveProjectOkResponse._unmap(response)

    @cast_models
    def get_project_plan(self, id_: int) -> GetProjectPlanOkResponse:
        """Returns information about items in a project plan. Items consists of tasks and activities and are linked to specific project phase and group.

        :param id_: The ID of the project
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get a project plan.
        :rtype: GetProjectPlanOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/projects/{{id}}/plan", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProjectPlanOkResponse._unmap(response)

    @cast_models
    def put_project_plan_activity(
        self,
        id_: int,
        activity_id: int,
        request_body: PutProjectPlanActivityRequest = None,
    ) -> PutProjectPlanActivityOkResponse:
        """Updates an activity phase or group in a project.

        :param request_body: The request body., defaults to None
        :type request_body: PutProjectPlanActivityRequest, optional
        :param id_: The ID of the project
        :type id_: int
        :param activity_id: The ID of the activity
        :type activity_id: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Updated activity in plan.
        :rtype: PutProjectPlanActivityOkResponse
        """

        Validator(PutProjectPlanActivityRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)
        Validator(int).validate(activity_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/projects/{{id}}/plan/activities/{{activityId}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("activityId", activity_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return PutProjectPlanActivityOkResponse._unmap(response)

    @cast_models
    def put_project_plan_task(
        self, id_: int, task_id: int, request_body: PutProjectPlanTaskRequest = None
    ) -> PutProjectPlanTaskOkResponse:
        """Updates a task phase or group in a project.

        :param request_body: The request body., defaults to None
        :type request_body: PutProjectPlanTaskRequest, optional
        :param id_: The ID of the project
        :type id_: int
        :param task_id: The ID of the task
        :type task_id: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Updated task in plan.
        :rtype: PutProjectPlanTaskOkResponse
        """

        Validator(PutProjectPlanTaskRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)
        Validator(int).validate(task_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/projects/{{id}}/plan/tasks/{{taskId}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("taskId", task_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return PutProjectPlanTaskOkResponse._unmap(response)

    @cast_models
    def get_project_groups(self, id_: int) -> GetProjectGroupsOkResponse:
        """Returns all active groups under a specific project.

        :param id_: The ID of the project
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get a project groups.
        :rtype: GetProjectGroupsOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/projects/{{id}}/groups", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProjectGroupsOkResponse._unmap(response)

    @cast_models
    def get_project_tasks(self, id_: int) -> GetProjectTasksOkResponse:
        """Returns tasks linked to a specific project.

        :param id_: The ID of the project
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of tasks.
        :rtype: GetProjectTasksOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/projects/{{id}}/tasks", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProjectTasksOkResponse._unmap(response)

    @cast_models
    def get_project_activities(self, id_: int) -> GetProjectActivitiesOkResponse:
        """Returns activities linked to a specific project.

        :param id_: The ID of the project
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of activities
        :rtype: GetProjectActivitiesOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/projects/{{id}}/activities",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProjectActivitiesOkResponse._unmap(response)

    @cast_models
    def get_projects_boards(self) -> GetProjectsBoardsOkResponse:
        """Returns all projects boards that are not deleted.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of project board.
        :rtype: GetProjectsBoardsOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/projects/boards", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProjectsBoardsOkResponse._unmap(response)

    @cast_models
    def get_projects_phases(self, board_id: int) -> GetProjectsPhasesOkResponse:
        """Returns all active project phases under a specific board.

        :param board_id: ID of the board for which phases are requested
        :type board_id: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of project phases.
        :rtype: GetProjectsPhasesOkResponse
        """

        Validator(int).validate(board_id)

        serialized_request = (
            Serializer(f"{self.base_url}/projects/phases", self.get_default_headers())
            .add_query("board_id", board_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProjectsPhasesOkResponse._unmap(response)
