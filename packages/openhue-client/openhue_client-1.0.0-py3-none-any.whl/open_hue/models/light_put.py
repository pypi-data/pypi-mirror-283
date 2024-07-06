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
from .dynamics import Dynamics
from .alert import Alert
from .signaling import Signaling
from .gradient import Gradient
from .effects import Effects
from .powerup import Powerup
from .supported_timed_effects import SupportedTimedEffects


class LightPutMode(Enum):
    """An enumeration representing different categories.

    :cvar NORMAL: "normal"
    :vartype NORMAL: str
    :cvar STREAMING: "streaming"
    :vartype STREAMING: str
    """

    NORMAL = "normal"
    STREAMING = "streaming"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, LightPutMode._member_map_.values()))


@JsonMap({})
class LightPutTimedEffects(BaseModel):
    """Basic feature containing timed effect properties.

    :param effect: Current status values the light is in regarding timed effects, defaults to None
    :type effect: SupportedTimedEffects, optional
    :param duration: Duration is mandatory when timed effect is set except for no_effect. Resolution decreases for a larger duration. e.g Effects with duration smaller than a minute will be rounded to a resolution of 1s, while effects with duration larger than an hour will be arounded up to a resolution of 300s. Duration has a max of 21600000 ms., defaults to None
    :type duration: int, optional
    """

    def __init__(self, effect: SupportedTimedEffects = None, duration: int = None):
        if effect is not None:
            self.effect = self._enum_matching(
                effect, SupportedTimedEffects.list(), "effect"
            )
        if duration is not None:
            self.duration = duration


@JsonMap({"type_": "type"})
class LightPut(BaseModel):
    """LightPut

    :param type_: Type of the supported resources (always `light` here), defaults to None
    :type type_: str, optional
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
    :param dynamics: dynamics, defaults to None
    :type dynamics: Dynamics, optional
    :param alert: Joined alert control, defaults to None
    :type alert: Alert, optional
    :param signaling: Feature containing basic signaling properties., defaults to None
    :type signaling: Signaling, optional
    :param mode: mode, defaults to None
    :type mode: LightPutMode, optional
    :param gradient: Basic feature containing gradient properties., defaults to None
    :type gradient: Gradient, optional
    :param effects: Basic feature containing effect properties., defaults to None
    :type effects: Effects, optional
    :param timed_effects: Basic feature containing timed effect properties., defaults to None
    :type timed_effects: LightPutTimedEffects, optional
    :param powerup: Feature containing properties to configure powerup behaviour of a lightsource., defaults to None
    :type powerup: Powerup, optional
    """

    def __init__(
        self,
        type_: str = None,
        on: On = None,
        dimming: Dimming = None,
        dimming_delta: DimmingDelta = None,
        color_temperature: ColorTemperature = None,
        color_temperature_delta: ColorTemperatureDelta = None,
        color: Color = None,
        dynamics: Dynamics = None,
        alert: Alert = None,
        signaling: Signaling = None,
        mode: LightPutMode = None,
        gradient: Gradient = None,
        effects: Effects = None,
        timed_effects: LightPutTimedEffects = None,
        powerup: Powerup = None,
    ):
        if type_ is not None:
            self.type_ = type_
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
        if dynamics is not None:
            self.dynamics = self._define_object(dynamics, Dynamics)
        if alert is not None:
            self.alert = self._define_object(alert, Alert)
        if signaling is not None:
            self.signaling = self._define_object(signaling, Signaling)
        if mode is not None:
            self.mode = self._enum_matching(mode, LightPutMode.list(), "mode")
        if gradient is not None:
            self.gradient = self._define_object(gradient, Gradient)
        if effects is not None:
            self.effects = self._define_object(effects, Effects)
        if timed_effects is not None:
            self.timed_effects = self._define_object(
                timed_effects, LightPutTimedEffects
            )
        if powerup is not None:
            self.powerup = self._define_object(powerup, Powerup)
