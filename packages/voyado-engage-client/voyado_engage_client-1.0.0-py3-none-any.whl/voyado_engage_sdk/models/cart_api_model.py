from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .cart_item_api_model import CartItemApiModel


@JsonMap({"cart_reference": "cartReference", "contact_id": "contactId"})
class CartApiModel(BaseModel):
    """Cart model

    :param cart_reference: Unique cart reference, defaults to None
    :type cart_reference: str, optional
    :param time: Last change date, defaults to None
    :type time: str, optional
    :param contact_id: Contact identifier, defaults to None
    :type contact_id: str, optional
    :param language: Language, defaults to None
    :type language: str, optional
    :param url: Url to cart, defaults to None
    :type url: str, optional
    :param items: Cart items, defaults to None
    :type items: List[CartItemApiModel], optional
    """

    def __init__(
        self,
        cart_reference: str = None,
        time: str = None,
        contact_id: str = None,
        language: str = None,
        url: str = None,
        items: List[CartItemApiModel] = None,
    ):
        if cart_reference is not None:
            self.cart_reference = cart_reference
        if time is not None:
            self.time = time
        if contact_id is not None:
            self.contact_id = contact_id
        if language is not None:
            self.language = language
        if url is not None:
            self.url = url
        if items is not None:
            self.items = self._define_list(items, CartItemApiModel)
