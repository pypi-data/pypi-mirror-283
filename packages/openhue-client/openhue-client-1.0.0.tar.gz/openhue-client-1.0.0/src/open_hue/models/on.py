from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class On(BaseModel):
    """On

    :param on: On/Off state of the light on=true, off=false, defaults to None
    :type on: bool, optional
    """

    def __init__(self, on: bool = None):
        if on is not None:
            self.on = on
