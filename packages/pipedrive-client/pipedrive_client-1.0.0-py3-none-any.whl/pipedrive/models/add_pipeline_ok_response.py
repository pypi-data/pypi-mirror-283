from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class AddPipelineOkResponseData(BaseModel):
    """The pipeline object

    :param id_: The ID of the pipeline, defaults to None
    :type id_: int, optional
    :param name: The name of the pipeline, defaults to None
    :type name: str, optional
    :param url_title: The pipeline title displayed in the URL, defaults to None
    :type url_title: str, optional
    :param order_nr: Defines the order of pipelines. First order (`order_nr=0`) is the default pipeline., defaults to None
    :type order_nr: int, optional
    :param active: Whether this pipeline will be made inactive (hidden) or active, defaults to None
    :type active: bool, optional
    :param deal_probability: Whether deal probability is disabled or enabled for this pipeline, defaults to None
    :type deal_probability: bool, optional
    :param add_time: The pipeline creation time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param update_time: The pipeline update time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        url_title: str = None,
        order_nr: int = None,
        active: bool = None,
        deal_probability: bool = None,
        add_time: str = None,
        update_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if url_title is not None:
            self.url_title = url_title
        if order_nr is not None:
            self.order_nr = order_nr
        if active is not None:
            self.active = active
        if deal_probability is not None:
            self.deal_probability = deal_probability
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time


@JsonMap({})
class AddPipelineOkResponse(BaseModel):
    """AddPipelineOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The pipeline object, defaults to None
    :type data: AddPipelineOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: AddPipelineOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, AddPipelineOkResponseData)
