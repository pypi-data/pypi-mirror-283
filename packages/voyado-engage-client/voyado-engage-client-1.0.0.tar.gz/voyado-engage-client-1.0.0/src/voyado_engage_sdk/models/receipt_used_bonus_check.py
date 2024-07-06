from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"check_number": "checkNumber"})
class ReceiptUsedBonusCheck(BaseModel):
    """ReceiptUsedBonusCheck

    :param check_number: check_number, defaults to None
    :type check_number: str, optional
    """

    def __init__(self, check_number: str = None):
        if check_number is not None:
            self.check_number = check_number
