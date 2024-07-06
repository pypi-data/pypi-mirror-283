from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class ReceiptExtraDataItem(BaseModel):
    """ReceiptExtraDataItem

    :param name: name, defaults to None
    :type name: str, optional
    :param value: value, defaults to None
    :type value: str, optional
    """

    def __init__(self, name: str = None, value: str = None):
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value
