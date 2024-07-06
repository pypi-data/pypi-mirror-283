from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_lead_label_request import UpdateLeadLabelRequest
from ..models.update_lead_label_ok_response import UpdateLeadLabelOkResponse
from ..models.get_lead_labels_ok_response import GetLeadLabelsOkResponse
from ..models.delete_lead_label_ok_response import DeleteLeadLabelOkResponse
from ..models.add_lead_label_request import AddLeadLabelRequest
from ..models.add_lead_label_ok_response import AddLeadLabelOkResponse


class LeadLabelsService(BaseService):

    @cast_models
    def get_lead_labels(self) -> GetLeadLabelsOkResponse:
        """Returns details of all lead labels. This endpoint does not support pagination and all labels are always returned.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response containing payload in the `data` field
        :rtype: GetLeadLabelsOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/leadLabels", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetLeadLabelsOkResponse._unmap(response)

    @cast_models
    def add_lead_label(
        self, request_body: AddLeadLabelRequest = None
    ) -> AddLeadLabelOkResponse:
        """Creates a lead label.

        :param request_body: The request body., defaults to None
        :type request_body: AddLeadLabelRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response containing payload in the `data` field
        :rtype: AddLeadLabelOkResponse
        """

        Validator(AddLeadLabelRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/leadLabels", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddLeadLabelOkResponse._unmap(response)

    @cast_models
    def update_lead_label(
        self, id_: str, request_body: UpdateLeadLabelRequest = None
    ) -> UpdateLeadLabelOkResponse:
        """Updates one or more properties of a lead label. Only properties included in the request will be updated.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateLeadLabelRequest, optional
        :param id_: The ID of the lead label
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response containing payload in the `data` field
        :rtype: UpdateLeadLabelOkResponse
        """

        Validator(UpdateLeadLabelRequest).is_optional().validate(request_body)
        Validator(str).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/leadLabels/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PATCH")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateLeadLabelOkResponse._unmap(response)

    @cast_models
    def delete_lead_label(self, id_: str) -> DeleteLeadLabelOkResponse:
        """Deletes a specific lead label.

        :param id_: The ID of the lead label
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response with id value only. Used in DELETE calls.
        :rtype: DeleteLeadLabelOkResponse
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/leadLabels/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteLeadLabelOkResponse._unmap(response)
