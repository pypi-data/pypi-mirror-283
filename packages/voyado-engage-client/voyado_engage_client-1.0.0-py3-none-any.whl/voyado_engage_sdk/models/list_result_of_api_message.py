from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .api_message import ApiMessage


@JsonMap({})
class ListResultOfApiMessage(BaseModel):
    """ListResultOfApiMessage

    :param count: count, defaults to None
    :type count: int, optional
    :param items: items, defaults to None
    :type items: List[ApiMessage], optional
    """

    def __init__(self, count: int = None, items: List[ApiMessage] = None):
        if count is not None:
            self.count = count
        if items is not None:
            self.items = self._define_list(items, ApiMessage)
