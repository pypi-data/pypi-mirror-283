from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class BoolRequest(BaseModel):
    """BoolRequest

    :param value: value, defaults to None
    :type value: bool, optional
    """

    def __init__(self, value: bool = None):
        if value is not None:
            self.value = value
