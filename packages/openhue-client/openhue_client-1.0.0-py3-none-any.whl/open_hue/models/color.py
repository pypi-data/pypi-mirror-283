from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .gamut_position import GamutPosition


@JsonMap({})
class Color(BaseModel):
    """Color

    :param xy: CIE XY gamut position, defaults to None
    :type xy: GamutPosition, optional
    """

    def __init__(self, xy: GamutPosition = None):
        if xy is not None:
            self.xy = self._define_object(xy, GamutPosition)
