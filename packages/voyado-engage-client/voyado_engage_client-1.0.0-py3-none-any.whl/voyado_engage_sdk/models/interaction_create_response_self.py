from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"contact_id": "contactId"})
class InteractionCreateResponseSelf(BaseModel):
    """InteractionCreateResponseSelf

    :param contact_id: contact_id, defaults to None
    :type contact_id: str, optional
    :param href: href, defaults to None
    :type href: str, optional
    :param created: created, defaults to None
    :type created: str, optional
    """

    def __init__(self, contact_id: str = None, href: str = None, created: str = None):
        if contact_id is not None:
            self.contact_id = contact_id
        if href is not None:
            self.href = href
        if created is not None:
            self.created = created
