from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class TypeParams1(BaseModel):
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
class GoalType1(BaseModel):
    """The type of the goal

    :param name: The name of the goal type, defaults to None
    :type name: str, optional
    :param params: The parameters that accompany the goal type, defaults to None
    :type params: TypeParams1, optional
    """

    def __init__(self, name: str = None, params: TypeParams1 = None):
        if name is not None:
            self.name = name
        if params is not None:
            self.params = self._define_object(params, TypeParams1)


@JsonMap({"id_": "id", "type_": "type"})
class GoalAssignee1(BaseModel):
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
class GoalDuration1(BaseModel):
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
class GoalExpectedOutcome1(BaseModel):
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
class DataGoal1(BaseModel):
    """DataGoal1

    :param id_: The ID of the goal, defaults to None
    :type id_: str, optional
    :param owner_id: The ID of the creator of the goal, defaults to None
    :type owner_id: int, optional
    :param title: The title of the goal, defaults to None
    :type title: str, optional
    :param type_: The type of the goal, defaults to None
    :type type_: GoalType1, optional
    :param assignee: Who the goal is assigned to, defaults to None
    :type assignee: GoalAssignee1, optional
    :param interval: The interval of the goal, defaults to None
    :type interval: str, optional
    :param duration: The duration of the goal, defaults to None
    :type duration: GoalDuration1, optional
    :param expected_outcome: The expected outcome of the goal, defaults to None
    :type expected_outcome: GoalExpectedOutcome1, optional
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
        type_: GoalType1 = None,
        assignee: GoalAssignee1 = None,
        interval: str = None,
        duration: GoalDuration1 = None,
        expected_outcome: GoalExpectedOutcome1 = None,
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
            self.type_ = self._define_object(type_, GoalType1)
        if assignee is not None:
            self.assignee = self._define_object(assignee, GoalAssignee1)
        if interval is not None:
            self.interval = interval
        if duration is not None:
            self.duration = self._define_object(duration, GoalDuration1)
        if expected_outcome is not None:
            self.expected_outcome = self._define_object(
                expected_outcome, GoalExpectedOutcome1
            )
        if is_active is not None:
            self.is_active = is_active
        if report_ids is not None:
            self.report_ids = report_ids


@JsonMap({})
class AddGoalOkResponseData(BaseModel):
    """AddGoalOkResponseData

    :param goal: goal, defaults to None
    :type goal: DataGoal1, optional
    """

    def __init__(self, goal: DataGoal1 = None):
        if goal is not None:
            self.goal = self._define_object(goal, DataGoal1)


@JsonMap({})
class AddGoalOkResponse(BaseModel):
    """AddGoalOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: AddGoalOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: AddGoalOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, AddGoalOkResponseData)
