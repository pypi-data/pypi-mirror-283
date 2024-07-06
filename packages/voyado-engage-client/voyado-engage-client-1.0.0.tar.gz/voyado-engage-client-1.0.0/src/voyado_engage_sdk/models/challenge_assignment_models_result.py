from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .i_hypermedia_link import IHypermediaLink
from .challenge_assignment_model import ChallengeAssignmentModel


@JsonMap({"total_count": "totalCount"})
class ChallengeAssignmentModelsResult(BaseModel):
    """ChallengeAssignmentModelsResult

    :param links: links, defaults to None
    :type links: List[IHypermediaLink], optional
    :param items: items, defaults to None
    :type items: List[ChallengeAssignmentModel], optional
    :param total_count: total_count, defaults to None
    :type total_count: int, optional
    :param offset: offset, defaults to None
    :type offset: int, optional
    :param count: count, defaults to None
    :type count: int, optional
    """

    def __init__(
        self,
        links: List[IHypermediaLink] = None,
        items: List[ChallengeAssignmentModel] = None,
        total_count: int = None,
        offset: int = None,
        count: int = None,
    ):
        if links is not None:
            self.links = self._define_list(links, IHypermediaLink)
        if items is not None:
            self.items = self._define_list(items, ChallengeAssignmentModel)
        if total_count is not None:
            self.total_count = total_count
        if offset is not None:
            self.offset = offset
        if count is not None:
            self.count = count
