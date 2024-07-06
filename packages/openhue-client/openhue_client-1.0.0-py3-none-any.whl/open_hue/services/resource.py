from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_resources_ok_response import GetResourcesOkResponse


class ResourceService(BaseService):

    @cast_models
    def get_resources(self) -> GetResourcesOkResponse:
        """API to retrieve all API resources

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Resource Success Response
        :rtype: GetResourcesOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/clip/v2/resource", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetResourcesOkResponse._unmap(response)
