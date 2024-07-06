from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class Success(BaseModel):
    """Success

    :param username: username, defaults to None
    :type username: str, optional
    :param clientkey: clientkey, defaults to None
    :type clientkey: str, optional
    """

    def __init__(self, username: str = None, clientkey: str = None):
        if username is not None:
            self.username = username
        if clientkey is not None:
            self.clientkey = clientkey


@JsonMap({"type_": "type"})
class ResponseError(BaseModel):
    """ResponseError

    :param type_: type_, defaults to None
    :type type_: int, optional
    :param address: address, defaults to None
    :type address: str, optional
    :param description: description, defaults to None
    :type description: str, optional
    """

    def __init__(self, type_: int = None, address: str = None, description: str = None):
        if type_ is not None:
            self.type_ = type_
        if address is not None:
            self.address = address
        if description is not None:
            self.description = description


@JsonMap({})
class Response(BaseModel):
    """Response

    :param success: success, defaults to None
    :type success: Success, optional
    :param error: error, defaults to None
    :type error: ResponseError, optional
    """

    def __init__(self, success: Success = None, error: ResponseError = None):
        if success is not None:
            self.success = self._define_object(success, Success)
        if error is not None:
            self.error = self._define_object(error, ResponseError)
