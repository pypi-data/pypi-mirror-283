from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .available_bonus_check_model import AvailableBonusCheckModel


@JsonMap({"total_count": "totalCount"})
class PagedResultOfAvailableBonusCheckModel(BaseModel):
    """PagedResultOfAvailableBonusCheckModel

    :param items: items, defaults to None
    :type items: List[AvailableBonusCheckModel], optional
    :param total_count: total_count, defaults to None
    :type total_count: int, optional
    :param offset: offset, defaults to None
    :type offset: int, optional
    :param count: count, defaults to None
    :type count: int, optional
    """

    def __init__(
        self,
        items: List[AvailableBonusCheckModel] = None,
        total_count: int = None,
        offset: int = None,
        count: int = None,
    ):
        if items is not None:
            self.items = self._define_list(items, AvailableBonusCheckModel)
        if total_count is not None:
            self.total_count = total_count
        if offset is not None:
            self.offset = offset
        if count is not None:
            self.count = count
