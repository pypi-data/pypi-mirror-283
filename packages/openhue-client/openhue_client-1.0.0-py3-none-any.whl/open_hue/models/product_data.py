from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .product_archetype import ProductArchetype


@JsonMap({})
class ProductData(BaseModel):
    """ProductData

    :param model_id: Unique identification of device model, defaults to None
    :type model_id: str, optional
    :param manufacturer_name: Name of device manufacturer, defaults to None
    :type manufacturer_name: str, optional
    :param product_name: Name of the product, defaults to None
    :type product_name: str, optional
    :param product_archetype: The default archetype given by manufacturer. Can be changed by user., defaults to None
    :type product_archetype: ProductArchetype, optional
    :param certified: This device is Hue certified, defaults to None
    :type certified: bool, optional
    :param software_version: Software version of the product, defaults to None
    :type software_version: str, optional
    :param hardware_platform_type: Hardware type; identified by Manufacturer code and ImageType, defaults to None
    :type hardware_platform_type: str, optional
    """

    def __init__(
        self,
        model_id: str = None,
        manufacturer_name: str = None,
        product_name: str = None,
        product_archetype: ProductArchetype = None,
        certified: bool = None,
        software_version: str = None,
        hardware_platform_type: str = None,
    ):
        if model_id is not None:
            self.model_id = model_id
        if manufacturer_name is not None:
            self.manufacturer_name = manufacturer_name
        if product_name is not None:
            self.product_name = product_name
        if product_archetype is not None:
            self.product_archetype = self._enum_matching(
                product_archetype, ProductArchetype.list(), "product_archetype"
            )
        if certified is not None:
            self.certified = certified
        if software_version is not None:
            self.software_version = self._pattern_matching(
                software_version, "\d+\.\d+\.\d+", "software_version"
            )
        if hardware_platform_type is not None:
            self.hardware_platform_type = hardware_platform_type
