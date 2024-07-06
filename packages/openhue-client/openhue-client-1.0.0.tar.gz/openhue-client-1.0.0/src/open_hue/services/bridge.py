from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_bridge_ok_response import UpdateBridgeOkResponse
from ..models.get_bridges_ok_response import GetBridgesOkResponse
from ..models.get_bridge_ok_response import GetBridgeOkResponse
from ..models.bridge_put import BridgePut


class BridgeService(BaseService):

    @cast_models
    def get_bridges(self) -> GetBridgesOkResponse:
        """List all available bridges

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Bridge Success Response
        :rtype: GetBridgesOkResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/bridge", self.get_default_headers()
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetBridgesOkResponse._unmap(response)

    @cast_models
    def get_bridge(self, bridge_id: str) -> GetBridgeOkResponse:
        """Get details of a single bridge from its given `{bridgeId}`.

        :param bridge_id: ID of the bridge
        :type bridge_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Bridge Success Response
        :rtype: GetBridgeOkResponse
        """

        Validator(str).validate(bridge_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/bridge/{{bridgeId}}",
                self.get_default_headers(),
            )
            .add_path("bridgeId", bridge_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetBridgeOkResponse._unmap(response)

    @cast_models
    def update_bridge(
        self, bridge_id: str, request_body: BridgePut = None
    ) -> UpdateBridgeOkResponse:
        """Update a single bridge from its given `{bridgeId}`.

        :param request_body: The request body., defaults to None
        :type request_body: BridgePut, optional
        :param bridge_id: ID of the bridge
        :type bridge_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateBridgeOkResponse
        """

        Validator(BridgePut).is_optional().validate(request_body)
        Validator(str).validate(bridge_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/bridge/{{bridgeId}}",
                self.get_default_headers(),
            )
            .add_path("bridgeId", bridge_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateBridgeOkResponse._unmap(response)
