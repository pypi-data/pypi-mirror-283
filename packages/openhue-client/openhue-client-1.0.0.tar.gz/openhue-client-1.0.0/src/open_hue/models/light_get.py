from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier
from .on import On
from .light_archetype import LightArchetype
from .gamut_position import GamutPosition
from .supported_dynamic_status import SupportedDynamicStatus
from .supported_signals import SupportedSignals
from .color import Color
from .supported_gradient_mode import SupportedGradientMode
from .supported_effects import SupportedEffects
from .supported_timed_effects import SupportedTimedEffects
from .dimming import Dimming


@JsonMap({})
class LightGetMetadata(BaseModel):
    """Deprecated, use metadata on device level

    :param name: Human readable name of a resource, defaults to None
    :type name: str, optional
    :param archetype: Light archetype, defaults to None
    :type archetype: LightArchetype, optional
    :param fixed_mired: A fixed mired value of the white lamp, defaults to None
    :type fixed_mired: int, optional
    """

    def __init__(
        self,
        name: str = None,
        archetype: LightArchetype = None,
        fixed_mired: int = None,
    ):
        if name is not None:
            self.name = name
        if archetype is not None:
            self.archetype = self._enum_matching(
                archetype, LightArchetype.list(), "archetype"
            )
        if fixed_mired is not None:
            self.fixed_mired = fixed_mired


@JsonMap({})
class LightGetDimming(BaseModel):
    """LightGetDimming

    :param brightness: Brightness percentage. value cannot be 0, writing 0 changes it to lowest possible brightness, defaults to None
    :type brightness: float, optional
    :param min_dim_level: Percentage of the maximum lumen the device outputs on minimum brightness, defaults to None
    :type min_dim_level: float, optional
    """

    def __init__(self, brightness: float = None, min_dim_level: float = None):
        if brightness is not None:
            self.brightness = brightness
        if min_dim_level is not None:
            self.min_dim_level = min_dim_level


@JsonMap({})
class MirekSchema(BaseModel):
    """MirekSchema

    :param mirek_minimum: minimum color temperature this light supports, defaults to None
    :type mirek_minimum: int, optional
    :param mirek_maximum: maximum color temperature this light supports, defaults to None
    :type mirek_maximum: int, optional
    """

    def __init__(self, mirek_minimum: int = None, mirek_maximum: int = None):
        if mirek_minimum is not None:
            self.mirek_minimum = mirek_minimum
        if mirek_maximum is not None:
            self.mirek_maximum = mirek_maximum


@JsonMap({})
class LightGetColorTemperature(BaseModel):
    """LightGetColorTemperature

    :param mirek: color temperature in mirek or null when the light color is not in the ct spectrum, defaults to None
    :type mirek: int, optional
    :param mirek_valid: Indication whether the value presented in mirek is valid, defaults to None
    :type mirek_valid: bool, optional
    :param mirek_schema: mirek_schema, defaults to None
    :type mirek_schema: MirekSchema, optional
    """

    def __init__(
        self,
        mirek: int = None,
        mirek_valid: bool = None,
        mirek_schema: MirekSchema = None,
    ):
        if mirek is not None:
            self.mirek = mirek
        if mirek_valid is not None:
            self.mirek_valid = mirek_valid
        if mirek_schema is not None:
            self.mirek_schema = self._define_object(mirek_schema, MirekSchema)


@JsonMap({})
class Gamut(BaseModel):
    """Color gamut of color bulb. Some bulbs do not properly return the Gamut information. In this case this is not present.

    :param red: CIE XY gamut position, defaults to None
    :type red: GamutPosition, optional
    :param green: CIE XY gamut position, defaults to None
    :type green: GamutPosition, optional
    :param blue: CIE XY gamut position, defaults to None
    :type blue: GamutPosition, optional
    """

    def __init__(
        self,
        red: GamutPosition = None,
        green: GamutPosition = None,
        blue: GamutPosition = None,
    ):
        if red is not None:
            self.red = self._define_object(red, GamutPosition)
        if green is not None:
            self.green = self._define_object(green, GamutPosition)
        if blue is not None:
            self.blue = self._define_object(blue, GamutPosition)


class GamutType(Enum):
    """An enumeration representing different categories.

    :cvar A: "A"
    :vartype A: str
    :cvar B: "B"
    :vartype B: str
    :cvar C: "C"
    :vartype C: str
    :cvar OTHER: "other"
    :vartype OTHER: str
    """

    A = "A"
    B = "B"
    C = "C"
    OTHER = "other"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, GamutType._member_map_.values()))


@JsonMap({})
class LightGetColor(BaseModel):
    """LightGetColor

    :param xy: CIE XY gamut position, defaults to None
    :type xy: GamutPosition, optional
    :param gamut: Color gamut of color bulb. Some bulbs do not properly return the Gamut information. In this case this is not present., defaults to None
    :type gamut: Gamut, optional
    :param gamut_type: The gammut types supported by hue – A Gamut of early Philips color-only products – B Limited gamut of first Hue color products – C Richer color gamut of Hue white and color ambiance products – other Color gamut of non-hue products with non-hue gamuts resp w/o gamut, defaults to None
    :type gamut_type: GamutType, optional
    """

    def __init__(
        self,
        xy: GamutPosition = None,
        gamut: Gamut = None,
        gamut_type: GamutType = None,
    ):
        if xy is not None:
            self.xy = self._define_object(xy, GamutPosition)
        if gamut is not None:
            self.gamut = self._define_object(gamut, Gamut)
        if gamut_type is not None:
            self.gamut_type = self._enum_matching(
                gamut_type, GamutType.list(), "gamut_type"
            )


@JsonMap({})
class LightGetDynamics(BaseModel):
    """LightGetDynamics

    :param status: Current status of the lamp with dynamics., defaults to None
    :type status: SupportedDynamicStatus, optional
    :param status_values: Statuses in which a lamp could be when playing dynamics., defaults to None
    :type status_values: List[SupportedDynamicStatus], optional
    :param speed: speed of dynamic palette or effect. The speed is valid for the dynamic palette if the status is dynamic_palette or for the corresponding effect listed in status. In case of status none, the speed is not valid, defaults to None
    :type speed: float, optional
    :param speed_valid: Indicates whether the value presented in speed is valid, defaults to None
    :type speed_valid: bool, optional
    """

    def __init__(
        self,
        status: SupportedDynamicStatus = None,
        status_values: List[SupportedDynamicStatus] = None,
        speed: float = None,
        speed_valid: bool = None,
    ):
        if status is not None:
            self.status = self._enum_matching(
                status, SupportedDynamicStatus.list(), "status"
            )
        if status_values is not None:
            self.status_values = self._define_list(
                status_values, SupportedDynamicStatus
            )
        if speed is not None:
            self.speed = speed
        if speed_valid is not None:
            self.speed_valid = speed_valid


@JsonMap({})
class LightGetSignaling(BaseModel):
    """Feature containing signaling properties.

    :param signal_values: signal_values, defaults to None
    :type signal_values: List[SupportedSignals], optional
    :param estimated_end: Timestamp indicating when the active signal is expected to end. Value is not set if there is no_signal, defaults to None
    :type estimated_end: int, optional
    :param colors: Colors that were provided for the active effect., defaults to None
    :type colors: List[Color], optional
    """

    def __init__(
        self,
        signal_values: List[SupportedSignals] = None,
        estimated_end: int = None,
        colors: List[Color] = None,
    ):
        if signal_values is not None:
            self.signal_values = self._define_list(signal_values, SupportedSignals)
        if estimated_end is not None:
            self.estimated_end = estimated_end
        if colors is not None:
            self.colors = self._define_list(colors, Color)


class LightGetMode(Enum):
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
        return list(map(lambda x: x.value, LightGetMode._member_map_.values()))


@JsonMap({})
class LightGetGradient(BaseModel):
    """LightGetGradient

    :param points: Collection of gradients points. For control of the gradient points through a PUT a minimum of 2 points need to be provided., defaults to None
    :type points: List[Color], optional
    :param mode: Mode in which the points are currently being deployed. If not provided during PUT/POST it will be defaulted to interpolated_palette, defaults to None
    :type mode: SupportedGradientMode, optional
    :param points_capable: Number of color points that gradient lamp is capable of showing with gradience., defaults to None
    :type points_capable: int, optional
    :param mode_values: Modes a gradient device can deploy the gradient palette of colors, defaults to None
    :type mode_values: List[SupportedGradientMode], optional
    :param pixel_count: Number of pixels in the device, defaults to None
    :type pixel_count: int, optional
    """

    def __init__(
        self,
        points: List[Color] = None,
        mode: SupportedGradientMode = None,
        points_capable: int = None,
        mode_values: List[SupportedGradientMode] = None,
        pixel_count: int = None,
    ):
        if points is not None:
            self.points = self._define_list(points, Color)
        if mode is not None:
            self.mode = self._enum_matching(mode, SupportedGradientMode.list(), "mode")
        if points_capable is not None:
            self.points_capable = points_capable
        if mode_values is not None:
            self.mode_values = self._define_list(mode_values, SupportedGradientMode)
        if pixel_count is not None:
            self.pixel_count = pixel_count


@JsonMap({})
class LightGetEffects(BaseModel):
    """Basic feature containing effect properties.

    :param status: status, defaults to None
    :type status: SupportedEffects, optional
    :param status_values: Possible status values in which a light could be when playing an effect., defaults to None
    :type status_values: List[SupportedEffects], optional
    :param effect: effect, defaults to None
    :type effect: SupportedEffects, optional
    :param effect_values: Possible status values in which a light could be when playing an effect., defaults to None
    :type effect_values: List[SupportedEffects], optional
    """

    def __init__(
        self,
        status: SupportedEffects = None,
        status_values: List[SupportedEffects] = None,
        effect: SupportedEffects = None,
        effect_values: List[SupportedEffects] = None,
    ):
        if status is not None:
            self.status = self._enum_matching(status, SupportedEffects.list(), "status")
        if status_values is not None:
            self.status_values = self._define_list(status_values, SupportedEffects)
        if effect is not None:
            self.effect = self._enum_matching(effect, SupportedEffects.list(), "effect")
        if effect_values is not None:
            self.effect_values = self._define_list(effect_values, SupportedEffects)


@JsonMap({})
class LightGetTimedEffects(BaseModel):
    """Basic feature containing timed effect properties.

    :param effect: Current status values the light is in regarding timed effects, defaults to None
    :type effect: SupportedTimedEffects, optional
    :param effect_values: Possible timed effect values you can set in a light, defaults to None
    :type effect_values: List[SupportedTimedEffects], optional
    :param status: Current status values the light is in regarding timed effects, defaults to None
    :type status: SupportedTimedEffects, optional
    :param status_values: Possible status values in which a light could be when playing a timed effect., defaults to None
    :type status_values: List[SupportedTimedEffects], optional
    :param duration: Duration is mandatory when timed effect is set except for no_effect. Resolution decreases for a larger duration. e.g Effects with duration smaller than a minute will be rounded to a resolution of 1s, while effects with duration larger than an hour will be arounded up to a resolution of 300s. Duration has a max of 21600000 ms., defaults to None
    :type duration: int, optional
    """

    def __init__(
        self,
        effect: SupportedTimedEffects = None,
        effect_values: List[SupportedTimedEffects] = None,
        status: SupportedTimedEffects = None,
        status_values: List[SupportedTimedEffects] = None,
        duration: int = None,
    ):
        if effect is not None:
            self.effect = self._enum_matching(
                effect, SupportedTimedEffects.list(), "effect"
            )
        if effect_values is not None:
            self.effect_values = self._define_list(effect_values, SupportedTimedEffects)
        if status is not None:
            self.status = self._enum_matching(
                status, SupportedTimedEffects.list(), "status"
            )
        if status_values is not None:
            self.status_values = self._define_list(status_values, SupportedTimedEffects)
        if duration is not None:
            self.duration = duration


class PowerupPreset1(Enum):
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
        return list(map(lambda x: x.value, PowerupPreset1._member_map_.values()))


class OnMode1(Enum):
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
        return list(map(lambda x: x.value, OnMode1._member_map_.values()))


@JsonMap({})
class PowerupOn1(BaseModel):
    """PowerupOn1

    :param mode: State to activate after powerup.<br/>On will use the value specified in the “on” property.<br/>When setting mode “on”, the on property must be included.<br/>Toggle will alternate between on and off on each subsequent power toggle.<br/>Previous will return to the state it was in before powering off.<br/>, defaults to None
    :type mode: OnMode1, optional
    :param on: on, defaults to None
    :type on: On, optional
    """

    def __init__(self, mode: OnMode1 = None, on: On = None):
        if mode is not None:
            self.mode = self._enum_matching(mode, OnMode1.list(), "mode")
        if on is not None:
            self.on = self._define_object(on, On)


class DimmingMode1(Enum):
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
        return list(map(lambda x: x.value, DimmingMode1._member_map_.values()))


class ColorMode1(Enum):
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
        return list(map(lambda x: x.value, ColorMode1._member_map_.values()))


@JsonMap({})
class ColorColorTemperature1(BaseModel):
    """ColorColorTemperature1

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
class DimmingColor1(BaseModel):
    """DimmingColor1

    :param mode: State to activate after powerup. Availability of “color_temperature” and “color” modes depend on the capabilities of the lamp. Colortemperature will set the colortemperature to the specified value after power up. When setting color_temperature, the color_temperature property must be included Color will set the color tot he specified value after power up. When setting color mode, the color property must be included Previous will set color to the state it was in before powering off., defaults to None
    :type mode: ColorMode1, optional
    :param color_temperature: color_temperature, defaults to None
    :type color_temperature: ColorColorTemperature1, optional
    """

    def __init__(
        self, mode: ColorMode1 = None, color_temperature: ColorColorTemperature1 = None
    ):
        if mode is not None:
            self.mode = self._enum_matching(mode, ColorMode1.list(), "mode")
        if color_temperature is not None:
            self.color_temperature = self._define_object(
                color_temperature, ColorColorTemperature1
            )


@JsonMap({})
class PowerupDimming1(BaseModel):
    """PowerupDimming1

    :param mode: Dimming will set the brightness to the specified value after power up.<br/>When setting mode “dimming”, the dimming property must be included.<br/>Previous will set brightness to the state it was in before powering off.<br/>, defaults to None
    :type mode: DimmingMode1, optional
    :param dimming: dimming, defaults to None
    :type dimming: Dimming, optional
    :param color: color, defaults to None
    :type color: DimmingColor1, optional
    """

    def __init__(
        self,
        mode: DimmingMode1 = None,
        dimming: Dimming = None,
        color: DimmingColor1 = None,
    ):
        if mode is not None:
            self.mode = self._enum_matching(mode, DimmingMode1.list(), "mode")
        if dimming is not None:
            self.dimming = self._define_object(dimming, Dimming)
        if color is not None:
            self.color = self._define_object(color, DimmingColor1)


@JsonMap({})
class LightGetPowerup(BaseModel):
    """Feature containing properties to configure powerup behaviour of a lightsource.

    :param preset: When setting the custom preset the additional properties can be set. For all other presets, no other properties can be included., defaults to None
    :type preset: PowerupPreset1, optional
    :param configured: Indicates if the shown values have been configured in the lightsource., defaults to None
    :type configured: bool, optional
    :param on: on, defaults to None
    :type on: PowerupOn1, optional
    :param dimming: dimming, defaults to None
    :type dimming: PowerupDimming1, optional
    """

    def __init__(
        self,
        preset: PowerupPreset1 = None,
        configured: bool = None,
        on: PowerupOn1 = None,
        dimming: PowerupDimming1 = None,
    ):
        if preset is not None:
            self.preset = self._enum_matching(preset, PowerupPreset1.list(), "preset")
        if configured is not None:
            self.configured = configured
        if on is not None:
            self.on = self._define_object(on, PowerupOn1)
        if dimming is not None:
            self.dimming = self._define_object(dimming, PowerupDimming1)


@JsonMap({"type_": "type", "id_": "id"})
class LightGet(BaseModel):
    """LightGet

    :param type_: Type of the supported resources, defaults to None
    :type type_: str, optional
    :param id_: Unique identifier representing a specific resource instance, defaults to None
    :type id_: str, optional
    :param id_v1: Clip v1 resource identifier, defaults to None
    :type id_v1: str, optional
    :param owner: owner, defaults to None
    :type owner: ResourceIdentifier, optional
    :param metadata: Deprecated, use metadata on device level, defaults to None
    :type metadata: LightGetMetadata, optional
    :param on: on, defaults to None
    :type on: On, optional
    :param dimming: dimming, defaults to None
    :type dimming: LightGetDimming, optional
    :param color_temperature: color_temperature, defaults to None
    :type color_temperature: LightGetColorTemperature, optional
    :param color: color, defaults to None
    :type color: LightGetColor, optional
    :param dynamics: dynamics, defaults to None
    :type dynamics: LightGetDynamics, optional
    :param alert: TODO, defaults to None
    :type alert: dict, optional
    :param signaling: Feature containing signaling properties., defaults to None
    :type signaling: LightGetSignaling, optional
    :param mode: mode, defaults to None
    :type mode: LightGetMode, optional
    :param gradient: gradient, defaults to None
    :type gradient: LightGetGradient, optional
    :param effects: Basic feature containing effect properties., defaults to None
    :type effects: LightGetEffects, optional
    :param timed_effects: Basic feature containing timed effect properties., defaults to None
    :type timed_effects: LightGetTimedEffects, optional
    :param powerup: Feature containing properties to configure powerup behaviour of a lightsource., defaults to None
    :type powerup: LightGetPowerup, optional
    """

    def __init__(
        self,
        type_: str = None,
        id_: str = None,
        id_v1: str = None,
        owner: ResourceIdentifier = None,
        metadata: LightGetMetadata = None,
        on: On = None,
        dimming: LightGetDimming = None,
        color_temperature: LightGetColorTemperature = None,
        color: LightGetColor = None,
        dynamics: LightGetDynamics = None,
        alert: dict = None,
        signaling: LightGetSignaling = None,
        mode: LightGetMode = None,
        gradient: LightGetGradient = None,
        effects: LightGetEffects = None,
        timed_effects: LightGetTimedEffects = None,
        powerup: LightGetPowerup = None,
    ):
        if type_ is not None:
            self.type_ = type_
        if id_ is not None:
            self.id_ = self._pattern_matching(
                id_, "^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$", "id_"
            )
        if id_v1 is not None:
            self.id_v1 = self._pattern_matching(
                id_v1, "^(\/[a-z]{4,32}\/[0-9a-zA-Z-]{1,32})?$", "id_v1"
            )
        if owner is not None:
            self.owner = self._define_object(owner, ResourceIdentifier)
        if metadata is not None:
            self.metadata = self._define_object(metadata, LightGetMetadata)
        if on is not None:
            self.on = self._define_object(on, On)
        if dimming is not None:
            self.dimming = self._define_object(dimming, LightGetDimming)
        if color_temperature is not None:
            self.color_temperature = self._define_object(
                color_temperature, LightGetColorTemperature
            )
        if color is not None:
            self.color = self._define_object(color, LightGetColor)
        if dynamics is not None:
            self.dynamics = self._define_object(dynamics, LightGetDynamics)
        if alert is not None:
            self.alert = alert
        if signaling is not None:
            self.signaling = self._define_object(signaling, LightGetSignaling)
        if mode is not None:
            self.mode = self._enum_matching(mode, LightGetMode.list(), "mode")
        if gradient is not None:
            self.gradient = self._define_object(gradient, LightGetGradient)
        if effects is not None:
            self.effects = self._define_object(effects, LightGetEffects)
        if timed_effects is not None:
            self.timed_effects = self._define_object(
                timed_effects, LightGetTimedEffects
            )
        if powerup is not None:
            self.powerup = self._define_object(powerup, LightGetPowerup)
