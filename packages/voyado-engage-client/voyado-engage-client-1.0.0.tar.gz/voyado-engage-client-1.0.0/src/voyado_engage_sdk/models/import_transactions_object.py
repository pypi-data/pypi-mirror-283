from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class ImportTransactionsObject(BaseModel):
    """ImportTransactionsObject

    :param receipts: receipts, defaults to None
    :type receipts: dict, optional
    """

    def __init__(self, receipts: dict = None):
        if receipts is not None:
            self.receipts = receipts
