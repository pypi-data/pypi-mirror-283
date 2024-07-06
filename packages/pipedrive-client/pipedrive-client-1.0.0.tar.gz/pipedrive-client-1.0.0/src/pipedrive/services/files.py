from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_file_request import UpdateFileRequest
from ..models.update_file_ok_response import UpdateFileOkResponse
from ..models.link_file_to_item_request import LinkFileToItemRequest
from ..models.link_file_to_item_ok_response import LinkFileToItemOkResponse
from ..models.get_files_ok_response import GetFilesOkResponse
from ..models.get_file_ok_response import GetFileOkResponse
from ..models.delete_file_ok_response import DeleteFileOkResponse
from ..models.add_file_request import AddFileRequest
from ..models.add_file_ok_response import AddFileOkResponse
from ..models.add_file_and_link_it_request import AddFileAndLinkItRequest
from ..models.add_file_and_link_it_ok_response import AddFileAndLinkItOkResponse


class FilesService(BaseService):

    @cast_models
    def get_files(
        self, start: int = None, limit: int = None, sort: str = None
    ) -> GetFilesOkResponse:
        """Returns data about all files.

        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param sort: The field names and sorting mode separated by a comma (`field_name_1 ASC`, `field_name_2 DESC`). Only first-level field keys are supported (no nested keys). Supported fields: `id`, `user_id`, `deal_id`, `person_id`, `org_id`, `product_id`, `add_time`, `update_time`, `file_name`, `file_type`, `file_size`, `comment`., defaults to None
        :type sort: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get data about all files uploaded to Pipedrive
        :rtype: GetFilesOkResponse
        """

        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(sort)

        serialized_request = (
            Serializer(f"{self.base_url}/files", self.get_default_headers())
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("sort", sort)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetFilesOkResponse._unmap(response)

    @cast_models
    def add_file(self, request_body: dict = None) -> AddFileOkResponse:
        """Lets you upload a file and associate it with a deal, person, organization, activity, product or lead. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/adding-a-file" target="_blank" rel="noopener noreferrer">adding a file</a>.

        :param request_body: The request body., defaults to None
        :type request_body: dict, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add a file from computer or Google Drive and associate it with deal, person, organization, activity or product
        :rtype: AddFileOkResponse
        """

        Validator(dict).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/files", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body, "multipart/form-data")
        )

        response = self.send_request(serialized_request)

        return AddFileOkResponse._unmap(response)

    @cast_models
    def add_file_and_link_it(
        self, request_body: AddFileAndLinkItRequest = None
    ) -> AddFileAndLinkItOkResponse:
        """Creates a new empty file in the remote location (`googledrive`) that will be linked to the item you supply. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/adding-a-remote-file" target="_blank" rel="noopener noreferrer">adding a remote file</a>.

        :param request_body: The request body., defaults to None
        :type request_body: AddFileAndLinkItRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Creates a new empty file in the remote location (googledrive) that will be linked to the item you supply - deal, person or organization
        :rtype: AddFileAndLinkItOkResponse
        """

        Validator(AddFileAndLinkItRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/files/remote", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body, "application/x-www-form-urlencoded")
        )

        response = self.send_request(serialized_request)

        return AddFileAndLinkItOkResponse._unmap(response)

    @cast_models
    def link_file_to_item(
        self, request_body: LinkFileToItemRequest = None
    ) -> LinkFileToItemOkResponse:
        """Links an existing remote file (`googledrive`) to the item you supply. For more information, see the tutorial for <a href="https://pipedrive.readme.io/docs/adding-a-remote-file" target="_blank" rel="noopener noreferrer">adding a remote file</a>.

        :param request_body: The request body., defaults to None
        :type request_body: LinkFileToItemRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Links an existing remote file (googledrive) to the item you supply - deal, person, organization
        :rtype: LinkFileToItemOkResponse
        """

        Validator(LinkFileToItemRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/files/remoteLink", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body, "application/x-www-form-urlencoded")
        )

        response = self.send_request(serialized_request)

        return LinkFileToItemOkResponse._unmap(response)

    @cast_models
    def get_file(self, id_: int) -> GetFileOkResponse:
        """Returns data about a specific file.

        :param id_: The ID of the file
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get data about one specific file uploaded to Pipedrive
        :rtype: GetFileOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/files/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetFileOkResponse._unmap(response)

    @cast_models
    def update_file(
        self, id_: int, request_body: UpdateFileRequest = None
    ) -> UpdateFileOkResponse:
        """Updates the properties of a file.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateFileRequest, optional
        :param id_: The ID of the file
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Update file name and description
        :rtype: UpdateFileOkResponse
        """

        Validator(UpdateFileRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/files/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body, "application/x-www-form-urlencoded")
        )

        response = self.send_request(serialized_request)

        return UpdateFileOkResponse._unmap(response)

    @cast_models
    def delete_file(self, id_: int) -> DeleteFileOkResponse:
        """Marks a file as deleted. After 30 days, the file will be permanently deleted.

        :param id_: The ID of the file
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete a file from Pipedrive
        :rtype: DeleteFileOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/files/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteFileOkResponse._unmap(response)

    @cast_models
    def download_file(self, id_: int) -> bytes:
        """Initializes a file download.

        :param id_: The ID of the file
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: success
        :rtype: bytes
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/files/{{id}}/download", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return response
