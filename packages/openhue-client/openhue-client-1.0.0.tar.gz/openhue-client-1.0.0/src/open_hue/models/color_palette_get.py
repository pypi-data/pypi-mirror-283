from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .color import Color
from .dimming import Dimming


@JsonMap({})
class ColorPaletteGet(BaseModel):
    """ColorPaletteGet

    :param color: color, defaults to None
    :type color: Color, optional
    :param dimming: dimming, defaults to None
    :type dimming: Dimming, optional
    """

    def __init__(self, color: Color = None, dimming: Dimming = None):
        if color is not None:
            self.color = self._define_object(color, Color)
        if dimming is not None:
            self.dimming = self._define_object(dimming, Dimming)
