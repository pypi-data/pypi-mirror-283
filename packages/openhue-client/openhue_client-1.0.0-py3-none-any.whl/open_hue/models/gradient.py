from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .color import Color
from .supported_gradient_mode import SupportedGradientMode


@JsonMap({})
class Gradient(BaseModel):
    """Basic feature containing gradient properties.

    :param points: Collection of gradients points. For control of the gradient points through a PUT a minimum of 2 points need to be provided., defaults to None
    :type points: List[Color], optional
    :param mode: Mode in which the points are currently being deployed. If not provided during PUT/POST it will be defaulted to interpolated_palette, defaults to None
    :type mode: SupportedGradientMode, optional
    """

    def __init__(self, points: List[Color] = None, mode: SupportedGradientMode = None):
        if points is not None:
            self.points = self._define_list(points, Color)
        if mode is not None:
            self.mode = self._enum_matching(mode, SupportedGradientMode.list(), "mode")
