from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class OkResult(BaseModel):
    """OkResult

    :param request: request, defaults to None
    :type request: dict, optional
    """

    def __init__(self, request: dict = None):
        if request is not None:
            self.request = request
