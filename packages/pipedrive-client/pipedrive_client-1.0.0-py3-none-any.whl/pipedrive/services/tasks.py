from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_task_request import UpdateTaskRequest
from ..models.update_task_ok_response import UpdateTaskOkResponse
from ..models.get_tasks_ok_response import GetTasksOkResponse
from ..models.get_tasks_done import GetTasksDone
from ..models.get_task_ok_response import GetTaskOkResponse
from ..models.delete_task_ok_response import DeleteTaskOkResponse
from ..models.add_task_request import AddTaskRequest
from ..models.add_task_created_response import AddTaskCreatedResponse


class TasksService(BaseService):

    @cast_models
    def get_tasks(
        self,
        cursor: str = None,
        limit: int = None,
        assignee_id: int = None,
        project_id: int = None,
        parent_task_id: int = None,
        done: GetTasksDone = None,
    ) -> GetTasksOkResponse:
        """Returns all tasks. This is a cursor-paginated endpoint. For more information, please refer to our documentation on <a href="https://pipedrive.readme.io/docs/core-api-concepts-pagination" target="_blank" rel="noopener noreferrer">pagination</a>.

        :param cursor: For pagination, the marker (an opaque string value) representing the first item on the next page, defaults to None
        :type cursor: str, optional
        :param limit: For pagination, the limit of entries to be returned. If not provided, up to 500 items will be returned., defaults to None
        :type limit: int, optional
        :param assignee_id: If supplied, only tasks that are assigned to this user are returned, defaults to None
        :type assignee_id: int, optional
        :param project_id: If supplied, only tasks that are assigned to this project are returned, defaults to None
        :type project_id: int, optional
        :param parent_task_id: If `null` is supplied then only parent tasks are returned. If integer is supplied then only subtasks of a specific task are returned. By default all tasks are returned., defaults to None
        :type parent_task_id: int, optional
        :param done: Whether the task is done or not. `0` = Not done, `1` = Done. If not omitted then returns both done and not done tasks., defaults to None
        :type done: GetTasksDone, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of tasks.
        :rtype: GetTasksOkResponse
        """

        Validator(str).is_optional().validate(cursor)
        Validator(int).is_optional().validate(limit)
        Validator(int).is_optional().validate(assignee_id)
        Validator(int).is_optional().validate(project_id)
        Validator(int).is_optional().validate(parent_task_id)
        Validator(GetTasksDone).is_optional().validate(done)

        serialized_request = (
            Serializer(f"{self.base_url}/tasks", self.get_default_headers())
            .add_query("cursor", cursor)
            .add_query("limit", limit)
            .add_query("assignee_id", assignee_id)
            .add_query("project_id", project_id)
            .add_query("parent_task_id", parent_task_id)
            .add_query("done", done)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetTasksOkResponse._unmap(response)

    @cast_models
    def add_task(self, request_body: AddTaskRequest = None) -> AddTaskCreatedResponse:
        """Adds a new task.

        :param request_body: The request body., defaults to None
        :type request_body: AddTaskRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Created task.
        :rtype: AddTaskCreatedResponse
        """

        Validator(AddTaskRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/tasks", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddTaskCreatedResponse._unmap(response)

    @cast_models
    def get_task(self, id_: int) -> GetTaskOkResponse:
        """Returns the details of a specific task.

        :param id_: The ID of the task
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get a task.
        :rtype: GetTaskOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/tasks/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetTaskOkResponse._unmap(response)

    @cast_models
    def update_task(
        self, id_: int, request_body: UpdateTaskRequest = None
    ) -> UpdateTaskOkResponse:
        """Updates a task.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateTaskRequest, optional
        :param id_: The ID of the task
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Updated task.
        :rtype: UpdateTaskOkResponse
        """

        Validator(UpdateTaskRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/tasks/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateTaskOkResponse._unmap(response)

    @cast_models
    def delete_task(self, id_: int) -> DeleteTaskOkResponse:
        """Marks a task as deleted. If the task has subtasks then those will also be deleted.

        :param id_: The ID of the task
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Deleted task.
        :rtype: DeleteTaskOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/tasks/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteTaskOkResponse._unmap(response)
