from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id", "date_": "date"})
class ApiAchievementValue(BaseModel):
    """ApiAchievementValue

    :param name: name, defaults to None
    :type name: str, optional
    :param id_: id_, defaults to None
    :type id_: str, optional
    :param date_: date_, defaults to None
    :type date_: str, optional
    """

    def __init__(self, name: str = None, id_: str = None, date_: str = None):
        if name is not None:
            self.name = name
        if id_ is not None:
            self.id_ = id_
        if date_ is not None:
            self.date_ = date_
