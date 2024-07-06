from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class Dimming(BaseModel):
    """Dimming

    :param brightness: Brightness percentage. value cannot be 0, writing 0 changes it to lowest possible brightness, defaults to None
    :type brightness: float, optional
    """

    def __init__(self, brightness: float = None):
        if brightness is not None:
            self.brightness = brightness
