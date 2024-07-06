from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_note_fields_ok_response import GetNoteFieldsOkResponse


class NoteFieldsService(BaseService):

    @cast_models
    def get_note_fields(self) -> GetNoteFieldsOkResponse:
        """Returns data about all note fields.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: GetNoteFieldsOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/noteFields", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetNoteFieldsOkResponse._unmap(response)
