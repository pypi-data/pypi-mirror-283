from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .color_palette_get import ColorPaletteGet
from .dimming import Dimming
from .color_temperature_palette_post import ColorTemperaturePalettePost
from .supported_effects import SupportedEffects


@JsonMap({})
class ScenePaletteEffects(BaseModel):
    """ScenePaletteEffects

    :param effect: effect, defaults to None
    :type effect: SupportedEffects, optional
    """

    def __init__(self, effect: SupportedEffects = None):
        if effect is not None:
            self.effect = self._enum_matching(effect, SupportedEffects.list(), "effect")


@JsonMap({})
class ScenePalette(BaseModel):
    """Group of colors that describe the palette of colors to be used when playing dynamics

    :param color: color, defaults to None
    :type color: List[ColorPaletteGet], optional
    :param dimming: dimming, defaults to None
    :type dimming: List[Dimming], optional
    :param color_temperature: color_temperature, defaults to None
    :type color_temperature: List[ColorTemperaturePalettePost], optional
    :param effects: effects, defaults to None
    :type effects: List[ScenePaletteEffects], optional
    """

    def __init__(
        self,
        color: List[ColorPaletteGet] = None,
        dimming: List[Dimming] = None,
        color_temperature: List[ColorTemperaturePalettePost] = None,
        effects: List[ScenePaletteEffects] = None,
    ):
        if color is not None:
            self.color = self._define_list(color, ColorPaletteGet)
        if dimming is not None:
            self.dimming = self._define_list(dimming, Dimming)
        if color_temperature is not None:
            self.color_temperature = self._define_list(
                color_temperature, ColorTemperaturePalettePost
            )
        if effects is not None:
            self.effects = self._define_list(effects, ScenePaletteEffects)
