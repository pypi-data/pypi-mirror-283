from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap(
    {
        "redeemed_on": "redeemedOn",
        "expires_on": "expiresOn",
        "id_": "id",
        "expire_date_time": "expireDateTime",
        "type_": "type",
    }
)
class AllLoyaltyBarClaimModel(BaseModel):
    """AllLoyaltyBarClaimModel

    :param redeemed_on: redeemed_on, defaults to None
    :type redeemed_on: str, optional
    :param redeemed: redeemed, defaults to None
    :type redeemed: bool, optional
    :param expires_on: expires_on, defaults to None
    :type expires_on: str, optional
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
        redeemed_on: str = None,
        redeemed: bool = None,
        expires_on: str = None,
        id_: str = None,
        description: str = None,
        expire_date_time: str = None,
        type_: str = None,
        value: dict = None,
        name: str = None,
    ):
        if redeemed_on is not None:
            self.redeemed_on = redeemed_on
        if redeemed is not None:
            self.redeemed = redeemed
        if expires_on is not None:
            self.expires_on = expires_on
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
