from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GamutPosition(BaseModel):
    """CIE XY gamut position

    :param x: X position in color gamut, defaults to None
    :type x: float, optional
    :param y: y position in color gamut, defaults to None
    :type y: float, optional
    """

    def __init__(self, x: float = None, y: float = None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
