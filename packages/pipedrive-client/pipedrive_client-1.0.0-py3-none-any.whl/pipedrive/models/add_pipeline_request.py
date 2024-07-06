from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class AddPipelineRequestDealProbability(Enum):
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
                AddPipelineRequestDealProbability._member_map_.values(),
            )
        )


class AddPipelineRequestActive(Enum):
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
            map(lambda x: x.value, AddPipelineRequestActive._member_map_.values())
        )


@JsonMap({})
class AddPipelineRequest(BaseModel):
    """AddPipelineRequest

    :param name: The name of the pipeline
    :type name: str
    :param deal_probability: deal_probability, defaults to None
    :type deal_probability: AddPipelineRequestDealProbability, optional
    :param order_nr: Defines the order of pipelines. First order (`order_nr=0`) is the default pipeline., defaults to None
    :type order_nr: int, optional
    :param active: active, defaults to None
    :type active: AddPipelineRequestActive, optional
    """

    def __init__(
        self,
        name: str,
        deal_probability: AddPipelineRequestDealProbability = None,
        order_nr: int = None,
        active: AddPipelineRequestActive = None,
    ):
        self.name = name
        if deal_probability is not None:
            self.deal_probability = self._enum_matching(
                deal_probability,
                AddPipelineRequestDealProbability.list(),
                "deal_probability",
            )
        if order_nr is not None:
            self.order_nr = order_nr
        if active is not None:
            self.active = self._enum_matching(
                active, AddPipelineRequestActive.list(), "active"
            )
