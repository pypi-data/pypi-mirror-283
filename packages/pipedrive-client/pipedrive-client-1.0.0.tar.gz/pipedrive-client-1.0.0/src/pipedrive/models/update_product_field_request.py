from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class UpdateProductFieldRequest(BaseModel):
    """UpdateProductFieldRequest

    :param name: The name of the field, defaults to None
    :type name: str, optional
    :param options: When `field_type` is either set or enum, possible options on update must be supplied as an array of objects each containing id and label, for example: [{"id":1, "label":"red"},{"id":2, "label":"blue"},{"id":3, "label":"lilac"}], defaults to None
    :type options: List[dict], optional
    """

    def __init__(self, name: str = None, options: List[dict] = None):
        if name is not None:
            self.name = name
        if options is not None:
            self.options = options
