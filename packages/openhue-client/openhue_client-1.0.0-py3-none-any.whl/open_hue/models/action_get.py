from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier
from .on import On
from .dimming import Dimming
from .color import Color
from .color_temperature import ColorTemperature
from .gradient import Gradient
from .supported_effects import SupportedEffects


@JsonMap({})
class ActionEffects1(BaseModel):
    """Basic feature containing effect properties.

    :param effect: effect, defaults to None
    :type effect: SupportedEffects, optional
    """

    def __init__(self, effect: SupportedEffects = None):
        if effect is not None:
            self.effect = self._enum_matching(effect, SupportedEffects.list(), "effect")


@JsonMap({})
class ActionGetAction(BaseModel):
    """The action to be executed on recall

    :param on: on, defaults to None
    :type on: On, optional
    :param dimming: dimming, defaults to None
    :type dimming: Dimming, optional
    :param color: color, defaults to None
    :type color: Color, optional
    :param color_temperature: color_temperature, defaults to None
    :type color_temperature: ColorTemperature, optional
    :param gradient: Basic feature containing gradient properties., defaults to None
    :type gradient: Gradient, optional
    :param effects: Basic feature containing effect properties., defaults to None
    :type effects: ActionEffects1, optional
    """

    def __init__(
        self,
        on: On = None,
        dimming: Dimming = None,
        color: Color = None,
        color_temperature: ColorTemperature = None,
        gradient: Gradient = None,
        effects: ActionEffects1 = None,
    ):
        if on is not None:
            self.on = self._define_object(on, On)
        if dimming is not None:
            self.dimming = self._define_object(dimming, Dimming)
        if color is not None:
            self.color = self._define_object(color, Color)
        if color_temperature is not None:
            self.color_temperature = self._define_object(
                color_temperature, ColorTemperature
            )
        if gradient is not None:
            self.gradient = self._define_object(gradient, Gradient)
        if effects is not None:
            self.effects = self._define_object(effects, ActionEffects1)


@JsonMap({"type_": "type", "id_": "id"})
class ActionGet(BaseModel):
    """ActionGet

    :param type_: Type of the supported resources, defaults to None
    :type type_: str, optional
    :param id_: Unique identifier representing a specific resource instance, defaults to None
    :type id_: str, optional
    :param id_v1: Clip v1 resource identifier, defaults to None
    :type id_v1: str, optional
    :param owner: owner, defaults to None
    :type owner: ResourceIdentifier, optional
    :param target: target, defaults to None
    :type target: ResourceIdentifier, optional
    :param action: The action to be executed on recall, defaults to None
    :type action: ActionGetAction, optional
    """

    def __init__(
        self,
        type_: str = None,
        id_: str = None,
        id_v1: str = None,
        owner: ResourceIdentifier = None,
        target: ResourceIdentifier = None,
        action: ActionGetAction = None,
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
        if target is not None:
            self.target = self._define_object(target, ResourceIdentifier)
        if action is not None:
            self.action = self._define_object(action, ActionGetAction)
