from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class IHypermediaLink(BaseModel):
    """IHypermediaLink

    :param href: href, defaults to None
    :type href: str, optional
    :param method: method, defaults to None
    :type method: str, optional
    :param rel: rel, defaults to None
    :type rel: str, optional
    """

    def __init__(self, href: str = None, method: str = None, rel: str = None):
        if href is not None:
            self.href = href
        if method is not None:
            self.method = method
        if rel is not None:
            self.rel = rel
