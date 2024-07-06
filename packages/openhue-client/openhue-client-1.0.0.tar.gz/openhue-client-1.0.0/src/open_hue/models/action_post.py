from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier
from .on import On
from .dimming import Dimming
from .color import Color
from .gradient import Gradient
from .dynamics_2 import Dynamics2
from .supported_effects import SupportedEffects


@JsonMap({})
class ActionColorTemperature(BaseModel):
    """ActionColorTemperature

    :param mirek: color temperature in mirek or null when the light color is not in the ct spectrum, defaults to None
    :type mirek: int, optional
    """

    def __init__(self, mirek: int = None):
        if mirek is not None:
            self.mirek = mirek


@JsonMap({})
class ActionEffects2(BaseModel):
    """Basic feature containing effect properties.

    :param effect: effect, defaults to None
    :type effect: SupportedEffects, optional
    """

    def __init__(self, effect: SupportedEffects = None):
        if effect is not None:
            self.effect = self._enum_matching(effect, SupportedEffects.list(), "effect")


@JsonMap({})
class ActionPostAction(BaseModel):
    """The action to be executed on recall

    :param on: on, defaults to None
    :type on: On, optional
    :param dimming: dimming, defaults to None
    :type dimming: Dimming, optional
    :param color: color, defaults to None
    :type color: Color, optional
    :param color_temperature: color_temperature, defaults to None
    :type color_temperature: ActionColorTemperature, optional
    :param gradient: Basic feature containing gradient properties., defaults to None
    :type gradient: Gradient, optional
    :param effects: Basic feature containing effect properties., defaults to None
    :type effects: ActionEffects2, optional
    :param dynamics: dynamics, defaults to None
    :type dynamics: Dynamics2, optional
    """

    def __init__(
        self,
        on: On = None,
        dimming: Dimming = None,
        color: Color = None,
        color_temperature: ActionColorTemperature = None,
        gradient: Gradient = None,
        effects: ActionEffects2 = None,
        dynamics: Dynamics2 = None,
    ):
        if on is not None:
            self.on = self._define_object(on, On)
        if dimming is not None:
            self.dimming = self._define_object(dimming, Dimming)
        if color is not None:
            self.color = self._define_object(color, Color)
        if color_temperature is not None:
            self.color_temperature = self._define_object(
                color_temperature, ActionColorTemperature
            )
        if gradient is not None:
            self.gradient = self._define_object(gradient, Gradient)
        if effects is not None:
            self.effects = self._define_object(effects, ActionEffects2)
        if dynamics is not None:
            self.dynamics = self._define_object(dynamics, Dynamics2)


@JsonMap({})
class ActionPost(BaseModel):
    """ActionPost

    :param target: target
    :type target: ResourceIdentifier
    :param action: The action to be executed on recall
    :type action: ActionPostAction
    """

    def __init__(self, target: ResourceIdentifier, action: ActionPostAction):
        self.target = self._define_object(target, ResourceIdentifier)
        self.action = self._define_object(action, ActionPostAction)
