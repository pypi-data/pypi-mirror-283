from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .i_hypermedia_link import IHypermediaLink


@JsonMap(
    {
        "balance_expires": "balanceExpires",
        "contact_id": "contactId",
        "definition_id": "definitionId",
        "id_": "id",
        "pending_points": "pendingPoints",
    }
)
class PointAccountModel(BaseModel):
    """PointAccountModel

    :param balance: balance, defaults to None
    :type balance: float, optional
    :param balance_expires: balance_expires, defaults to None
    :type balance_expires: str, optional
    :param contact_id: contact_id, defaults to None
    :type contact_id: str, optional
    :param definition_id: definition_id, defaults to None
    :type definition_id: int, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param pending_points: pending_points, defaults to None
    :type pending_points: float, optional
    :param links: links, defaults to None
    :type links: List[IHypermediaLink], optional
    """

    def __init__(
        self,
        balance: float = None,
        balance_expires: str = None,
        contact_id: str = None,
        definition_id: int = None,
        id_: int = None,
        pending_points: float = None,
        links: List[IHypermediaLink] = None,
    ):
        if balance is not None:
            self.balance = balance
        if balance_expires is not None:
            self.balance_expires = balance_expires
        if contact_id is not None:
            self.contact_id = contact_id
        if definition_id is not None:
            self.definition_id = definition_id
        if id_ is not None:
            self.id_ = id_
        if pending_points is not None:
            self.pending_points = pending_points
        if links is not None:
            self.links = self._define_list(links, IHypermediaLink)
