from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .i_hypermedia_link import IHypermediaLink


@JsonMap({"id_": "id"})
class PointDefinitionModel(BaseModel):
    """PointDefinitionModel

    :param description: description, defaults to None
    :type description: str, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param name: name, defaults to None
    :type name: str, optional
    :param links: links, defaults to None
    :type links: List[IHypermediaLink], optional
    """

    def __init__(
        self,
        description: str = None,
        id_: int = None,
        name: str = None,
        links: List[IHypermediaLink] = None,
    ):
        if description is not None:
            self.description = description
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if links is not None:
            self.links = self._define_list(links, IHypermediaLink)
