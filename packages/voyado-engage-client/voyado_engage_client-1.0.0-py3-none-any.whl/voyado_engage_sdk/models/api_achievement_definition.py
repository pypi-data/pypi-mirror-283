from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id", "meta_data": "metaData"})
class ApiAchievementDefinition(BaseModel):
    """ApiAchievementDefinition

    :param name: name, defaults to None
    :type name: str, optional
    :param id_: id_, defaults to None
    :type id_: str, optional
    :param meta_data: meta_data, defaults to None
    :type meta_data: dict, optional
    """

    def __init__(self, name: str = None, id_: str = None, meta_data: dict = None):
        if name is not None:
            self.name = name
        if id_ is not None:
            self.id_ = id_
        if meta_data is not None:
            self.meta_data = meta_data
