from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .hypermedia_link import HypermediaLink
from .interaction_model import InteractionModel


@JsonMap({})
class InteractionPage(BaseModel):
    """InteractionPage

    :param links: links, defaults to None
    :type links: List[HypermediaLink], optional
    :param items: items, defaults to None
    :type items: List[InteractionModel], optional
    """

    def __init__(
        self, links: List[HypermediaLink] = None, items: List[InteractionModel] = None
    ):
        if links is not None:
            self.links = self._define_list(links, HypermediaLink)
        if items is not None:
            self.items = self._define_list(items, InteractionModel)
