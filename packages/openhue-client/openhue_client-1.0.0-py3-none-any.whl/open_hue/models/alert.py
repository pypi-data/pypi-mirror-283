from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class Alert(BaseModel):
    """Joined alert control

    :param action: action, defaults to None
    :type action: str, optional
    """

    def __init__(self, action: str = None):
        if action is not None:
            self.action = action
