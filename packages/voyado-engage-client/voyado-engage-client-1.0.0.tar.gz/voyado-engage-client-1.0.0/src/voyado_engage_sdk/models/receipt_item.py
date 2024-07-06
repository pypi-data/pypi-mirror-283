from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .receipt_extra_data_item import ReceiptExtraDataItem
from .receipt_item_discount import ReceiptItemDiscount


class ReceiptItemType(Enum):
    """An enumeration representing different categories.

    :cvar PURCHASE: "PURCHASE"
    :vartype PURCHASE: str
    :cvar RETURN: "RETURN"
    :vartype RETURN: str
    :cvar ADJUSTMENT: "ADJUSTMENT"
    :vartype ADJUSTMENT: str
    """

    PURCHASE = "PURCHASE"
    RETURN = "RETURN"
    ADJUSTMENT = "ADJUSTMENT"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ReceiptItemType._member_map_.values()))


@JsonMap(
    {
        "type_": "type",
        "pack_quantity": "packQuantity",
        "gross_paid_price": "grossPaidPrice",
        "tax_amount": "taxAmount",
        "tax_percent": "taxPercent",
        "extra_data": "extraData",
        "article_number": "articleNumber",
        "article_name": "articleName",
        "article_group": "articleGroup",
        "margin_percent": "marginPercent",
        "awards_bonus": "awardsBonus",
    }
)
class ReceiptItem(BaseModel):
    """ReceiptItem

    :param type_: type_
    :type type_: ReceiptItemType
    :param sku: sku
    :type sku: str
    :param quantity: quantity
    :type quantity: int
    :param pack_quantity: pack_quantity, defaults to None
    :type pack_quantity: float, optional
    :param gross_paid_price: gross_paid_price
    :type gross_paid_price: float
    :param tax_amount: tax_amount
    :type tax_amount: float
    :param tax_percent: tax_percent
    :type tax_percent: float
    :param extra_data: extra_data, defaults to None
    :type extra_data: List[ReceiptExtraDataItem], optional
    :param article_number: article_number
    :type article_number: str
    :param article_name: article_name
    :type article_name: str
    :param article_group: article_group, defaults to None
    :type article_group: str, optional
    :param margin_percent: margin_percent, defaults to None
    :type margin_percent: float, optional
    :param awards_bonus: awards_bonus, defaults to None
    :type awards_bonus: bool, optional
    :param discounts: discounts, defaults to None
    :type discounts: List[ReceiptItemDiscount], optional
    """

    def __init__(
        self,
        type_: ReceiptItemType,
        sku: str,
        quantity: int,
        gross_paid_price: float,
        tax_amount: float,
        tax_percent: float,
        article_number: str,
        article_name: str,
        pack_quantity: float = None,
        extra_data: List[ReceiptExtraDataItem] = None,
        article_group: str = None,
        margin_percent: float = None,
        awards_bonus: bool = None,
        discounts: List[ReceiptItemDiscount] = None,
    ):
        self.type_ = self._enum_matching(type_, ReceiptItemType.list(), "type_")
        self.sku = sku
        self.quantity = quantity
        if pack_quantity is not None:
            self.pack_quantity = pack_quantity
        self.gross_paid_price = gross_paid_price
        self.tax_amount = tax_amount
        self.tax_percent = tax_percent
        if extra_data is not None:
            self.extra_data = self._define_list(extra_data, ReceiptExtraDataItem)
        self.article_number = article_number
        self.article_name = article_name
        if article_group is not None:
            self.article_group = article_group
        if margin_percent is not None:
            self.margin_percent = margin_percent
        if awards_bonus is not None:
            self.awards_bonus = awards_bonus
        if discounts is not None:
            self.discounts = self._define_list(discounts, ReceiptItemDiscount)
