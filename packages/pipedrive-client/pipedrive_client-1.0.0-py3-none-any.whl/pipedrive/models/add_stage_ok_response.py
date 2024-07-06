from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class AddStageOkResponseData(BaseModel):
    """Updated stage object

    :param id_: The ID of the stage, defaults to None
    :type id_: int, optional
    :param order_nr: Defines the order of the stage, defaults to None
    :type order_nr: int, optional
    :param name: The name of the stage, defaults to None
    :type name: str, optional
    :param active_flag: Whether the stage is active or deleted, defaults to None
    :type active_flag: bool, optional
    :param deal_probability: The success probability percentage of the deal. Used/shown when the deal weighted values are used., defaults to None
    :type deal_probability: int, optional
    :param pipeline_id: The ID of the pipeline to add the stage to, defaults to None
    :type pipeline_id: int, optional
    :param rotten_flag: Whether deals in this stage can become rotten, defaults to None
    :type rotten_flag: bool, optional
    :param rotten_days: The number of days the deals not updated in this stage would become rotten. Applies only if the `rotten_flag` is set., defaults to None
    :type rotten_days: int, optional
    :param add_time: The stage creation time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param update_time: The stage update time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        order_nr: int = None,
        name: str = None,
        active_flag: bool = None,
        deal_probability: int = None,
        pipeline_id: int = None,
        rotten_flag: bool = None,
        rotten_days: int = None,
        add_time: str = None,
        update_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if order_nr is not None:
            self.order_nr = order_nr
        if name is not None:
            self.name = name
        if active_flag is not None:
            self.active_flag = active_flag
        if deal_probability is not None:
            self.deal_probability = deal_probability
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if rotten_flag is not None:
            self.rotten_flag = rotten_flag
        if rotten_days is not None:
            self.rotten_days = rotten_days
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time


@JsonMap({})
class AddStageOkResponse(BaseModel):
    """AddStageOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: Updated stage object, defaults to None
    :type data: AddStageOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: AddStageOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, AddStageOkResponseData)
