from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier
from .product_data import ProductData
from .product_archetype import ProductArchetype


class DeviceGetType(Enum):
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
        return list(map(lambda x: x.value, DeviceGetType._member_map_.values()))


@JsonMap({})
class DeviceGetMetadata(BaseModel):
    """DeviceGetMetadata

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


class UsertestStatus(Enum):
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
        return list(map(lambda x: x.value, UsertestStatus._member_map_.values()))


@JsonMap({})
class DeviceGetUsertest(BaseModel):
    """DeviceGetUsertest

    :param status: status, defaults to None
    :type status: UsertestStatus, optional
    :param usertest: Activates or extends user usertest mode of device for 120 seconds.<br/>`false` deactivates usertest mode.<br/>In usertest mode, devices report changes in state faster and indicate state changes on device LED (if applicable)<br/>, defaults to None
    :type usertest: bool, optional
    """

    def __init__(self, status: UsertestStatus = None, usertest: bool = None):
        if status is not None:
            self.status = self._enum_matching(status, UsertestStatus.list(), "status")
        if usertest is not None:
            self.usertest = usertest


@JsonMap({"type_": "type", "id_": "id"})
class DeviceGet(BaseModel):
    """DeviceGet

    :param type_: type_, defaults to None
    :type type_: DeviceGetType, optional
    :param id_: Unique identifier representing a specific resource instance, defaults to None
    :type id_: str, optional
    :param id_v1: Clip v1 resource identifier, defaults to None
    :type id_v1: str, optional
    :param owner: owner, defaults to None
    :type owner: ResourceIdentifier, optional
    :param product_data: product_data, defaults to None
    :type product_data: ProductData, optional
    :param metadata: metadata, defaults to None
    :type metadata: DeviceGetMetadata, optional
    :param usertest: usertest, defaults to None
    :type usertest: DeviceGetUsertest, optional
    :param services: References all services providing control and state of the device., defaults to None
    :type services: List[ResourceIdentifier], optional
    """

    def __init__(
        self,
        type_: DeviceGetType = None,
        id_: str = None,
        id_v1: str = None,
        owner: ResourceIdentifier = None,
        product_data: ProductData = None,
        metadata: DeviceGetMetadata = None,
        usertest: DeviceGetUsertest = None,
        services: List[ResourceIdentifier] = None,
    ):
        if type_ is not None:
            self.type_ = self._enum_matching(type_, DeviceGetType.list(), "type_")
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
        if product_data is not None:
            self.product_data = self._define_object(product_data, ProductData)
        if metadata is not None:
            self.metadata = self._define_object(metadata, DeviceGetMetadata)
        if usertest is not None:
            self.usertest = self._define_object(usertest, DeviceGetUsertest)
        if services is not None:
            self.services = self._define_list(services, ResourceIdentifier)
