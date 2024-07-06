from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class InteractionSchemaResponseSelf(BaseModel):
    """InteractionSchemaResponseSelf

    :param href: href, defaults to None
    :type href: str, optional
    :param created: created, defaults to None
    :type created: str, optional
    """

    def __init__(self, href: str = None, created: str = None):
        if href is not None:
            self.href = href
        if created is not None:
            self.created = created
