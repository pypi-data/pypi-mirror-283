from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"status_color": "statusColor", "status_text": "statusText"})
class MemberStatusModel(BaseModel):
    """MemberStatusModel

    :param status_color: status_color, defaults to None
    :type status_color: str, optional
    :param status_text: status_text, defaults to None
    :type status_text: str, optional
    :param data: data, defaults to None
    :type data: dict, optional
    """

    def __init__(
        self, status_color: str = None, status_text: str = None, data: dict = None
    ):
        if status_color is not None:
            self.status_color = status_color
        if status_text is not None:
            self.status_text = status_text
        if data is not None:
            self.data = data
