from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .utm import Utm


@JsonMap(
    {
        "item_id": "itemId",
        "contact_id": "contactId",
        "session_id": "sessionId",
        "new_session": "newSession",
        "external_referrer": "externalReferrer",
    }
)
class ProductViewApiModel(BaseModel):
    """ProductViewApiModel

    :param item_id: item_id
    :type item_id: str
    :param category: category, defaults to None
    :type category: str, optional
    :param time: time, defaults to None
    :type time: str, optional
    :param contact_id: contact_id
    :type contact_id: str
    :param session_id: session_id, defaults to None
    :type session_id: str, optional
    :param new_session: new_session, defaults to None
    :type new_session: bool, optional
    :param language: language, defaults to None
    :type language: str, optional
    :param url: url, defaults to None
    :type url: str, optional
    :param external_referrer: external_referrer, defaults to None
    :type external_referrer: str, optional
    :param utm: utm, defaults to None
    :type utm: List[Utm], optional
    """

    def __init__(
        self,
        item_id: str,
        contact_id: str,
        category: str = None,
        time: str = None,
        session_id: str = None,
        new_session: bool = None,
        language: str = None,
        url: str = None,
        external_referrer: str = None,
        utm: List[Utm] = None,
    ):
        self.item_id = item_id
        if category is not None:
            self.category = category
        if time is not None:
            self.time = time
        self.contact_id = contact_id
        if session_id is not None:
            self.session_id = session_id
        if new_session is not None:
            self.new_session = new_session
        if language is not None:
            self.language = language
        if url is not None:
            self.url = url
        if external_referrer is not None:
            self.external_referrer = external_referrer
        if utm is not None:
            self.utm = self._define_list(utm, Utm)
