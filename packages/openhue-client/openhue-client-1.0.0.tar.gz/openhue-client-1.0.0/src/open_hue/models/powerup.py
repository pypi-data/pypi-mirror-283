from __future__ import annotations
from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel
from .on import On
from .color import Color


class PowerupPreset2(Enum):
    """An enumeration representing different categories.

    :cvar SAFETY: "safety"
    :vartype SAFETY: str
    :cvar POWERFAIL: "powerfail"
    :vartype POWERFAIL: str
    :cvar LAST_ON_STATE: "last_on_state"
    :vartype LAST_ON_STATE: str
    :cvar CUSTOM: "custom"
    :vartype CUSTOM: str
    """

    SAFETY = "safety"
    POWERFAIL = "powerfail"
    LAST_ON_STATE = "last_on_state"
    CUSTOM = "custom"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, PowerupPreset2._member_map_.values()))


class OnMode2(Enum):
    """An enumeration representing different categories.

    :cvar ON: "on"
    :vartype ON: str
    :cvar TOGGLE: "toggle"
    :vartype TOGGLE: str
    :cvar PREVIOUS: "previous"
    :vartype PREVIOUS: str
    """

    ON = "on"
    TOGGLE = "toggle"
    PREVIOUS = "previous"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, OnMode2._member_map_.values()))


@JsonMap({})
class PowerupOn2(BaseModel):
    """PowerupOn2

    :param mode: State to activate after powerup.<br/>On will use the value specified in the “on” property.<br/>When setting mode “on”, the on property must be included.<br/>Toggle will alternate between on and off on each subsequent power toggle.<br/>Previous will return to the state it was in before powering off.<br/>, defaults to None
    :type mode: OnMode2, optional
    :param on: on, defaults to None
    :type on: On, optional
    """

    def __init__(self, mode: OnMode2 = None, on: On = None):
        if mode is not None:
            self.mode = self._enum_matching(mode, OnMode2.list(), "mode")
        if on is not None:
            self.on = self._define_object(on, On)


class DimmingMode2(Enum):
    """An enumeration representing different categories.

    :cvar DIMMING: "dimming"
    :vartype DIMMING: str
    :cvar PREVIOUS: "previous"
    :vartype PREVIOUS: str
    """

    DIMMING = "dimming"
    PREVIOUS = "previous"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, DimmingMode2._member_map_.values()))


class ColorMode2(Enum):
    """An enumeration representing different categories.

    :cvar COLOR_TEMPERATURE: "color_temperature"
    :vartype COLOR_TEMPERATURE: str
    :cvar COLOR: "color"
    :vartype COLOR: str
    :cvar PREVIOUS: "previous"
    :vartype PREVIOUS: str
    """

    COLOR_TEMPERATURE = "color_temperature"
    COLOR = "color"
    PREVIOUS = "previous"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ColorMode2._member_map_.values()))


@JsonMap({})
class ColorColorTemperature2(BaseModel):
    """ColorColorTemperature2

    :param mirek: color temperature in mirek or null when the light color is not in the ct spectrum, defaults to None
    :type mirek: int, optional
    :param color: color, defaults to None
    :type color: Color, optional
    """

    def __init__(self, mirek: int = None, color: Color = None):
        if mirek is not None:
            self.mirek = mirek
        if color is not None:
            self.color = self._define_object(color, Color)


@JsonMap({})
class DimmingColor2(BaseModel):
    """DimmingColor2

    :param mode: State to activate after powerup. Availability of “color_temperature” and “color” modes depend on the capabilities of the lamp. Colortemperature will set the colortemperature to the specified value after power up. When setting color_temperature, the color_temperature property must be included Color will set the color tot he specified value after power up. When setting color mode, the color property must be included Previous will set color to the state it was in before powering off., defaults to None
    :type mode: ColorMode2, optional
    :param color_temperature: color_temperature, defaults to None
    :type color_temperature: ColorColorTemperature2, optional
    """

    def __init__(
        self, mode: ColorMode2 = None, color_temperature: ColorColorTemperature2 = None
    ):
        if mode is not None:
            self.mode = self._enum_matching(mode, ColorMode2.list(), "mode")
        if color_temperature is not None:
            self.color_temperature = self._define_object(
                color_temperature, ColorColorTemperature2
            )


@JsonMap({})
class PowerupDimming2(BaseModel):
    """PowerupDimming2

    :param mode: Dimming will set the brightness to the specified value after power up.<br/>When setting mode “dimming”, the dimming property must be included.<br/>Previous will set brightness to the state it was in before powering off.<br/>, defaults to None
    :type mode: DimmingMode2, optional
    :param dimming: Brightness percentage. value cannot be 0, writing 0 changes it to lowest possible brightness, defaults to None
    :type dimming: float, optional
    :param color: color, defaults to None
    :type color: DimmingColor2, optional
    """

    def __init__(
        self,
        mode: DimmingMode2 = None,
        dimming: float = None,
        color: DimmingColor2 = None,
    ):
        if mode is not None:
            self.mode = self._enum_matching(mode, DimmingMode2.list(), "mode")
        if dimming is not None:
            self.dimming = dimming
        if color is not None:
            self.color = self._define_object(color, DimmingColor2)


@JsonMap({})
class Powerup(BaseModel):
    """Feature containing properties to configure powerup behaviour of a lightsource.

    :param preset: When setting the custom preset the additional properties can be set. For all other presets, no other properties can be included., defaults to None
    :type preset: PowerupPreset2, optional
    :param configured: Indicates if the shown values have been configured in the lightsource., defaults to None
    :type configured: bool, optional
    :param on: on, defaults to None
    :type on: PowerupOn2, optional
    :param dimming: dimming, defaults to None
    :type dimming: PowerupDimming2, optional
    """

    def __init__(
        self,
        preset: PowerupPreset2 = None,
        configured: bool = None,
        on: PowerupOn2 = None,
        dimming: PowerupDimming2 = None,
    ):
        if preset is not None:
            self.preset = self._enum_matching(preset, PowerupPreset2.list(), "preset")
        if configured is not None:
            self.configured = configured
        if on is not None:
            self.on = self._define_object(on, PowerupOn2)
        if dimming is not None:
            self.dimming = self._define_object(dimming, PowerupDimming2)
