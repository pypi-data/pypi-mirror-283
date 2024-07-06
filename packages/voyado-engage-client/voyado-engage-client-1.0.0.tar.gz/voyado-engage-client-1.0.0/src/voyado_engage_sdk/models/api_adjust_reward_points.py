from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"type_": "type"})
class ApiAdjustRewardPoints(BaseModel):
    """ApiAdjustRewardPoints

    :param points: points
    :type points: float
    :param description: description, defaults to None
    :type description: str, optional
    :param type_: type_, defaults to None
    :type type_: str, optional
    """

    def __init__(self, points: float, description: str = None, type_: str = None):
        self.points = points
        if description is not None:
            self.description = description
        if type_ is not None:
            self.type_ = type_
