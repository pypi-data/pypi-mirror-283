from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .dimming import Dimming


@JsonMap({})
class ColorTemperaturePalettePostColorTemperature(BaseModel):
    """ColorTemperaturePalettePostColorTemperature

    :param mirek: color temperature in mirek or null when the light color is not in the ct spectrum, defaults to None
    :type mirek: int, optional
    """

    def __init__(self, mirek: int = None):
        if mirek is not None:
            self.mirek = mirek


@JsonMap({})
class ColorTemperaturePalettePost(BaseModel):
    """ColorTemperaturePalettePost

    :param color_temperature: color_temperature, defaults to None
    :type color_temperature: ColorTemperaturePalettePostColorTemperature, optional
    :param dimming: dimming, defaults to None
    :type dimming: Dimming, optional
    """

    def __init__(
        self,
        color_temperature: ColorTemperaturePalettePostColorTemperature = None,
        dimming: Dimming = None,
    ):
        if color_temperature is not None:
            self.color_temperature = self._define_object(
                color_temperature, ColorTemperaturePalettePostColorTemperature
            )
        if dimming is not None:
            self.dimming = self._define_object(dimming, Dimming)
