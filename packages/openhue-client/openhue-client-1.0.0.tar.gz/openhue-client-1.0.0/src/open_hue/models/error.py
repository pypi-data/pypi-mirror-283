from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class Error(BaseModel):
    """Error

    :param description: a human-readable explanation specific to this occurrence of the problem., defaults to None
    :type description: str, optional
    """

    def __init__(self, description: str = None):
        if description is not None:
            self.description = description
