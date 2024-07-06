from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class Unit(Enum):
    """An enumeration representing different categories.

    :cvar MONTHS: "Months"
    :vartype MONTHS: str
    :cvar DAYS: "Days"
    :vartype DAYS: str
    """

    MONTHS = "Months"
    DAYS = "Days"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Unit._member_map_.values()))


@JsonMap({})
class AssignDateRange(BaseModel):
    """The validity time of the promotion set when assignment occured

    :param unit: unit
    :type unit: Unit
    :param amount: amount
    :type amount: int
    """

    def __init__(self, unit: Unit, amount: int):
        self.unit = self._enum_matching(unit, Unit.list(), "unit")
        self.amount = amount
