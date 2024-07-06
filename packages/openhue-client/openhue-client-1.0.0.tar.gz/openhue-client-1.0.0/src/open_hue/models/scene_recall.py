from __future__ import annotations
from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel
from .dimming import Dimming


class SceneRecallAction(Enum):
    """An enumeration representing different categories.

    :cvar ACTIVE: "active"
    :vartype ACTIVE: str
    :cvar DYNAMIC_PALETTE: "dynamic_palette"
    :vartype DYNAMIC_PALETTE: str
    :cvar STATIC: "static"
    :vartype STATIC: str
    """

    ACTIVE = "active"
    DYNAMIC_PALETTE = "dynamic_palette"
    STATIC = "static"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SceneRecallAction._member_map_.values()))


@JsonMap({})
class SceneRecall(BaseModel):
    """SceneRecall

    :param action: When writing active, the actions in the scene are executed on the target. dynamic_palette starts dynamic scene with colors in the Palette object., defaults to None
    :type action: SceneRecallAction, optional
    :param duration: Transition to the scene within the timeframe given by duration, defaults to None
    :type duration: int, optional
    :param dimming: dimming, defaults to None
    :type dimming: Dimming, optional
    """

    def __init__(
        self,
        action: SceneRecallAction = None,
        duration: int = None,
        dimming: Dimming = None,
    ):
        if action is not None:
            self.action = self._enum_matching(
                action, SceneRecallAction.list(), "action"
            )
        if duration is not None:
            self.duration = duration
        if dimming is not None:
            self.dimming = self._define_object(dimming, Dimming)
