from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_bridge_homes_ok_response import GetBridgeHomesOkResponse
from ..models.get_bridge_home_ok_response import GetBridgeHomeOkResponse


class BridgeHomeService(BaseService):

    @cast_models
    def get_bridge_homes(self) -> GetBridgeHomesOkResponse:
        """List all available bridge homes.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Bridge Home Success Response
        :rtype: GetBridgeHomesOkResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/bridge_home",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetBridgeHomesOkResponse._unmap(response)

    @cast_models
    def get_bridge_home(self, bridge_home_id: str) -> GetBridgeHomeOkResponse:
        """Get details of a single bridge home from its given `{bridgeHomeId}`.

        :param bridge_home_id: ID of the bridge home.
        :type bridge_home_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Bridge Home Success Response
        :rtype: GetBridgeHomeOkResponse
        """

        Validator(str).validate(bridge_home_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/bridge_home/{{bridgeHomeId}}",
                self.get_default_headers(),
            )
            .add_path("bridgeHomeId", bridge_home_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetBridgeHomeOkResponse._unmap(response)
