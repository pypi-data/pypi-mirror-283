from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .supported_effects import SupportedEffects


@JsonMap({})
class Effects(BaseModel):
    """Basic feature containing effect properties.

    :param effect: effect, defaults to None
    :type effect: SupportedEffects, optional
    """

    def __init__(self, effect: SupportedEffects = None):
        if effect is not None:
            self.effect = self._enum_matching(effect, SupportedEffects.list(), "effect")
