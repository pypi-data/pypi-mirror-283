from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_organization_relationship_request import (
    UpdateOrganizationRelationshipRequest,
)
from ..models.update_organization_relationship_ok_response import (
    UpdateOrganizationRelationshipOkResponse,
)
from ..models.get_organization_relationships_ok_response import (
    GetOrganizationRelationshipsOkResponse,
)
from ..models.get_organization_relationship_ok_response import (
    GetOrganizationRelationshipOkResponse,
)
from ..models.delete_organization_relationship_ok_response import (
    DeleteOrganizationRelationshipOkResponse,
)
from ..models.add_organization_relationship_request import (
    AddOrganizationRelationshipRequest,
)
from ..models.add_organization_relationship_ok_response import (
    AddOrganizationRelationshipOkResponse,
)


class OrganizationRelationshipsService(BaseService):

    @cast_models
    def get_organization_relationships(
        self, org_id: int
    ) -> GetOrganizationRelationshipsOkResponse:
        """Gets all of the relationships for a supplied organization ID.

        :param org_id: The ID of the organization to get relationships for
        :type org_id: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationRelationshipsOkResponse
        """

        Validator(int).validate(org_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizationRelationships", self.get_default_headers()
            )
            .add_query("org_id", org_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationRelationshipsOkResponse._unmap(response)

    @cast_models
    def add_organization_relationship(
        self, request_body: AddOrganizationRelationshipRequest = None
    ) -> AddOrganizationRelationshipOkResponse:
        """Creates and returns an organization relationship.

        :param request_body: The request body., defaults to None
        :type request_body: AddOrganizationRelationshipRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: AddOrganizationRelationshipOkResponse
        """

        Validator(AddOrganizationRelationshipRequest).is_optional().validate(
            request_body
        )

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizationRelationships", self.get_default_headers()
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddOrganizationRelationshipOkResponse._unmap(response)

    @cast_models
    def get_organization_relationship(
        self, id_: int, org_id: int = None
    ) -> GetOrganizationRelationshipOkResponse:
        """Finds and returns an organization relationship from its ID.

        :param id_: The ID of the organization relationship
        :type id_: int
        :param org_id: The ID of the base organization for the returned calculated values, defaults to None
        :type org_id: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetOrganizationRelationshipOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(org_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizationRelationships/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("org_id", org_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetOrganizationRelationshipOkResponse._unmap(response)

    @cast_models
    def update_organization_relationship(
        self, id_: int, request_body: UpdateOrganizationRelationshipRequest = None
    ) -> UpdateOrganizationRelationshipOkResponse:
        """Updates and returns an organization relationship.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateOrganizationRelationshipRequest, optional
        :param id_: The ID of the organization relationship
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateOrganizationRelationshipOkResponse
        """

        Validator(UpdateOrganizationRelationshipRequest).is_optional().validate(
            request_body
        )
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizationRelationships/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateOrganizationRelationshipOkResponse._unmap(response)

    @cast_models
    def delete_organization_relationship(
        self, id_: int
    ) -> DeleteOrganizationRelationshipOkResponse:
        """Deletes an organization relationship and returns the deleted ID.

        :param id_: The ID of the organization relationship
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteOrganizationRelationshipOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/organizationRelationships/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteOrganizationRelationshipOkResponse._unmap(response)
