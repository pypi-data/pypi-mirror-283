from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_team_request import UpdateTeamRequest
from ..models.update_team_ok_response import UpdateTeamOkResponse
from ..models.get_user_teams_skip_users import GetUserTeamsSkipUsers
from ..models.get_user_teams_order_by import GetUserTeamsOrderBy
from ..models.get_user_teams_ok_response import GetUserTeamsOkResponse
from ..models.get_teams_skip_users import GetTeamsSkipUsers
from ..models.get_teams_order_by import GetTeamsOrderBy
from ..models.get_teams_ok_response import GetTeamsOkResponse
from ..models.get_team_users_ok_response import GetTeamUsersOkResponse
from ..models.get_team_skip_users import GetTeamSkipUsers
from ..models.get_team_ok_response import GetTeamOkResponse
from ..models.delete_team_user_request import DeleteTeamUserRequest
from ..models.delete_team_user_ok_response import DeleteTeamUserOkResponse
from ..models.add_team_user_request import AddTeamUserRequest
from ..models.add_team_user_ok_response import AddTeamUserOkResponse
from ..models.add_team_request import AddTeamRequest
from ..models.add_team_ok_response import AddTeamOkResponse


class LegacyTeamsService(BaseService):

    @cast_models
    def get_teams(
        self, order_by: GetTeamsOrderBy = None, skip_users: GetTeamsSkipUsers = None
    ) -> GetTeamsOkResponse:
        """Returns data about teams within the company.

        :param order_by: The field name to sort returned teams by, defaults to None
        :type order_by: GetTeamsOrderBy, optional
        :param skip_users: When enabled, the teams will not include IDs of member users, defaults to None
        :type skip_users: GetTeamsSkipUsers, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The list of team objects
        :rtype: GetTeamsOkResponse
        """

        Validator(GetTeamsOrderBy).is_optional().validate(order_by)
        Validator(GetTeamsSkipUsers).is_optional().validate(skip_users)

        serialized_request = (
            Serializer(f"{self.base_url}/legacyTeams", self.get_default_headers())
            .add_query("order_by", order_by)
            .add_query("skip_users", skip_users)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetTeamsOkResponse._unmap(response)

    @cast_models
    def add_team(self, request_body: AddTeamRequest = None) -> AddTeamOkResponse:
        """Adds a new team to the company and returns the created object.

        :param request_body: The request body., defaults to None
        :type request_body: AddTeamRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The team data
        :rtype: AddTeamOkResponse
        """

        Validator(AddTeamRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/legacyTeams", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddTeamOkResponse._unmap(response)

    @cast_models
    def get_team(
        self, id_: int, skip_users: GetTeamSkipUsers = None
    ) -> GetTeamOkResponse:
        """Returns data about a specific team.

        :param id_: The ID of the team
        :type id_: int
        :param skip_users: When enabled, the teams will not include IDs of member users, defaults to None
        :type skip_users: GetTeamSkipUsers, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The team data
        :rtype: GetTeamOkResponse
        """

        Validator(int).validate(id_)
        Validator(GetTeamSkipUsers).is_optional().validate(skip_users)

        serialized_request = (
            Serializer(
                f"{self.base_url}/legacyTeams/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("skip_users", skip_users)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetTeamOkResponse._unmap(response)

    @cast_models
    def update_team(
        self, id_: int, request_body: UpdateTeamRequest = None
    ) -> UpdateTeamOkResponse:
        """Updates an existing team and returns the updated object.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateTeamRequest, optional
        :param id_: The ID of the team
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The team data
        :rtype: UpdateTeamOkResponse
        """

        Validator(UpdateTeamRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/legacyTeams/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateTeamOkResponse._unmap(response)

    @cast_models
    def get_team_users(self, id_: int) -> GetTeamUsersOkResponse:
        """Returns a list of all user IDs within a team.

        :param id_: The ID of the team
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of user IDs within a team
        :rtype: GetTeamUsersOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/legacyTeams/{{id}}/users", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetTeamUsersOkResponse._unmap(response)

    @cast_models
    def add_team_user(
        self, id_: int, request_body: AddTeamUserRequest = None
    ) -> AddTeamUserOkResponse:
        """Adds users to an existing team.

        :param request_body: The request body., defaults to None
        :type request_body: AddTeamUserRequest, optional
        :param id_: The ID of the team
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of user IDs within a team
        :rtype: AddTeamUserOkResponse
        """

        Validator(AddTeamUserRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/legacyTeams/{{id}}/users", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddTeamUserOkResponse._unmap(response)

    @cast_models
    def delete_team_user(
        self, id_: int, request_body: DeleteTeamUserRequest = None
    ) -> DeleteTeamUserOkResponse:
        """Deletes users from an existing team.

        :param request_body: The request body., defaults to None
        :type request_body: DeleteTeamUserRequest, optional
        :param id_: The ID of the team
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of user IDs within a team
        :rtype: DeleteTeamUserOkResponse
        """

        Validator(DeleteTeamUserRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/legacyTeams/{{id}}/users", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return DeleteTeamUserOkResponse._unmap(response)

    @cast_models
    def get_user_teams(
        self,
        id_: int,
        order_by: GetUserTeamsOrderBy = None,
        skip_users: GetUserTeamsSkipUsers = None,
    ) -> GetUserTeamsOkResponse:
        """Returns data about all teams which have the specified user as a member.

        :param id_: The ID of the user
        :type id_: int
        :param order_by: The field name to sort returned teams by, defaults to None
        :type order_by: GetUserTeamsOrderBy, optional
        :param skip_users: When enabled, the teams will not include IDs of member users, defaults to None
        :type skip_users: GetUserTeamsSkipUsers, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The list of team objects
        :rtype: GetUserTeamsOkResponse
        """

        Validator(int).validate(id_)
        Validator(GetUserTeamsOrderBy).is_optional().validate(order_by)
        Validator(GetUserTeamsSkipUsers).is_optional().validate(skip_users)

        serialized_request = (
            Serializer(
                f"{self.base_url}/legacyTeams/user/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("order_by", order_by)
            .add_query("skip_users", skip_users)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetUserTeamsOkResponse._unmap(response)
