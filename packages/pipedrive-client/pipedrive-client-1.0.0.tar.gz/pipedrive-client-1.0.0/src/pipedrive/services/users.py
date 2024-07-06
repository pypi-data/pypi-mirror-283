from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_user_request import UpdateUserRequest
from ..models.update_user_ok_response import UpdateUserOkResponse
from ..models.search_by_email import SearchByEmail
from ..models.get_users_ok_response import GetUsersOkResponse
from ..models.get_user_role_settings_ok_response import GetUserRoleSettingsOkResponse
from ..models.get_user_role_assignments_ok_response import (
    GetUserRoleAssignmentsOkResponse,
)
from ..models.get_user_permissions_ok_response import GetUserPermissionsOkResponse
from ..models.get_user_ok_response import GetUserOkResponse
from ..models.get_user_followers_ok_response import GetUserFollowersOkResponse
from ..models.get_current_user_ok_response import GetCurrentUserOkResponse
from ..models.find_users_by_name_ok_response import FindUsersByNameOkResponse
from ..models.add_user_request import AddUserRequest
from ..models.add_user_ok_response import AddUserOkResponse


class UsersService(BaseService):

    @cast_models
    def get_users(self) -> GetUsersOkResponse:
        """Returns data about all users within the company.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The list of user objects
        :rtype: GetUsersOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/users", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetUsersOkResponse._unmap(response)

    @cast_models
    def add_user(self, request_body: AddUserRequest = None) -> AddUserOkResponse:
        """Adds a new user to the company, returns the ID upon success.

        :param request_body: The request body., defaults to None
        :type request_body: AddUserRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The data of the user
        :rtype: AddUserOkResponse
        """

        Validator(AddUserRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/users", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddUserOkResponse._unmap(response)

    @cast_models
    def find_users_by_name(
        self, term: str, search_by_email: SearchByEmail = None
    ) -> FindUsersByNameOkResponse:
        """Finds users by their name.

        :param term: The search term to look for
        :type term: str
        :param search_by_email: When enabled, the term will only be matched against email addresses of users. Default: `false`., defaults to None
        :type search_by_email: SearchByEmail, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The list of user objects
        :rtype: FindUsersByNameOkResponse
        """

        Validator(str).validate(term)
        Validator(SearchByEmail).is_optional().validate(search_by_email)

        serialized_request = (
            Serializer(f"{self.base_url}/users/find", self.get_default_headers())
            .add_query("term", term)
            .add_query("search_by_email", search_by_email)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return FindUsersByNameOkResponse._unmap(response)

    @cast_models
    def get_current_user(self) -> GetCurrentUserOkResponse:
        """Returns data about an authorized user within the company with bound company data: company ID, company name, and domain. Note that the `locale` property means 'Date/number format' in the Pipedrive account settings, not the chosen language.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The data of the logged in user
        :rtype: GetCurrentUserOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/users/me", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetCurrentUserOkResponse._unmap(response)

    @cast_models
    def get_user(self, id_: int) -> GetUserOkResponse:
        """Returns data about a specific user within the company.

        :param id_: The ID of the user
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The data of the user
        :rtype: GetUserOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/users/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetUserOkResponse._unmap(response)

    @cast_models
    def update_user(
        self, id_: int, request_body: UpdateUserRequest = None
    ) -> UpdateUserOkResponse:
        """Updates the properties of a user. Currently, only `active_flag` can be updated.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateUserRequest, optional
        :param id_: The ID of the user
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The data of the user
        :rtype: UpdateUserOkResponse
        """

        Validator(UpdateUserRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/users/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateUserOkResponse._unmap(response)

    @cast_models
    def get_user_followers(self, id_: int) -> GetUserFollowersOkResponse:
        """Lists the followers of a specific user.

        :param id_: The ID of the user
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The list of user IDs
        :rtype: GetUserFollowersOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/users/{{id}}/followers", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetUserFollowersOkResponse._unmap(response)

    @cast_models
    def get_user_permissions(self, id_: int) -> GetUserPermissionsOkResponse:
        """Lists aggregated permissions over all assigned permission sets for a user.

        :param id_: The ID of the user
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The list of user permissions
        :rtype: GetUserPermissionsOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/users/{{id}}/permissions", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetUserPermissionsOkResponse._unmap(response)

    @cast_models
    def get_user_role_assignments(
        self, id_: int, start: int = None, limit: int = None
    ) -> GetUserRoleAssignmentsOkResponse:
        """Lists role assignments for a user.

        :param id_: The ID of the user
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List assignments for a role
        :rtype: GetUserRoleAssignmentsOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/users/{{id}}/roleAssignments",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetUserRoleAssignmentsOkResponse._unmap(response)

    @cast_models
    def get_user_role_settings(self, id_: int) -> GetUserRoleSettingsOkResponse:
        """Lists the settings of user's assigned role.

        :param id_: The ID of the user
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List role settings
        :rtype: GetUserRoleSettingsOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/users/{{id}}/roleSettings", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetUserRoleSettingsOkResponse._unmap(response)
