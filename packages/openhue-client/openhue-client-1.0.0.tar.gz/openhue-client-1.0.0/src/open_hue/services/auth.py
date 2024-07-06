from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.response import Response
from ..models.authenticate_request import AuthenticateRequest


class AuthService(BaseService):

    @cast_models
    def authenticate(self, request_body: AuthenticateRequest = None) -> List[Response]:
        """Authenticate to retrieve the HUE application key. Requires to go and press the button on the bridge

        :param request_body: The request body., defaults to None
        :type request_body: AuthenticateRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Authentication Success
        :rtype: List[Response]
        """

        Validator(AuthenticateRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/api", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return [Response._unmap(item) for item in response]
