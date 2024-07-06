from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"type_": "type"})
class ReceiptItemDiscount(BaseModel):
    """ReceiptItemDiscount

    :param value: value
    :type value: float
    :param type_: type_, defaults to None
    :type type_: str, optional
    :param description: description, defaults to None
    :type description: str, optional
    """

    def __init__(self, value: float, type_: str = None, description: str = None):
        self.value = value
        if type_ is not None:
            self.type_ = type_
        if description is not None:
            self.description = description
