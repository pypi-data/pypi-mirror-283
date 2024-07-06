from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"date_": "date", "id_": "id"})
class IApiConsent(BaseModel):
    """IApiConsent

    :param comment: comment, defaults to None
    :type comment: str, optional
    :param date_: date_, defaults to None
    :type date_: str, optional
    :param id_: id_, defaults to None
    :type id_: str, optional
    :param source: source, defaults to None
    :type source: str, optional
    :param value: value, defaults to None
    :type value: bool, optional
    """

    def __init__(
        self,
        comment: str = None,
        date_: str = None,
        id_: str = None,
        source: str = None,
        value: bool = None,
    ):
        if comment is not None:
            self.comment = comment
        if date_ is not None:
            self.date_ = date_
        if id_ is not None:
            self.id_ = id_
        if source is not None:
            self.source = source
        if value is not None:
            self.value = value
