from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class Dynamics(BaseModel):
    """Dynamics

    :param duration: Duration of a light transition or timed effects in ms., defaults to None
    :type duration: int, optional
    :param speed: Speed of dynamic palette or effect.<br/>The speed is valid for the dynamic palette if the status is `dynamic_palette` or for the corresponding effect listed in status.<br/>In case of status `none`, the speed is not valid.<br/>, defaults to None
    :type speed: float, optional
    """

    def __init__(self, duration: int = None, speed: float = None):
        if duration is not None:
            self.duration = duration
        if speed is not None:
            self.speed = speed
