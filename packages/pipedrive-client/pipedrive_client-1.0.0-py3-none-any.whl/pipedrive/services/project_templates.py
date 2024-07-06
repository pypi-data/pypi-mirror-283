from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_projects_phase_ok_response import GetProjectsPhaseOkResponse
from ..models.get_projects_board_ok_response import GetProjectsBoardOkResponse
from ..models.get_project_templates_ok_response import GetProjectTemplatesOkResponse
from ..models.get_project_template_ok_response import GetProjectTemplateOkResponse


class ProjectTemplatesService(BaseService):

    @cast_models
    def get_projects_board(self, id_: int) -> GetProjectsBoardOkResponse:
        """Returns the details of a specific project board.

        :param id_: The ID of the project board
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get a project board.
        :rtype: GetProjectsBoardOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/projects/boards/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProjectsBoardOkResponse._unmap(response)

    @cast_models
    def get_projects_phase(self, id_: int) -> GetProjectsPhaseOkResponse:
        """Returns the details of a specific project phase.

        :param id_: The ID of the project phase
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get a project phase.
        :rtype: GetProjectsPhaseOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/projects/phases/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProjectsPhaseOkResponse._unmap(response)

    @cast_models
    def get_project_templates(
        self, cursor: str = None, limit: int = None
    ) -> GetProjectTemplatesOkResponse:
        """Returns all not deleted project templates. This is a cursor-paginated endpoint. For more information, please refer to our documentation on <a href="https://pipedrive.readme.io/docs/core-api-concepts-pagination" target="_blank" rel="noopener noreferrer">pagination</a>.

        :param cursor: For pagination, the marker (an opaque string value) representing the first item on the next page, defaults to None
        :type cursor: str, optional
        :param limit: For pagination, the limit of entries to be returned. If not provided, up to 500 items will be returned., defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: A list of project template.
        :rtype: GetProjectTemplatesOkResponse
        """

        Validator(str).is_optional().validate(cursor)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/projectTemplates", self.get_default_headers())
            .add_query("cursor", cursor)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProjectTemplatesOkResponse._unmap(response)

    @cast_models
    def get_project_template(self, id_: int) -> GetProjectTemplateOkResponse:
        """Returns the details of a specific project template.

        :param id_: The ID of the project template
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get a project template.
        :rtype: GetProjectTemplateOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/projectTemplates/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetProjectTemplateOkResponse._unmap(response)
