from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class ColorTemperature(BaseModel):
    """ColorTemperature

    :param mirek: color temperature in mirek or null when the light color is not in the ct spectrum, defaults to None
    :type mirek: int, optional
    """

    def __init__(self, mirek: int = None):
        if mirek is not None:
            self.mirek = mirek
