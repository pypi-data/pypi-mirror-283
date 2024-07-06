from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class UpdateDealFieldRequest(BaseModel):
    """UpdateDealFieldRequest

    :param name: The name of the field, defaults to None
    :type name: str, optional
    :param options: When `field_type` is either set or enum, possible options must be supplied as a JSON-encoded sequential array of objects. All active items must be supplied and already existing items must have their ID supplied. New items only require a label. Example: `[{"id":123,"label":"Existing Item"},{"label":"New Item"}]`, defaults to None
    :type options: List[dict], optional
    :param add_visible_flag: Whether the field is available in 'add new' modal or not (both in web and mobile app), defaults to None
    :type add_visible_flag: bool, optional
    """

    def __init__(
        self,
        name: str = None,
        options: List[dict] = None,
        add_visible_flag: bool = None,
    ):
        if name is not None:
            self.name = name
        if options is not None:
            self.options = options
        if add_visible_flag is not None:
            self.add_visible_flag = add_visible_flag
