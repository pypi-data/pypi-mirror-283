from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_temperature_ok_response import UpdateTemperatureOkResponse
from ..models.temperature_put import TemperaturePut
from ..models.get_temperatures_ok_response import GetTemperaturesOkResponse
from ..models.get_temperature_ok_response import GetTemperatureOkResponse


class TemperatureService(BaseService):

    @cast_models
    def get_temperatures(self) -> GetTemperaturesOkResponse:
        """List all temperatures

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Temperature Success Response
        :rtype: GetTemperaturesOkResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/temperature",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetTemperaturesOkResponse._unmap(response)

    @cast_models
    def get_temperature(self, temperature_id: str) -> GetTemperatureOkResponse:
        """Get details of a single temperature sensor from its given `{temperatureId}`.

        :param temperature_id: ID of the temperature sensor
        :type temperature_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Temperature Success Response
        :rtype: GetTemperatureOkResponse
        """

        Validator(str).validate(temperature_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/temperature/{{temperatureId}}",
                self.get_default_headers(),
            )
            .add_path("temperatureId", temperature_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetTemperatureOkResponse._unmap(response)

    @cast_models
    def update_temperature(
        self, temperature_id: str, request_body: TemperaturePut = None
    ) -> UpdateTemperatureOkResponse:
        """Update a temperature sensor from its given `{temperatureId}`.

        :param request_body: The request body., defaults to None
        :type request_body: TemperaturePut, optional
        :param temperature_id: ID of the temperature sensor
        :type temperature_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateTemperatureOkResponse
        """

        Validator(TemperaturePut).is_optional().validate(request_body)
        Validator(str).validate(temperature_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/temperature/{{temperatureId}}",
                self.get_default_headers(),
            )
            .add_path("temperatureId", temperature_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateTemperatureOkResponse._unmap(response)
