from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_note_request import UpdateNoteRequest
from ..models.update_note_ok_response import UpdateNoteOkResponse
from ..models.update_comment_for_note_request import UpdateCommentForNoteRequest
from ..models.update_comment_for_note_ok_response import UpdateCommentForNoteOkResponse
from ..models.get_notes_pinned_to_person_flag import GetNotesPinnedToPersonFlag
from ..models.get_notes_pinned_to_organization_flag import (
    GetNotesPinnedToOrganizationFlag,
)
from ..models.get_notes_pinned_to_lead_flag import GetNotesPinnedToLeadFlag
from ..models.get_notes_pinned_to_deal_flag import GetNotesPinnedToDealFlag
from ..models.get_notes_ok_response import GetNotesOkResponse
from ..models.get_note_ok_response import GetNoteOkResponse
from ..models.get_note_comments_ok_response import GetNoteCommentsOkResponse
from ..models.get_comment_ok_response import GetCommentOkResponse
from ..models.delete_note_ok_response import DeleteNoteOkResponse
from ..models.delete_comment_ok_response import DeleteCommentOkResponse
from ..models.add_note_request import AddNoteRequest
from ..models.add_note_ok_response import AddNoteOkResponse
from ..models.add_note_comment_request import AddNoteCommentRequest
from ..models.add_note_comment_ok_response import AddNoteCommentOkResponse


class NotesService(BaseService):

    @cast_models
    def get_notes(
        self,
        user_id: int = None,
        lead_id: str = None,
        deal_id: int = None,
        person_id: int = None,
        org_id: int = None,
        start: int = None,
        limit: int = None,
        sort: str = None,
        start_date: str = None,
        end_date: str = None,
        pinned_to_lead_flag: GetNotesPinnedToLeadFlag = None,
        pinned_to_deal_flag: GetNotesPinnedToDealFlag = None,
        pinned_to_organization_flag: GetNotesPinnedToOrganizationFlag = None,
        pinned_to_person_flag: GetNotesPinnedToPersonFlag = None,
    ) -> GetNotesOkResponse:
        """Returns all notes.

        :param user_id: The ID of the user whose notes to fetch. If omitted, notes by all users will be returned., defaults to None
        :type user_id: int, optional
        :param lead_id: The ID of the lead which notes to fetch. If omitted, notes about all leads will be returned., defaults to None
        :type lead_id: str, optional
        :param deal_id: The ID of the deal which notes to fetch. If omitted, notes about all deals will be returned., defaults to None
        :type deal_id: int, optional
        :param person_id: The ID of the person whose notes to fetch. If omitted, notes about all persons will be returned., defaults to None
        :type person_id: int, optional
        :param org_id: The ID of the organization which notes to fetch. If omitted, notes about all organizations will be returned., defaults to None
        :type org_id: int, optional
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param sort: The field names and sorting mode separated by a comma (`field_name_1 ASC`, `field_name_2 DESC`). Only first-level field keys are supported (no nested keys). Supported fields: `id`, `user_id`, `deal_id`, `person_id`, `org_id`, `content`, `add_time`, `update_time`., defaults to None
        :type sort: str, optional
        :param start_date: The date in format of YYYY-MM-DD from which notes to fetch, defaults to None
        :type start_date: str, optional
        :param end_date: The date in format of YYYY-MM-DD until which notes to fetch to, defaults to None
        :type end_date: str, optional
        :param pinned_to_lead_flag: If set, the results are filtered by note to lead pinning state, defaults to None
        :type pinned_to_lead_flag: GetNotesPinnedToLeadFlag, optional
        :param pinned_to_deal_flag: If set, the results are filtered by note to deal pinning state, defaults to None
        :type pinned_to_deal_flag: GetNotesPinnedToDealFlag, optional
        :param pinned_to_organization_flag: If set, the results are filtered by note to organization pinning state, defaults to None
        :type pinned_to_organization_flag: GetNotesPinnedToOrganizationFlag, optional
        :param pinned_to_person_flag: If set, the results are filtered by note to person pinning state, defaults to None
        :type pinned_to_person_flag: GetNotesPinnedToPersonFlag, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get all notes
        :rtype: GetNotesOkResponse
        """

        Validator(int).is_optional().validate(user_id)
        Validator(str).is_optional().validate(lead_id)
        Validator(int).is_optional().validate(deal_id)
        Validator(int).is_optional().validate(person_id)
        Validator(int).is_optional().validate(org_id)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(str).is_optional().validate(sort)
        Validator(str).is_optional().validate(start_date)
        Validator(str).is_optional().validate(end_date)
        Validator(GetNotesPinnedToLeadFlag).is_optional().validate(pinned_to_lead_flag)
        Validator(GetNotesPinnedToDealFlag).is_optional().validate(pinned_to_deal_flag)
        Validator(GetNotesPinnedToOrganizationFlag).is_optional().validate(
            pinned_to_organization_flag
        )
        Validator(GetNotesPinnedToPersonFlag).is_optional().validate(
            pinned_to_person_flag
        )

        serialized_request = (
            Serializer(f"{self.base_url}/notes", self.get_default_headers())
            .add_query("user_id", user_id)
            .add_query("lead_id", lead_id)
            .add_query("deal_id", deal_id)
            .add_query("person_id", person_id)
            .add_query("org_id", org_id)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("sort", sort)
            .add_query("start_date", start_date)
            .add_query("end_date", end_date)
            .add_query("pinned_to_lead_flag", pinned_to_lead_flag)
            .add_query("pinned_to_deal_flag", pinned_to_deal_flag)
            .add_query("pinned_to_organization_flag", pinned_to_organization_flag)
            .add_query("pinned_to_person_flag", pinned_to_person_flag)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetNotesOkResponse._unmap(response)

    @cast_models
    def add_note(self, request_body: AddNoteRequest = None) -> AddNoteOkResponse:
        """Adds a new note.

        :param request_body: The request body., defaults to None
        :type request_body: AddNoteRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add, update or get a note
        :rtype: AddNoteOkResponse
        """

        Validator(AddNoteRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/notes", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddNoteOkResponse._unmap(response)

    @cast_models
    def get_note(self, id_: int) -> GetNoteOkResponse:
        """Returns details about a specific note.

        :param id_: The ID of the note
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add, update or get a note
        :rtype: GetNoteOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/notes/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetNoteOkResponse._unmap(response)

    @cast_models
    def update_note(
        self, id_: int, request_body: UpdateNoteRequest = None
    ) -> UpdateNoteOkResponse:
        """Updates a note.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateNoteRequest, optional
        :param id_: The ID of the note
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add, update or get a note
        :rtype: UpdateNoteOkResponse
        """

        Validator(UpdateNoteRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/notes/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateNoteOkResponse._unmap(response)

    @cast_models
    def delete_note(self, id_: int) -> DeleteNoteOkResponse:
        """Deletes a specific note.

        :param id_: The ID of the note
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete a note
        :rtype: DeleteNoteOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/notes/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteNoteOkResponse._unmap(response)

    @cast_models
    def get_note_comments(
        self, id_: int, start: int = None, limit: int = None
    ) -> GetNoteCommentsOkResponse:
        """Returns all comments associated with a note.

        :param id_: The ID of the note
        :type id_: int
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get all comments
        :rtype: GetNoteCommentsOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/notes/{{id}}/comments", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetNoteCommentsOkResponse._unmap(response)

    @cast_models
    def add_note_comment(
        self, id_: int, request_body: AddNoteCommentRequest = None
    ) -> AddNoteCommentOkResponse:
        """Adds a new comment to a note.

        :param request_body: The request body., defaults to None
        :type request_body: AddNoteCommentRequest, optional
        :param id_: The ID of the note
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add, update or get a comment
        :rtype: AddNoteCommentOkResponse
        """

        Validator(AddNoteCommentRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/notes/{{id}}/comments", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddNoteCommentOkResponse._unmap(response)

    @cast_models
    def get_comment(self, id_: int, comment_id: str) -> GetCommentOkResponse:
        """Returns the details of a comment.

        :param id_: The ID of the note
        :type id_: int
        :param comment_id: The ID of the comment
        :type comment_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add, update or get a comment
        :rtype: GetCommentOkResponse
        """

        Validator(int).validate(id_)
        Validator(str).validate(comment_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/notes/{{id}}/comments/{{commentId}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("commentId", comment_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetCommentOkResponse._unmap(response)

    @cast_models
    def update_comment_for_note(
        self,
        id_: int,
        comment_id: str,
        request_body: UpdateCommentForNoteRequest = None,
    ) -> UpdateCommentForNoteOkResponse:
        """Updates a comment related to a note.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateCommentForNoteRequest, optional
        :param id_: The ID of the note
        :type id_: int
        :param comment_id: The ID of the comment
        :type comment_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add, update or get a comment
        :rtype: UpdateCommentForNoteOkResponse
        """

        Validator(UpdateCommentForNoteRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)
        Validator(str).validate(comment_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/notes/{{id}}/comments/{{commentId}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("commentId", comment_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateCommentForNoteOkResponse._unmap(response)

    @cast_models
    def delete_comment(self, id_: int, comment_id: str) -> DeleteCommentOkResponse:
        """Deletes a comment.

        :param id_: The ID of the note
        :type id_: int
        :param comment_id: The ID of the comment
        :type comment_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete a comment
        :rtype: DeleteCommentOkResponse
        """

        Validator(int).validate(id_)
        Validator(str).validate(comment_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/notes/{{id}}/comments/{{commentId}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("commentId", comment_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteCommentOkResponse._unmap(response)
