from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap(
    {
        "message_id": "messageId",
        "send_date_time": "sendDateTime",
        "type_": "type",
        "is_transactional": "isTransactional",
        "message_link": "messageLink",
        "message_text": "messageText",
    }
)
class ApiMessage(BaseModel):
    """ApiMessage

    :param message_id: message_id, defaults to None
    :type message_id: str, optional
    :param name: name, defaults to None
    :type name: str, optional
    :param send_date_time: send_date_time, defaults to None
    :type send_date_time: str, optional
    :param type_: type_, defaults to None
    :type type_: str, optional
    :param source: source, defaults to None
    :type source: str, optional
    :param is_transactional: is_transactional, defaults to None
    :type is_transactional: bool, optional
    :param status: status, defaults to None
    :type status: str, optional
    :param message_link: message_link, defaults to None
    :type message_link: str, optional
    :param message_text: message_text, defaults to None
    :type message_text: str, optional
    """

    def __init__(
        self,
        message_id: str = None,
        name: str = None,
        send_date_time: str = None,
        type_: str = None,
        source: str = None,
        is_transactional: bool = None,
        status: str = None,
        message_link: str = None,
        message_text: str = None,
    ):
        if message_id is not None:
            self.message_id = message_id
        if name is not None:
            self.name = name
        if send_date_time is not None:
            self.send_date_time = send_date_time
        if type_ is not None:
            self.type_ = type_
        if source is not None:
            self.source = source
        if is_transactional is not None:
            self.is_transactional = is_transactional
        if status is not None:
            self.status = status
        if message_link is not None:
            self.message_link = message_link
        if message_text is not None:
            self.message_text = message_text
