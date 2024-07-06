from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap(
    {
        "expires_on": "expiresOn",
        "id_": "id",
        "check_number": "checkNumber",
        "local_values": "localValues",
        "bonus_points": "bonusPoints",
    }
)
class AvailableBonusCheckModel(BaseModel):
    """AvailableBonusCheckModel

    :param expires_on: expires_on, defaults to None
    :type expires_on: str, optional
    :param id_: id_, defaults to None
    :type id_: str, optional
    :param check_number: check_number, defaults to None
    :type check_number: str, optional
    :param name: name, defaults to None
    :type name: str, optional
    :param value: value, defaults to None
    :type value: dict, optional
    :param local_values: local_values, defaults to None
    :type local_values: List[dict], optional
    :param bonus_points: bonus_points, defaults to None
    :type bonus_points: float, optional
    """

    def __init__(
        self,
        expires_on: str = None,
        id_: str = None,
        check_number: str = None,
        name: str = None,
        value: dict = None,
        local_values: List[dict] = None,
        bonus_points: float = None,
    ):
        if expires_on is not None:
            self.expires_on = expires_on
        if id_ is not None:
            self.id_ = id_
        if check_number is not None:
            self.check_number = check_number
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value
        if local_values is not None:
            self.local_values = local_values
        if bonus_points is not None:
            self.bonus_points = bonus_points
