from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class ColorTemperatureDeltaAction(Enum):
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
        return list(
            map(lambda x: x.value, ColorTemperatureDeltaAction._member_map_.values())
        )


@JsonMap({})
class ColorTemperatureDelta(BaseModel):
    """ColorTemperatureDelta

    :param action: action, defaults to None
    :type action: ColorTemperatureDeltaAction, optional
    :param mirek_delta: Mirek delta to current mirek. Clip at mirek_minimum and mirek_maximum of mirek_schema., defaults to None
    :type mirek_delta: int, optional
    """

    def __init__(
        self, action: ColorTemperatureDeltaAction = None, mirek_delta: int = None
    ):
        if action is not None:
            self.action = self._enum_matching(
                action, ColorTemperatureDeltaAction.list(), "action"
            )
        if mirek_delta is not None:
            self.mirek_delta = mirek_delta
