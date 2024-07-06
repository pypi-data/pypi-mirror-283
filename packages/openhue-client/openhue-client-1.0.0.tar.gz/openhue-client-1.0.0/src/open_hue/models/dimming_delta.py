from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class DimmingDeltaAction(Enum):
    """An enumeration representing different categories.

    :cvar UP: "up"
    :vartype UP: str
    :cvar DOWN: "down"
    :vartype DOWN: str
    :cvar STOP: "stop"
    :vartype STOP: str
    """

    UP = "up"
    DOWN = "down"
    STOP = "stop"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, DimmingDeltaAction._member_map_.values()))


@JsonMap({})
class DimmingDelta(BaseModel):
    """DimmingDelta

    :param action: action, defaults to None
    :type action: DimmingDeltaAction, optional
    :param brightness_delta: Brightness percentage of full-scale increase delta to current dimlevel. Clip at Max-level or Min-level.<br/>, defaults to None
    :type brightness_delta: float, optional
    """

    def __init__(
        self, action: DimmingDeltaAction = None, brightness_delta: float = None
    ):
        if action is not None:
            self.action = self._enum_matching(
                action, DimmingDeltaAction.list(), "action"
            )
        if brightness_delta is not None:
            self.brightness_delta = brightness_delta
