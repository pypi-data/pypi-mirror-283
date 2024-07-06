from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .api_message import ApiMessage


@JsonMap({"total_count": "totalCount"})
class PagedResultOfApiMessage(BaseModel):
    """PagedResultOfApiMessage

    :param items: items, defaults to None
    :type items: List[ApiMessage], optional
    :param total_count: total_count, defaults to None
    :type total_count: int, optional
    :param offset: offset, defaults to None
    :type offset: int, optional
    :param count: count, defaults to None
    :type count: int, optional
    """

    def __init__(
        self,
        items: List[ApiMessage] = None,
        total_count: int = None,
        offset: int = None,
        count: int = None,
    ):
        if items is not None:
            self.items = self._define_list(items, ApiMessage)
        if total_count is not None:
            self.total_count = total_count
        if offset is not None:
            self.offset = offset
        if count is not None:
            self.count = count
