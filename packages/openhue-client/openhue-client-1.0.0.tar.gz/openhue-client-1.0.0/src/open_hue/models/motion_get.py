from __future__ import annotations
from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier


@JsonMap({})
class MotionReport(BaseModel):
    """MotionReport

    :param changed: last time the value of this property is changed, defaults to None
    :type changed: str, optional
    :param motion: true if motion is detected, defaults to None
    :type motion: bool, optional
    """

    def __init__(self, changed: str = None, motion: bool = None):
        if changed is not None:
            self.changed = changed
        if motion is not None:
            self.motion = motion


@JsonMap({})
class Motion(BaseModel):
    """Motion

    :param motion: Deprecated. Moved to motion_report/motion., defaults to None
    :type motion: bool, optional
    :param motion_valid: Deprecated. Motion is valid when motion_report property is present, invalid when absent., defaults to None
    :type motion_valid: bool, optional
    :param motion_report: motion_report, defaults to None
    :type motion_report: MotionReport, optional
    """

    def __init__(
        self,
        motion: bool = None,
        motion_valid: bool = None,
        motion_report: MotionReport = None,
    ):
        if motion is not None:
            self.motion = motion
        if motion_valid is not None:
            self.motion_valid = motion_valid
        if motion_report is not None:
            self.motion_report = self._define_object(motion_report, MotionReport)


class SensitivityStatus(Enum):
    """An enumeration representing different categories.

    :cvar SET: "set"
    :vartype SET: str
    :cvar CHANGING: "changing"
    :vartype CHANGING: str
    """

    SET = "set"
    CHANGING = "changing"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SensitivityStatus._member_map_.values()))


@JsonMap({})
class MotionGetSensitivity(BaseModel):
    """MotionGetSensitivity

    :param status: status, defaults to None
    :type status: SensitivityStatus, optional
    :param sensitivity: Sensitivity of the sensor. Value in the range 0 to sensitivity_max, defaults to None
    :type sensitivity: int, optional
    :param sensitivity_max: Maximum value of the sensitivity configuration attribute., defaults to None
    :type sensitivity_max: int, optional
    """

    def __init__(
        self,
        status: SensitivityStatus = None,
        sensitivity: int = None,
        sensitivity_max: int = None,
    ):
        if status is not None:
            self.status = self._enum_matching(
                status, SensitivityStatus.list(), "status"
            )
        if sensitivity is not None:
            self.sensitivity = sensitivity
        if sensitivity_max is not None:
            self.sensitivity_max = sensitivity_max


@JsonMap({"type_": "type", "id_": "id"})
class MotionGet(BaseModel):
    """MotionGet

    :param type_: Type of the supported resources, defaults to None
    :type type_: str, optional
    :param id_: Unique identifier representing a specific resource instance, defaults to None
    :type id_: str, optional
    :param id_v1: Clip v1 resource identifier, defaults to None
    :type id_v1: str, optional
    :param owner: owner, defaults to None
    :type owner: ResourceIdentifier, optional
    :param enabled: ture when the sensor is activated, false when deactivated, defaults to None
    :type enabled: bool, optional
    :param motion: motion, defaults to None
    :type motion: Motion, optional
    :param sensitivity: sensitivity, defaults to None
    :type sensitivity: MotionGetSensitivity, optional
    """

    def __init__(
        self,
        type_: str = None,
        id_: str = None,
        id_v1: str = None,
        owner: ResourceIdentifier = None,
        enabled: bool = None,
        motion: Motion = None,
        sensitivity: MotionGetSensitivity = None,
    ):
        if type_ is not None:
            self.type_ = type_
        if id_ is not None:
            self.id_ = self._pattern_matching(
                id_, "^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$", "id_"
            )
        if id_v1 is not None:
            self.id_v1 = self._pattern_matching(
                id_v1, "^(\/[a-z]{4,32}\/[0-9a-zA-Z-]{1,32})?$", "id_v1"
            )
        if owner is not None:
            self.owner = self._define_object(owner, ResourceIdentifier)
        if enabled is not None:
            self.enabled = enabled
        if motion is not None:
            self.motion = self._define_object(motion, Motion)
        if sensitivity is not None:
            self.sensitivity = self._define_object(sensitivity, MotionGetSensitivity)
