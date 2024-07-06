from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AuthenticateRequest(BaseModel):
    """AuthenticateRequest

    :param devicetype: devicetype, defaults to None
    :type devicetype: str, optional
    :param generateclientkey: generateclientkey, defaults to None
    :type generateclientkey: bool, optional
    """

    def __init__(self, devicetype: str = None, generateclientkey: bool = None):
        if devicetype is not None:
            self.devicetype = devicetype
        if generateclientkey is not None:
            self.generateclientkey = generateclientkey
