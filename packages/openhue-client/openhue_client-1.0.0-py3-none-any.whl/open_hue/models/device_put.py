from __future__ import annotations
from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel
from .product_archetype import ProductArchetype


class DevicePutType(Enum):
    """An enumeration representing different categories.

    :cvar DEVICE: "device"
    :vartype DEVICE: str
    """

    DEVICE = "device"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, DevicePutType._member_map_.values()))


@JsonMap({})
class DevicePutMetadata(BaseModel):
    """DevicePutMetadata

    :param name: Human readable name of a resource, defaults to None
    :type name: str, optional
    :param archetype: The default archetype given by manufacturer. Can be changed by user., defaults to None
    :type archetype: ProductArchetype, optional
    """

    def __init__(self, name: str = None, archetype: ProductArchetype = None):
        if name is not None:
            self.name = name
        if archetype is not None:
            self.archetype = self._enum_matching(
                archetype, ProductArchetype.list(), "archetype"
            )


class IdentifyAction(Enum):
    """An enumeration representing different categories.

    :cvar IDENTIFY: "identify"
    :vartype IDENTIFY: str
    """

    IDENTIFY = "identify"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, IdentifyAction._member_map_.values()))


@JsonMap({})
class Identify(BaseModel):
    """Identify

    :param action: Triggers a visual identification sequence, current implemented as (which can change in the future):<br/>Bridge performs Zigbee LED identification cycles for 5 seconds Lights perform one breathe cycle Sensors<br/>perform LED identification cycles for 15 seconds<br/>, defaults to None
    :type action: IdentifyAction, optional
    """

    def __init__(self, action: IdentifyAction = None):
        if action is not None:
            self.action = self._enum_matching(action, IdentifyAction.list(), "action")


@JsonMap({})
class DevicePutUsertest(BaseModel):
    """DevicePutUsertest

    :param usertest: Activates or extends user usertest mode of device for 120 seconds.<br/>`false` deactivates usertest mode. In usertest mode, devices report changes in state faster and indicate<br/>state changes on device LED (if applicable)<br/>, defaults to None
    :type usertest: bool, optional
    """

    def __init__(self, usertest: bool = None):
        if usertest is not None:
            self.usertest = usertest


@JsonMap({"type_": "type"})
class DevicePut(BaseModel):
    """DevicePut

    :param type_: type_, defaults to None
    :type type_: DevicePutType, optional
    :param metadata: metadata, defaults to None
    :type metadata: DevicePutMetadata, optional
    :param identify: identify, defaults to None
    :type identify: Identify, optional
    :param usertest: usertest, defaults to None
    :type usertest: DevicePutUsertest, optional
    """

    def __init__(
        self,
        type_: DevicePutType = None,
        metadata: DevicePutMetadata = None,
        identify: Identify = None,
        usertest: DevicePutUsertest = None,
    ):
        if type_ is not None:
            self.type_ = self._enum_matching(type_, DevicePutType.list(), "type_")
        if metadata is not None:
            self.metadata = self._define_object(metadata, DevicePutMetadata)
        if identify is not None:
            self.identify = self._define_object(identify, Identify)
        if usertest is not None:
            self.usertest = self._define_object(usertest, DevicePutUsertest)
