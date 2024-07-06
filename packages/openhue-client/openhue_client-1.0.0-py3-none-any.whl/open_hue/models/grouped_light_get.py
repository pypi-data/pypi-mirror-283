from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier
from .on import On
from .dimming import Dimming
from .supported_signals import SupportedSignals


@JsonMap({})
class GroupedLightGetAlert(BaseModel):
    """Joined alert control

    :param action_values: action_values, defaults to None
    :type action_values: List[str], optional
    """

    def __init__(self, action_values: List[str] = None):
        if action_values is not None:
            self.action_values = action_values


@JsonMap({})
class GroupedLightGetSignaling(BaseModel):
    """Feature containing basic signaling properties.

    :param signal_values: Signals that the light supports., defaults to None
    :type signal_values: List[SupportedSignals], optional
    """

    def __init__(self, signal_values: List[SupportedSignals] = None):
        if signal_values is not None:
            self.signal_values = self._define_list(signal_values, SupportedSignals)


@JsonMap({"type_": "type", "id_": "id"})
class GroupedLightGet(BaseModel):
    """GroupedLightGet

    :param type_: Type of the supported resources, defaults to None
    :type type_: str, optional
    :param id_: Unique identifier representing a specific resource instance, defaults to None
    :type id_: str, optional
    :param id_v1: Clip v1 resource identifier, defaults to None
    :type id_v1: str, optional
    :param owner: owner, defaults to None
    :type owner: ResourceIdentifier, optional
    :param on: on, defaults to None
    :type on: On, optional
    :param dimming: dimming, defaults to None
    :type dimming: Dimming, optional
    :param alert: Joined alert control, defaults to None
    :type alert: GroupedLightGetAlert, optional
    :param signaling: Feature containing basic signaling properties., defaults to None
    :type signaling: GroupedLightGetSignaling, optional
    """

    def __init__(
        self,
        type_: str = None,
        id_: str = None,
        id_v1: str = None,
        owner: ResourceIdentifier = None,
        on: On = None,
        dimming: Dimming = None,
        alert: GroupedLightGetAlert = None,
        signaling: GroupedLightGetSignaling = None,
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
        if on is not None:
            self.on = self._define_object(on, On)
        if dimming is not None:
            self.dimming = self._define_object(dimming, Dimming)
        if alert is not None:
            self.alert = self._define_object(alert, GroupedLightGetAlert)
        if signaling is not None:
            self.signaling = self._define_object(signaling, GroupedLightGetSignaling)
