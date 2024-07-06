from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_permission_sets_ok_response import GetPermissionSetsOkResponse
from ..models.get_permission_sets_app import GetPermissionSetsApp
from ..models.get_permission_set_ok_response import GetPermissionSetOkResponse
from ..models.get_permission_set_assignments_ok_response import (
    GetPermissionSetAssignmentsOkResponse,
)


class PermissionSetsService(BaseService):

    @cast_models
    def get_permission_sets(
        self, app: GetPermissionSetsApp = None
    ) -> GetPermissionSetsOkResponse:
        """Returns data about all permission sets.

        :param app: The app to filter the permission sets by, defaults to None
        :type app: GetPermissionSetsApp, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get all permissions
        :rtype: GetPermissionSetsOkResponse
        """

        Validator(GetPermissionSetsApp).is_optional().validate(app)

        serialized_request = (
            Serializer(f"{self.base_url}/permissionSets", self.get_default_headers())
            .add_query("app", app)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPermissionSetsOkResponse._unmap(response)

    @cast_models
    def get_permission_set(self, id_: str) -> GetPermissionSetOkResponse:
        """Returns data about a specific permission set.

        :param id_: The ID of the permission set
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The permission set of a specific user ID
        :rtype: GetPermissionSetOkResponse
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/permissionSets/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPermissionSetOkResponse._unmap(response)

    @cast_models
    def get_permission_set_assignments(
        self, id_: str, start: int = None, limit: int = None
    ) -> GetPermissionSetAssignmentsOkResponse:
        """Returns the list of assignments for a permission set.

        :param id_: The ID of the permission set
        :type id_: str
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The assignments of a specific user ID
        :rtype: GetPermissionSetAssignmentsOkResponse
        """

        Validator(str).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/permissionSets/{{id}}/assignments",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPermissionSetAssignmentsOkResponse._unmap(response)
