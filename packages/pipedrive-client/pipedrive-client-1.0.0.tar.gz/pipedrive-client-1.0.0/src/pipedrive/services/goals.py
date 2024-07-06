from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_goal_request import UpdateGoalRequest
from ..models.update_goal_ok_response import UpdateGoalOkResponse
from ..models.type_name import TypeName
from ..models.get_goals_ok_response import GetGoalsOkResponse
from ..models.get_goal_result_ok_response import GetGoalResultOkResponse
from ..models.expected_outcome_tracking_metric import ExpectedOutcomeTrackingMetric
from ..models.delete_goal_ok_response import DeleteGoalOkResponse
from ..models.assignee_type import AssigneeType
from ..models.add_goal_request import AddGoalRequest
from ..models.add_goal_ok_response import AddGoalOkResponse


class GoalsService(BaseService):

    @cast_models
    def add_goal(self, request_body: AddGoalRequest = None) -> AddGoalOkResponse:
        """Adds a new goal. Along with adding a new goal, a report is created to track the progress of your goal.

        :param request_body: The request body., defaults to None
        :type request_body: AddGoalRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response containing payload in the `data.goal` object
        :rtype: AddGoalOkResponse
        """

        Validator(AddGoalRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/goals", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddGoalOkResponse._unmap(response)

    @cast_models
    def get_goals(
        self,
        type_name: TypeName = None,
        title: str = None,
        is_active: bool = None,
        assignee_id: int = None,
        assignee_type: AssigneeType = None,
        expected_outcome_target: float = None,
        expected_outcome_tracking_metric: ExpectedOutcomeTrackingMetric = None,
        expected_outcome_currency_id: int = None,
        type_params_pipeline_id: List[int] = None,
        type_params_stage_id: int = None,
        type_params_activity_type_id: List[int] = None,
        period_start: str = None,
        period_end: str = None,
    ) -> GetGoalsOkResponse:
        """Returns data about goals based on criteria. For searching, append `{searchField}={searchValue}` to the URL, where `searchField` can be any one of the lowest-level fields in dot-notation (e.g. `type.params.pipeline_id`; `title`). `searchValue` should be the value you are looking for on that field. Additionally, `is_active=<true|false>` can be provided to search for only active/inactive goals. When providing `period.start`, `period.end` must also be provided and vice versa.

        :param type_name: The type of the goal. If provided, everyone's goals will be returned., defaults to None
        :type type_name: TypeName, optional
        :param title: The title of the goal, defaults to None
        :type title: str, optional
        :param is_active: Whether the goal is active or not, defaults to None
        :type is_active: bool, optional
        :param assignee_id: The ID of the user who's goal to fetch. When omitted, only your goals will be returned., defaults to None
        :type assignee_id: int, optional
        :param assignee_type: The type of the goal's assignee. If provided, everyone's goals will be returned., defaults to None
        :type assignee_type: AssigneeType, optional
        :param expected_outcome_target: The numeric value of the outcome. If provided, everyone's goals will be returned., defaults to None
        :type expected_outcome_target: float, optional
        :param expected_outcome_tracking_metric: The tracking metric of the expected outcome of the goal. If provided, everyone's goals will be returned., defaults to None
        :type expected_outcome_tracking_metric: ExpectedOutcomeTrackingMetric, optional
        :param expected_outcome_currency_id: The numeric ID of the goal's currency. Only applicable to goals with `expected_outcome.tracking_metric` with value `sum`. If provided, everyone's goals will be returned., defaults to None
        :type expected_outcome_currency_id: int, optional
        :param type_params_pipeline_id: An array of pipeline IDs or `null` for all pipelines. If provided, everyone's goals will be returned., defaults to None
        :type type_params_pipeline_id: List[int], optional
        :param type_params_stage_id: The ID of the stage. Applicable to only `deals_progressed` type of goals. If provided, everyone's goals will be returned., defaults to None
        :type type_params_stage_id: int, optional
        :param type_params_activity_type_id: An array of IDs or `null` for all activity types. Only applicable for `activities_completed` and/or `activities_added` types of goals. If provided, everyone's goals will be returned., defaults to None
        :type type_params_activity_type_id: List[int], optional
        :param period_start: The start date of the period for which to find goals. Date in format of YYYY-MM-DD. When `period.start` is provided, `period.end` must be provided too., defaults to None
        :type period_start: str, optional
        :param period_end: The end date of the period for which to find goals. Date in format of YYYY-MM-DD., defaults to None
        :type period_end: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response containing payload in the `data.goal` object
        :rtype: GetGoalsOkResponse
        """

        Validator(TypeName).is_optional().validate(type_name)
        Validator(str).is_optional().validate(title)
        Validator(bool).is_optional().validate(is_active)
        Validator(int).is_optional().validate(assignee_id)
        Validator(AssigneeType).is_optional().validate(assignee_type)
        Validator(float).is_optional().validate(expected_outcome_target)
        Validator(ExpectedOutcomeTrackingMetric).is_optional().validate(
            expected_outcome_tracking_metric
        )
        Validator(int).is_optional().validate(expected_outcome_currency_id)
        Validator(int).is_array().is_optional().validate(type_params_pipeline_id)
        Validator(int).is_optional().validate(type_params_stage_id)
        Validator(int).is_array().is_optional().validate(type_params_activity_type_id)
        Validator(str).is_optional().validate(period_start)
        Validator(str).is_optional().validate(period_end)

        serialized_request = (
            Serializer(f"{self.base_url}/goals/find", self.get_default_headers())
            .add_query("type.name", type_name)
            .add_query("title", title)
            .add_query("is_active", is_active)
            .add_query("assignee.id", assignee_id)
            .add_query("assignee.type", assignee_type)
            .add_query("expected_outcome.target", expected_outcome_target)
            .add_query(
                "expected_outcome.tracking_metric", expected_outcome_tracking_metric
            )
            .add_query("expected_outcome.currency_id", expected_outcome_currency_id)
            .add_query("type.params.pipeline_id", type_params_pipeline_id)
            .add_query("type.params.stage_id", type_params_stage_id)
            .add_query("type.params.activity_type_id", type_params_activity_type_id)
            .add_query("period.start", period_start)
            .add_query("period.end", period_end)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetGoalsOkResponse._unmap(response)

    @cast_models
    def update_goal(
        self, id_: str, request_body: UpdateGoalRequest = None
    ) -> UpdateGoalOkResponse:
        """Updates an existing goal.

        :param request_body: The request body., defaults to None
        :type request_body: UpdateGoalRequest, optional
        :param id_: The ID of the goal
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response containing payload in the `data.goal` object
        :rtype: UpdateGoalOkResponse
        """

        Validator(UpdateGoalRequest).is_optional().validate(request_body)
        Validator(str).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/goals/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateGoalOkResponse._unmap(response)

    @cast_models
    def delete_goal(self, id_: str) -> DeleteGoalOkResponse:
        """Marks a goal as deleted.

        :param id_: The ID of the goal
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response with id 'success' field only
        :rtype: DeleteGoalOkResponse
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(f"{self.base_url}/goals/{{id}}", self.get_default_headers())
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteGoalOkResponse._unmap(response)

    @cast_models
    def get_goal_result(
        self, id_: str, period_start: str, period_end: str
    ) -> GetGoalResultOkResponse:
        """Gets the progress of a goal for the specified period.

        :param id_: The ID of the goal that the results are looked for
        :type id_: str
        :param period_start: The start date of the period for which to find the goal's progress. Format: YYYY-MM-DD. This date must be the same or after the goal duration start date.
        :type period_start: str
        :param period_end: The end date of the period for which to find the goal's progress. Format: YYYY-MM-DD. This date must be the same or before the goal duration end date.
        :type period_end: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful response containing payload in the `data.goal` object
        :rtype: GetGoalResultOkResponse
        """

        Validator(str).validate(id_)
        Validator(str).validate(period_start)
        Validator(str).validate(period_end)

        serialized_request = (
            Serializer(
                f"{self.base_url}/goals/{{id}}/results", self.get_default_headers()
            )
            .add_path("id", id_)
            .add_query("period.start", period_start)
            .add_query("period.end", period_end)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetGoalResultOkResponse._unmap(response)
