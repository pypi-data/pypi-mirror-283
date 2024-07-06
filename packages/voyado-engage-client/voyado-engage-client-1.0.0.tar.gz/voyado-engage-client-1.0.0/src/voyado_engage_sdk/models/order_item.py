from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .order_item_discount import OrderItemDiscount


class OrderItemType(Enum):
    """An enumeration representing different categories.

    :cvar PURCHASE: "PURCHASE"
    :vartype PURCHASE: str
    :cvar RETURN: "RETURN"
    :vartype RETURN: str
    """

    PURCHASE = "PURCHASE"
    RETURN = "RETURN"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, OrderItemType._member_map_.values()))


@JsonMap(
    {
        "type_": "type",
        "gross_paid_price": "grossPaidPrice",
        "gross_paid_price_per_unit": "grossPaidPricePerUnit",
        "tax_amount": "taxAmount",
        "tax_percent": "taxPercent",
        "image_url": "imageUrl",
        "target_url": "targetUrl",
        "extra_data": "extraData",
        "total_discount": "totalDiscount",
        "original_price": "originalPrice",
        "original_price_per_unit": "originalPricePerUnit",
    }
)
class OrderItem(BaseModel):
    """OrderItem

    :param type_: type_
    :type type_: OrderItemType
    :param sku: sku
    :type sku: str
    :param quantity: quantity
    :type quantity: float
    :param gross_paid_price: gross_paid_price
    :type gross_paid_price: float
    :param gross_paid_price_per_unit: gross_paid_price_per_unit, defaults to None
    :type gross_paid_price_per_unit: float, optional
    :param tax_amount: tax_amount, defaults to None
    :type tax_amount: float, optional
    :param tax_percent: tax_percent, defaults to None
    :type tax_percent: float, optional
    :param description: description
    :type description: str
    :param image_url: image_url, defaults to None
    :type image_url: str, optional
    :param target_url: target_url, defaults to None
    :type target_url: str, optional
    :param extra_data: extra_data, defaults to None
    :type extra_data: dict, optional
    :param total_discount: total_discount, defaults to None
    :type total_discount: float, optional
    :param original_price: original_price, defaults to None
    :type original_price: float, optional
    :param original_price_per_unit: original_price_per_unit, defaults to None
    :type original_price_per_unit: float, optional
    :param discounts: discounts, defaults to None
    :type discounts: List[OrderItemDiscount], optional
    :param discounted: discounted, defaults to None
    :type discounted: bool, optional
    """

    def __init__(
        self,
        type_: OrderItemType,
        sku: str,
        quantity: float,
        gross_paid_price: float,
        description: str,
        gross_paid_price_per_unit: float = None,
        tax_amount: float = None,
        tax_percent: float = None,
        image_url: str = None,
        target_url: str = None,
        extra_data: dict = None,
        total_discount: float = None,
        original_price: float = None,
        original_price_per_unit: float = None,
        discounts: List[OrderItemDiscount] = None,
        discounted: bool = None,
    ):
        self.type_ = self._enum_matching(type_, OrderItemType.list(), "type_")
        self.sku = sku
        self.quantity = quantity
        self.gross_paid_price = gross_paid_price
        if gross_paid_price_per_unit is not None:
            self.gross_paid_price_per_unit = gross_paid_price_per_unit
        if tax_amount is not None:
            self.tax_amount = tax_amount
        if tax_percent is not None:
            self.tax_percent = tax_percent
        self.description = description
        if image_url is not None:
            self.image_url = image_url
        if target_url is not None:
            self.target_url = target_url
        if extra_data is not None:
            self.extra_data = extra_data
        if total_discount is not None:
            self.total_discount = total_discount
        if original_price is not None:
            self.original_price = original_price
        if original_price_per_unit is not None:
            self.original_price_per_unit = original_price_per_unit
        if discounts is not None:
            self.discounts = self._define_list(discounts, OrderItemDiscount)
        if discounted is not None:
            self.discounted = discounted
