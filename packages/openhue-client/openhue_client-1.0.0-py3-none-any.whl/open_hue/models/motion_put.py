from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class MotionPutSensitivity(BaseModel):
    """MotionPutSensitivity

    :param sensitivity: Sensitivity of the sensor. Value in the range 0 to sensitivity_max., defaults to None
    :type sensitivity: int, optional
    """

    def __init__(self, sensitivity: int = None):
        if sensitivity is not None:
            self.sensitivity = sensitivity


@JsonMap({"type_": "type"})
class MotionPut(BaseModel):
    """MotionPut

    :param type_: Type of the supported resources (always `motion` here), defaults to None
    :type type_: str, optional
    :param enabled: true when the sensor is activated, false when deactivated, defaults to None
    :type enabled: bool, optional
    :param sensitivity: sensitivity, defaults to None
    :type sensitivity: MotionPutSensitivity, optional
    """

    def __init__(
        self,
        type_: str = None,
        enabled: bool = None,
        sensitivity: MotionPutSensitivity = None,
    ):
        if type_ is not None:
            self.type_ = type_
        if enabled is not None:
            self.enabled = enabled
        if sensitivity is not None:
            self.sensitivity = self._define_object(sensitivity, MotionPutSensitivity)
