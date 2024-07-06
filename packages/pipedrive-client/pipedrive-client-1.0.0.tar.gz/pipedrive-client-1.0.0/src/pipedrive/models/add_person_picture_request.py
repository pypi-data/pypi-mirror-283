from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AddPersonPictureRequest(BaseModel):
    """AddPersonPictureRequest

    :param file: One image supplied in the multipart/form-data encoding
    :type file: any
    :param crop_x: X coordinate to where start cropping form (in pixels), defaults to None
    :type crop_x: int, optional
    :param crop_y: Y coordinate to where start cropping form (in pixels), defaults to None
    :type crop_y: int, optional
    :param crop_width: The width of the cropping area (in pixels), defaults to None
    :type crop_width: int, optional
    :param crop_height: The height of the cropping area (in pixels), defaults to None
    :type crop_height: int, optional
    """

    def __init__(
        self,
        file: any,
        crop_x: int = None,
        crop_y: int = None,
        crop_width: int = None,
        crop_height: int = None,
    ):
        self.file = file
        if crop_x is not None:
            self.crop_x = crop_x
        if crop_y is not None:
            self.crop_y = crop_y
        if crop_width is not None:
            self.crop_width = crop_width
        if crop_height is not None:
            self.crop_height = crop_height
