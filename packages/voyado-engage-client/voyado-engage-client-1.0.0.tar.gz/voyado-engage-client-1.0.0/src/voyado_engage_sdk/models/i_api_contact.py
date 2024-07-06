from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .i_api_consent import IApiConsent


@JsonMap({"id_": "id"})
class IApiContact(BaseModel):
    """IApiContact

    :param id_: id_, defaults to None
    :type id_: str, optional
    :param attributes: attributes, defaults to None
    :type attributes: dict, optional
    :param meta: meta, defaults to None
    :type meta: dict, optional
    :param preferences: preferences, defaults to None
    :type preferences: dict, optional
    :param consents: consents, defaults to None
    :type consents: List[IApiConsent], optional
    """

    def __init__(
        self,
        id_: str = None,
        attributes: dict = None,
        meta: dict = None,
        preferences: dict = None,
        consents: List[IApiConsent] = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if attributes is not None:
            self.attributes = attributes
        if meta is not None:
            self.meta = meta
        if preferences is not None:
            self.preferences = preferences
        if consents is not None:
            self.consents = self._define_list(consents, IApiConsent)
