from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class Dynamics2(BaseModel):
    """Dynamics2

    :param duration: Duration of a light transition or timed effects in ms., defaults to None
    :type duration: int, optional
    """

    def __init__(self, duration: int = None):
        if duration is not None:
            self.duration = duration
