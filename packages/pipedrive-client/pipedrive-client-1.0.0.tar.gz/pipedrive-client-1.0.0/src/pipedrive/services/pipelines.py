from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_pipeline_request import UpdatePipelineRequest
from ..models.update_pipeline_ok_response import UpdatePipelineOkResponse
from ..models.get_summary import GetSummary
from ..models.get_pipelines_ok_response import GetPipelinesOkResponse
from ..models.get_pipeline_ok_response import GetPipelineOkResponse
from ..models.get_pipeline_movement_statistics_ok_response import (
    GetPipelineMovementStatisticsOkResponse,
)
from ..models.get_pipeline_deals_ok_response import GetPipelineDealsOkResponse
from ..models.get_pipeline_deals_everyone import GetPipelineDealsEveryone
from ..models.get_pipeline_conversion_statistics_ok_response import (
    GetPipelineConversionStatisticsOkResponse,
)
from ..models.delete_pipeline_ok_response import DeletePipelineOkResponse
from ..models.add_pipeline_request import AddPipelineRequest
from ..models.add_pipeline_ok_response import AddPipelineOkResponse


class PipelinesService(BaseService):

    @cast_models
    def get_pipelines(self) -> GetPipelinesOkResponse:
        """Returns data about all pipelines.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get all pipelines
        :rtype: GetPipelinesOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/pipelines", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPipelinesOkResponse._unmap(response)

    @cast_models
    def add_pipeline(
        self, request_body: AddPipelineRequest = None
    ) -> AddPipelineOkResponse:
        """Adds a new pipeline.

        :param request_body: The request body., defaults to None
        :type request_body: AddPipelineRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Add pipeline
        :rtype: AddPipelineOkResponse
        """

        Validator(AddPipelineRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/pipelines", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddPipelineOkResponse._unmap(response)

    @cast_models
    def get_pipeline(
        self, id_: int, totals_convert_currency: str = None
    ) -> GetPipelineOkResponse:
        """Returns data about a specific pipeline. Also returns the summary of the deals in this pipeline across its stages.

        :param id_: The ID of the pipeline
        :type id_: int
        :param totals_convert_currency: The 3-letter currency code of any of the supported currencies. When supplied, `per_stages_converted` is returned in `deals_summary` which contains the currency-converted total amounts in the given currency per each stage. You may also set this parameter to `default_currency` in which case users default currency is used., defaults to None
        :type totals_convert_currency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get pipeline
        :rtype: GetPipelineOkResponse
        """

        Validator(int).validate(id_)
        Validator(str).is_optional().validate(totals_convert_currency)

        serialized_request = (
            Serializer(f"{self.base_url}/pipelines/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .add_query("totals_convert_currency", totals_convert_currency)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPipelineOkResponse._unmap(response)

    @cast_models
    def update_pipeline(
        self, id_: int, request_body: UpdatePipelineRequest = None
    ) -> UpdatePipelineOkResponse:
        """Updates the properties of a pipeline.

        :param request_body: The request body., defaults to None
        :type request_body: UpdatePipelineRequest, optional
        :param id_: The ID of the pipeline
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Edit pipeline
        :rtype: UpdatePipelineOkResponse
        """

        Validator(UpdatePipelineRequest).is_optional().validate(request_body)
        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/pipelines/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdatePipelineOkResponse._unmap(response)

    @cast_models
    def delete_pipeline(self, id_: int) -> DeletePipelineOkResponse:
        """Marks a pipeline as deleted.

        :param id_: The ID of the pipeline
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Delete pipeline
        :rtype: DeletePipelineOkResponse
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/pipelines/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeletePipelineOkResponse._unmap(response)

    @cast_models
    def get_pipeline_conversion_statistics(
        self, id_: int, start_date: str, end_date: str, user_id: int = None
    ) -> GetPipelineConversionStatisticsOkResponse:
        """Returns all stage-to-stage conversion and pipeline-to-close rates for the given time period.

        :param id_: The ID of the pipeline
        :type id_: int
        :param start_date: The start of the period. Date in format of YYYY-MM-DD.
        :type start_date: str
        :param end_date: The end of the period. Date in format of YYYY-MM-DD.
        :type end_date: str
        :param user_id: The ID of the user who's pipeline metrics statistics to fetch. If omitted, the authorized user will be used., defaults to None
        :type user_id: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get pipeline deals conversion rates
        :rtype: GetPipelineConversionStatisticsOkResponse
        """

        Validator(int).validate(id_)
        Validator(str).validate(start_date)
        Validator(str).validate(end_date)
        Validator(int).is_optional().validate(user_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/pipelines/{{id}}/conversion_statistics",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("start_date", start_date)
            .add_query("end_date", end_date)
            .add_query("user_id", user_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPipelineConversionStatisticsOkResponse._unmap(response)

    @cast_models
    def get_pipeline_deals(
        self,
        id_: int,
        filter_id: int = None,
        user_id: int = None,
        everyone: GetPipelineDealsEveryone = None,
        stage_id: int = None,
        start: int = None,
        limit: int = None,
        get_summary: GetSummary = None,
        totals_convert_currency: str = None,
    ) -> GetPipelineDealsOkResponse:
        """Lists deals in a specific pipeline across all its stages.

        :param id_: The ID of the pipeline
        :type id_: int
        :param filter_id: If supplied, only deals matching the given filter will be returned, defaults to None
        :type filter_id: int, optional
        :param user_id: If supplied, `filter_id` will not be considered and only deals owned by the given user will be returned. If omitted, deals owned by the authorized user will be returned., defaults to None
        :type user_id: int, optional
        :param everyone: If supplied, `filter_id` and `user_id` will not be considered – instead, deals owned by everyone will be returned, defaults to None
        :type everyone: GetPipelineDealsEveryone, optional
        :param stage_id: If supplied, only deals within the given stage will be returned, defaults to None
        :type stage_id: int, optional
        :param start: Pagination start, defaults to None
        :type start: int, optional
        :param limit: Items shown per page, defaults to None
        :type limit: int, optional
        :param get_summary: Whether to include a summary of the pipeline in the `additional_data` or not, defaults to None
        :type get_summary: GetSummary, optional
        :param totals_convert_currency: The 3-letter currency code of any of the supported currencies. When supplied, `per_stages_converted` is returned inside `deals_summary` inside `additional_data` which contains the currency-converted total amounts in the given currency per each stage. You may also set this parameter to `default_currency` in which case users default currency is used. Only works when `get_summary` parameter flag is enabled., defaults to None
        :type totals_convert_currency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get deals in a stage
        :rtype: GetPipelineDealsOkResponse
        """

        Validator(int).validate(id_)
        Validator(int).is_optional().validate(filter_id)
        Validator(int).is_optional().validate(user_id)
        Validator(GetPipelineDealsEveryone).is_optional().validate(everyone)
        Validator(int).is_optional().validate(stage_id)
        Validator(int).is_optional().validate(start)
        Validator(int).is_optional().validate(limit)
        Validator(GetSummary).is_optional().validate(get_summary)
        Validator(str).is_optional().validate(totals_convert_currency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/pipelines/{{id}}/deals", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("filter_id", filter_id)
            .add_query("user_id", user_id)
            .add_query("everyone", everyone)
            .add_query("stage_id", stage_id)
            .add_query("start", start)
            .add_query("limit", limit)
            .add_query("get_summary", get_summary)
            .add_query("totals_convert_currency", totals_convert_currency)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPipelineDealsOkResponse._unmap(response)

    @cast_models
    def get_pipeline_movement_statistics(
        self, id_: int, start_date: str, end_date: str, user_id: int = None
    ) -> GetPipelineMovementStatisticsOkResponse:
        """Returns statistics for deals movements for the given time period.

        :param id_: The ID of the pipeline
        :type id_: int
        :param start_date: The start of the period. Date in format of YYYY-MM-DD.
        :type start_date: str
        :param end_date: The end of the period. Date in format of YYYY-MM-DD.
        :type end_date: str
        :param user_id: The ID of the user who's pipeline statistics to fetch. If omitted, the authorized user will be used., defaults to None
        :type user_id: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Get pipeline deals conversion rates
        :rtype: GetPipelineMovementStatisticsOkResponse
        """

        Validator(int).validate(id_)
        Validator(str).validate(start_date)
        Validator(str).validate(end_date)
        Validator(int).is_optional().validate(user_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/pipelines/{{id}}/movement_statistics",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("start_date", start_date)
            .add_query("end_date", end_date)
            .add_query("user_id", user_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetPipelineMovementStatisticsOkResponse._unmap(response)
