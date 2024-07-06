from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"external_id": "externalId"})
class StockLevelRequest(BaseModel):
    """StockLevelRequest

    :param sku: sku, defaults to None
    :type sku: str, optional
    :param locale: locale, defaults to None
    :type locale: str, optional
    :param quantity: quantity, defaults to None
    :type quantity: int, optional
    :param external_id: external_id, defaults to None
    :type external_id: str, optional
    """

    def __init__(
        self,
        sku: str = None,
        locale: str = None,
        quantity: int = None,
        external_id: str = None,
    ):
        if sku is not None:
            self.sku = sku
        if locale is not None:
            self.locale = locale
        if quantity is not None:
            self.quantity = quantity
        if external_id is not None:
            self.external_id = external_id
