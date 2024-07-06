from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class UpdatePipelineRequestDealProbability(Enum):
    """An enumeration representing different categories.

    :cvar _0: 0
    :vartype _0: str
    :cvar _1: 1
    :vartype _1: str
    """

    _0 = 0
    _1 = 1

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(
                lambda x: x.value,
                UpdatePipelineRequestDealProbability._member_map_.values(),
            )
        )


class UpdatePipelineRequestActive(Enum):
    """An enumeration representing different categories.

    :cvar _0: 0
    :vartype _0: str
    :cvar _1: 1
    :vartype _1: str
    """

    _0 = 0
    _1 = 1

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, UpdatePipelineRequestActive._member_map_.values())
        )


@JsonMap({})
class UpdatePipelineRequest(BaseModel):
    """UpdatePipelineRequest

    :param name: The name of the pipeline, defaults to None
    :type name: str, optional
    :param deal_probability: deal_probability, defaults to None
    :type deal_probability: UpdatePipelineRequestDealProbability, optional
    :param order_nr: Defines the order of pipelines. First order (`order_nr=0`) is the default pipeline., defaults to None
    :type order_nr: int, optional
    :param active: active, defaults to None
    :type active: UpdatePipelineRequestActive, optional
    """

    def __init__(
        self,
        name: str = None,
        deal_probability: UpdatePipelineRequestDealProbability = None,
        order_nr: int = None,
        active: UpdatePipelineRequestActive = None,
    ):
        if name is not None:
            self.name = name
        if deal_probability is not None:
            self.deal_probability = self._enum_matching(
                deal_probability,
                UpdatePipelineRequestDealProbability.list(),
                "deal_probability",
            )
        if order_nr is not None:
            self.order_nr = order_nr
        if active is not None:
            self.active = self._enum_matching(
                active, UpdatePipelineRequestActive.list(), "active"
            )
