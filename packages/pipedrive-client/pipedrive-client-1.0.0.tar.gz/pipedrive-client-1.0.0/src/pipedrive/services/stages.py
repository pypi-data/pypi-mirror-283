from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_stage_request import UpdateStageRequest
from ..models.update_stage_ok_response import UpdateStageOkResponse
from ..models.get_stages_ok_response import GetStagesOkResponse
from ..models.get_stage_ok_response import GetStageOkResponse
from ..models.get_stage_everyone import GetStageEveryone
from ..models.get_stage_deals_ok_response import GetStageDealsOkResponse
from ..models.get_stage_deals_everyone import GetStageDealsEveryone
from ..models.delete_stages_ok_response import DeleteStagesOkResponse
from ..models.delete_stage_ok_response import DeleteStageOkResponse
from ..models.add_stage_request import AddStageRequest
from ..models.add_stage_ok_response import AddStageOkResponse


class StagesService(BaseService):

    @cast_models
    def get_stages(
        self, pipeline_id: int = None, start: int = None, limit: int = None
    ) -> GetStagesOkResponse:
        """Returns data about all stages.

        :param pipeline_id: The ID of the pipeline to fetch stages for. If omitted, stages for all pipelines will be fetched., defaults to None
        :type pipeline_id: int, optional
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get all stages
        :rtype: GetStagesOkResponse
        """

        Validator(int).is_optional().validate(pipeline_id)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(f"{self.base_url}/stages", self.get_default_headers())
            .add_query("pipeline_id", pipeline_id)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetStagesOkResponse._unmap(response)

    @cast_models
    def add_stage(self, request_body: AddStageRequest = None) -> AddStageOkResponse:
        """Adds a new stage, returns the ID upon success.

        :param request_body: The request body., defaults to None
        :type request_body: AddStageRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get all stages
        :rtype: AddStageOkResponse
        """

        Validator(AddStageRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/stages", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddStageOkResponse._unmap(response)

    @cast_models
    def delete_stages(self, ids: str) -> DeleteStagesOkResponse:
        """Marks multiple stages as deleted.

        :param ids: The comma-separated stage IDs to delete
        :type ids: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete multiple stages
        :rtype: DeleteStagesOkResponse
        """

        Validator(str).validate(ids)

        serialized_request = (
            Serializer(f"{self.base_url}/stages", self.get_default_headers())
            .add_query("ids", ids)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteStagesOkResponse._unmap(response)

    @cast_models
    def get_stage(
        self, id_: int, everyone: GetStageEveryone = None
    ) -> GetStageOkResponse:
        """Returns data about a specific stage.

        :param id_: The ID of the stage
        :type id_: int
        :param everyone: If `everyone=1` is provided, deals summary will return deals owned by every user, defaults to None
        :type everyone: GetStageEveryone, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get stage
        :rtype: GetStageOkResponse
        """

        Validator(int).validate(id_)
        Validator(GetStageEveryone).is_optional().validate(everyone)

        serialized_request = (
            Serializer(f"{self.base_url}/stages/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .add_query("everyone", everyone)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetStageOkResponse._unmap(response)

    @cast_models
    def update_stage(
        self, id_: int, request_body: UpdateStageRequest = None
    ) -> UpdateStageOkResponse:
        """Updates the properties of a stage.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateStageRequest, optional
        :param id_: The ID of the stage
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get all stages
        :rtype: UpdateStageOkResponse
        """

        Validator(UpdateStageRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/stages/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateStageOkResponse._unmap(response)

    @cast_models
    def delete_stage(self, id_: int) -> DeleteStageOkResponse:
        """Marks a stage as deleted.

        :param id_: The ID of the stage
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete stage
        :rtype: DeleteStageOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/stages/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteStageOkResponse._unmap(response)

    @cast_models
    def get_stage_deals(
        self,
        id_: int,
        filter_id: int = None,
        user_id: int = None,
        everyone: GetStageDealsEveryone = None,
        start: int = None,
        limit: int = None,
    ) -> GetStageDealsOkResponse:
        """Lists deals in a specific stage.

        :param id_: The ID of the stage
        :type id_: int
        :param filter_id: If supplied, only deals matching the given filter will be returned, defaults to None
        :type filter_id: int, optional
        :param user_id: If supplied, `filter_id` will not be considered and only deals owned by the given user will be returned. If omitted, deals owned by the authorized user will be returned., defaults to None
        :type user_id: int, optional
        :param everyone: If supplied, `filter_id` and `user_id` will not be considered – instead, deals owned by everyone will be returned, defaults to None
        :type everyone: GetStageDealsEveryone, optional
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get deals in a stage
        :rtype: GetStageDealsOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(filter_id)
        Validator(int).is_optional().validate(user_id)
        Validator(GetStageDealsEveryone).is_optional().validate(everyone)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)

        serialized_request = (
            Serializer(
                f"{self.base_url}/stages/{{id}}/deals", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("filter_id", filter_id)
            .add_query("user_id", user_id)
            .add_query("everyone", everyone)
            .add_query("start", start)
            .add_query("limit", limit)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetStageDealsOkResponse._unmap(response)
