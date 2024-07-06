from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class CartItemApiModel(BaseModel):
    """Cart item model

    :param sku: Stock keeping unit (article number), defaults to None
    :type sku: str, optional
    :param quantity: Quantity, defaults to None
    :type quantity: int, optional
    """

    def __init__(self, sku: str = None, quantity: int = None):
        if sku is not None:
            self.sku = sku
        if quantity is not None:
            self.quantity = quantity
