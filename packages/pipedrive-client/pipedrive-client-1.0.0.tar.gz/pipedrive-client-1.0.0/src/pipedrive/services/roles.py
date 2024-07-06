from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_role_request import UpdateRoleRequest
from ..models.update_role_pipelines_request import UpdateRolePipelinesRequest
from ..models.update_role_pipelines_ok_response import UpdateRolePipelinesOkResponse
from ..models.update_role_ok_response import UpdateRoleOkResponse
from ..models.get_roles_ok_response import GetRolesOkResponse
from ..models.get_role_settings_ok_response import GetRoleSettingsOkResponse
from ..models.get_role_pipelines_ok_response import GetRolePipelinesOkResponse
from ..models.get_role_ok_response import GetRoleOkResponse
from ..models.get_role_assignments_ok_response import GetRoleAssignmentsOkResponse
from ..models.delete_role_ok_response import DeleteRoleOkResponse
from ..models.delete_role_assignment_request import DeleteRoleAssignmentRequest
from ..models.delete_role_assignment_ok_response import DeleteRoleAssignmentOkResponse
from ..models.add_role_request import AddRoleRequest
from ..models.add_role_ok_response import AddRoleOkResponse
from ..models.add_role_assignment_request import AddRoleAssignmentRequest
from ..models.add_role_assignment_ok_response import AddRoleAssignmentOkResponse
from ..models.add_or_update_role_setting_request import AddOrUpdateRoleSettingRequest
from ..models.add_or_update_role_setting_ok_response import (
    AddOrUpdateRoleSettingOkResponse,
)


class RolesService(BaseService):

    @cast_models
    def get_roles(self, start: int = None, limit: int = None) -> GetRolesOkResponse:
        """Returns all the roles within the company.

        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get all roles
        :rtype: GetRolesOkResponse
        """

        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/roles", self.get_default_headers())
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetRolesOkResponse._unmap(response)

    @cast_models
    def add_role(self, request_body: AddRoleRequest = None) -> AddRoleOkResponse:
        """Adds a new role.

        :param request_body: The request body., defaults to None
        :type request_body: AddRoleRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add a role
        :rtype: AddRoleOkResponse
        """

        Validator(AddRoleRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/roles", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddRoleOkResponse._unmap(response)

    @cast_models
    def get_role(self, id_: int) -> GetRoleOkResponse:
        """Returns the details of a specific role.

        :param id_: The ID of the role
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get one role
        :rtype: GetRoleOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/roles/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetRoleOkResponse._unmap(response)

    @cast_models
    def update_role(
        self, id_: int, request_body: UpdateRoleRequest = None
    ) -> UpdateRoleOkResponse:
        """Updates the parent role and/or the name of a specific role.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateRoleRequest, optional
        :param id_: The ID of the role
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Update role details
        :rtype: UpdateRoleOkResponse
        """

        Validator(UpdateRoleRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/roles/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateRoleOkResponse._unmap(response)

    @cast_models
    def delete_role(self, id_: int) -> DeleteRoleOkResponse:
        """Marks a role as deleted.

        :param id_: The ID of the role
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete a role
        :rtype: DeleteRoleOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/roles/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteRoleOkResponse._unmap(response)

    @cast_models
    def get_role_assignments(
        self, id_: int, start: int = None, limit: int = None
    ) -> GetRoleAssignmentsOkResponse:
        """Returns all users assigned to a role.

        :param id_: The ID of the role
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List assignments for a role
        :rtype: GetRoleAssignmentsOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/roles/{{id}}/assignments", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetRoleAssignmentsOkResponse._unmap(response)

    @cast_models
    def add_role_assignment(
        self, id_: int, request_body: AddRoleAssignmentRequest = None
    ) -> AddRoleAssignmentOkResponse:
        """Assigns a user to a role.

        :param request_body: The request body., defaults to None
        :type request_body: AddRoleAssignmentRequest, optional
        :param id_: The ID of the role
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add assignment for a role
        :rtype: AddRoleAssignmentOkResponse
        """

        Validator(AddRoleAssignmentRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/roles/{{id}}/assignments", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddRoleAssignmentOkResponse._unmap(response)

    @cast_models
    def delete_role_assignment(
        self, id_: int, request_body: DeleteRoleAssignmentRequest = None
    ) -> DeleteRoleAssignmentOkResponse:
        """Removes the assigned user from a role and adds to the default role.

        :param request_body: The request body., defaults to None
        :type request_body: DeleteRoleAssignmentRequest, optional
        :param id_: The ID of the role
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete assignment from a role
        :rtype: DeleteRoleAssignmentOkResponse
        """

        Validator(DeleteRoleAssignmentRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/roles/{{id}}/assignments", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return DeleteRoleAssignmentOkResponse._unmap(response)

    @cast_models
    def get_role_settings(self, id_: int) -> GetRoleSettingsOkResponse:
        """Returns the visibility settings of a specific role.

        :param id_: The ID of the role
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List role settings
        :rtype: GetRoleSettingsOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/roles/{{id}}/settings", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetRoleSettingsOkResponse._unmap(response)

    @cast_models
    def add_or_update_role_setting(
        self, id_: int, request_body: AddOrUpdateRoleSettingRequest = None
    ) -> AddOrUpdateRoleSettingOkResponse:
        """Adds or updates the visibility setting for a role.

        :param request_body: The request body., defaults to None
        :type request_body: AddOrUpdateRoleSettingRequest, optional
        :param id_: The ID of the role
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List role settings
        :rtype: AddOrUpdateRoleSettingOkResponse
        """

        Validator(AddOrUpdateRoleSettingRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/roles/{{id}}/settings", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddOrUpdateRoleSettingOkResponse._unmap(response)

    @cast_models
    def get_role_pipelines(
        self, id_: int, visible: bool = None
    ) -> GetRolePipelinesOkResponse:
        """Returns the list of either visible or hidden pipeline IDs for a specific role. For more information on pipeline visibility, please refer to the <a href="https://support.pipedrive.com/en/article/visibility-groups" target="_blank" rel="noopener noreferrer">Visibility groups article</a>.

        :param id_: The ID of the role
        :type id_: int
        :param visible: Whether to return the visible or hidden pipelines for the role, defaults to None
        :type visible: bool, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get either visible or hidden pipeline ids for a role
        :rtype: GetRolePipelinesOkResponse
        """

        Validator(int).validate(id_)
        Validator(bool).is_optional().validate(visible)

        serialized_request = (
            Serializer(
                f"{self.base_url}/roles/{{id}}/pipelines", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("visible", visible)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetRolePipelinesOkResponse._unmap(response)

    @cast_models
    def update_role_pipelines(
        self, id_: int, request_body: UpdateRolePipelinesRequest = None
    ) -> UpdateRolePipelinesOkResponse:
        """Updates the specified pipelines to be visible and/or hidden for a specific role. For more information on pipeline visibility, please refer to the <a href="https://support.pipedrive.com/en/article/visibility-groups" target="_blank" rel="noopener noreferrer">Visibility groups article</a>.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateRolePipelinesRequest, optional
        :param id_: The ID of the role
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Update pipeline visibility for a role
        :rtype: UpdateRolePipelinesOkResponse
        """

        Validator(UpdateRolePipelinesRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/roles/{{id}}/pipelines", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateRolePipelinesOkResponse._unmap(response)
