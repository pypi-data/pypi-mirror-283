from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class TypeParams2(BaseModel):
    """The parameters that accompany the goal type

    :param pipeline_id: The IDs of pipelines of the goal, defaults to None
    :type pipeline_id: List[int], optional
    :param activity_type_id: The IDs of activity types of the goal, defaults to None
    :type activity_type_id: List[int], optional
    """

    def __init__(
        self, pipeline_id: List[int] = None, activity_type_id: List[int] = None
    ):
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if activity_type_id is not None:
            self.activity_type_id = activity_type_id


@JsonMap({})
class GoalsType(BaseModel):
    """The type of the goal

    :param name: The name of the goal type, defaults to None
    :type name: str, optional
    :param params: The parameters that accompany the goal type, defaults to None
    :type params: TypeParams2, optional
    """

    def __init__(self, name: str = None, params: TypeParams2 = None):
        if name is not None:
            self.name = name
        if params is not None:
            self.params = self._define_object(params, TypeParams2)


@JsonMap({"id_": "id", "type_": "type"})
class GoalsAssignee(BaseModel):
    """Who the goal is assigned to

    :param id_: The ID of the goal assignee, defaults to None
    :type id_: int, optional
    :param type_: The type of the assignee, defaults to None
    :type type_: str, optional
    """

    def __init__(self, id_: int = None, type_: str = None):
        if id_ is not None:
            self.id_ = id_
        if type_ is not None:
            self.type_ = type_


@JsonMap({})
class GoalsDuration(BaseModel):
    """The duration of the goal

    :param start: The start date of the goal, defaults to None
    :type start: str, optional
    :param end: The end date of the goal, defaults to None
    :type end: str, optional
    """

    def __init__(self, start: str = None, end: str = None):
        if start is not None:
            self.start = start
        if end is not None:
            self.end = end


@JsonMap({})
class GoalsExpectedOutcome(BaseModel):
    """The expected outcome of the goal

    :param target: The numeric target of the goal, defaults to None
    :type target: int, optional
    :param tracking_metric: The tracking metric of the goal, defaults to None
    :type tracking_metric: str, optional
    """

    def __init__(self, target: int = None, tracking_metric: str = None):
        if target is not None:
            self.target = target
        if tracking_metric is not None:
            self.tracking_metric = tracking_metric


@JsonMap({"id_": "id", "type_": "type"})
class Goals(BaseModel):
    """Goals

    :param id_: The ID of the goal, defaults to None
    :type id_: str, optional
    :param owner_id: The ID of the creator of the goal, defaults to None
    :type owner_id: int, optional
    :param title: The title of the goal, defaults to None
    :type title: str, optional
    :param type_: The type of the goal, defaults to None
    :type type_: GoalsType, optional
    :param assignee: Who the goal is assigned to, defaults to None
    :type assignee: GoalsAssignee, optional
    :param interval: The interval of the goal, defaults to None
    :type interval: str, optional
    :param duration: The duration of the goal, defaults to None
    :type duration: GoalsDuration, optional
    :param expected_outcome: The expected outcome of the goal, defaults to None
    :type expected_outcome: GoalsExpectedOutcome, optional
    :param is_active: Whether the goal is currently active or not, defaults to None
    :type is_active: bool, optional
    :param report_ids: The IDs of the reports that belong to the goal, defaults to None
    :type report_ids: List[str], optional
    """

    def __init__(
        self,
        id_: str = None,
        owner_id: int = None,
        title: str = None,
        type_: GoalsType = None,
        assignee: GoalsAssignee = None,
        interval: str = None,
        duration: GoalsDuration = None,
        expected_outcome: GoalsExpectedOutcome = None,
        is_active: bool = None,
        report_ids: List[str] = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if owner_id is not None:
            self.owner_id = owner_id
        if title is not None:
            self.title = title
        if type_ is not None:
            self.type_ = self._define_object(type_, GoalsType)
        if assignee is not None:
            self.assignee = self._define_object(assignee, GoalsAssignee)
        if interval is not None:
            self.interval = interval
        if duration is not None:
            self.duration = self._define_object(duration, GoalsDuration)
        if expected_outcome is not None:
            self.expected_outcome = self._define_object(
                expected_outcome, GoalsExpectedOutcome
            )
        if is_active is not None:
            self.is_active = is_active
        if report_ids is not None:
            self.report_ids = report_ids


@JsonMap({})
class GetGoalsOkResponseData(BaseModel):
    """GetGoalsOkResponseData

    :param goals: goals, defaults to None
    :type goals: List[Goals], optional
    """

    def __init__(self, goals: List[Goals] = None):
        if goals is not None:
            self.goals = self._define_list(goals, Goals)


@JsonMap({})
class GetGoalsOkResponse(BaseModel):
    """GetGoalsOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: GetGoalsOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: GetGoalsOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetGoalsOkResponseData)
