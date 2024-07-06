from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id", "expire_date_time": "expireDateTime", "type_": "type"})
class RedeemedLoyaltyBarClaimModel(BaseModel):
    """RedeemedLoyaltyBarClaimModel

    :param id_: id_, defaults to None
    :type id_: str, optional
    :param description: description, defaults to None
    :type description: str, optional
    :param expire_date_time: expire_date_time, defaults to None
    :type expire_date_time: str, optional
    :param type_: type_, defaults to None
    :type type_: str, optional
    :param value: value, defaults to None
    :type value: dict, optional
    :param name: name, defaults to None
    :type name: str, optional
    """

    def __init__(
        self,
        id_: str = None,
        description: str = None,
        expire_date_time: str = None,
        type_: str = None,
        value: dict = None,
        name: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if description is not None:
            self.description = description
        if expire_date_time is not None:
            self.expire_date_time = expire_date_time
        if type_ is not None:
            self.type_ = type_
        if value is not None:
            self.value = value
        if name is not None:
            self.name = name
