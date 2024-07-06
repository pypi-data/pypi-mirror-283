from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .receipt_extra_data_item import ReceiptExtraDataItem


@JsonMap({"type_": "type", "extra_data": "extraData"})
class ReceiptPaymentMethod(BaseModel):
    """ReceiptPaymentMethod

    :param type_: type_
    :type type_: str
    :param description: description, defaults to None
    :type description: str, optional
    :param value: value
    :type value: float
    :param extra_data: extra_data, defaults to None
    :type extra_data: List[ReceiptExtraDataItem], optional
    """

    def __init__(
        self,
        type_: str,
        value: float,
        description: str = None,
        extra_data: List[ReceiptExtraDataItem] = None,
    ):
        self.type_ = type_
        if description is not None:
            self.description = description
        self.value = value
        if extra_data is not None:
            self.extra_data = self._define_list(extra_data, ReceiptExtraDataItem)
