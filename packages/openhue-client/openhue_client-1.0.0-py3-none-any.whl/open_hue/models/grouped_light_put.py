from __future__ import annotations
from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel
from .on import On
from .dimming import Dimming
from .dimming_delta import DimmingDelta
from .color_temperature import ColorTemperature
from .color_temperature_delta import ColorTemperatureDelta
from .color import Color
from .alert import Alert
from .signaling import Signaling
from .dynamics_2 import Dynamics2


class GroupedLightPutType(Enum):
    """An enumeration representing different categories.

    :cvar GROUPED_LIGHT: "grouped_light"
    :vartype GROUPED_LIGHT: str
    """

    GROUPED_LIGHT = "grouped_light"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, GroupedLightPutType._member_map_.values()))


@JsonMap({"type_": "type"})
class GroupedLightPut(BaseModel):
    """GroupedLightPut

    :param type_: Type of the supported resources (always `grouped_light` here), defaults to None
    :type type_: GroupedLightPutType, optional
    :param on: on, defaults to None
    :type on: On, optional
    :param dimming: dimming, defaults to None
    :type dimming: Dimming, optional
    :param dimming_delta: dimming_delta, defaults to None
    :type dimming_delta: DimmingDelta, optional
    :param color_temperature: color_temperature, defaults to None
    :type color_temperature: ColorTemperature, optional
    :param color_temperature_delta: color_temperature_delta, defaults to None
    :type color_temperature_delta: ColorTemperatureDelta, optional
    :param color: color, defaults to None
    :type color: Color, optional
    :param alert: Joined alert control, defaults to None
    :type alert: Alert, optional
    :param signaling: Feature containing basic signaling properties., defaults to None
    :type signaling: Signaling, optional
    :param dynamics: dynamics, defaults to None
    :type dynamics: Dynamics2, optional
    """

    def __init__(
        self,
        type_: GroupedLightPutType = None,
        on: On = None,
        dimming: Dimming = None,
        dimming_delta: DimmingDelta = None,
        color_temperature: ColorTemperature = None,
        color_temperature_delta: ColorTemperatureDelta = None,
        color: Color = None,
        alert: Alert = None,
        signaling: Signaling = None,
        dynamics: Dynamics2 = None,
    ):
        if type_ is not None:
            self.type_ = self._enum_matching(type_, GroupedLightPutType.list(), "type_")
        if on is not None:
            self.on = self._define_object(on, On)
        if dimming is not None:
            self.dimming = self._define_object(dimming, Dimming)
        if dimming_delta is not None:
            self.dimming_delta = self._define_object(dimming_delta, DimmingDelta)
        if color_temperature is not None:
            self.color_temperature = self._define_object(
                color_temperature, ColorTemperature
            )
        if color_temperature_delta is not None:
            self.color_temperature_delta = self._define_object(
                color_temperature_delta, ColorTemperatureDelta
            )
        if color is not None:
            self.color = self._define_object(color, Color)
        if alert is not None:
            self.alert = self._define_object(alert, Alert)
        if signaling is not None:
            self.signaling = self._define_object(signaling, Signaling)
        if dynamics is not None:
            self.dynamics = self._define_object(dynamics, Dynamics2)
