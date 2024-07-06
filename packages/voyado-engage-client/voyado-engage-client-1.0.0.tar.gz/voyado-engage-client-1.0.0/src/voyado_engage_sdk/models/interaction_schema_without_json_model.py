from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id", "display_name": "displayName"})
class InteractionSchemaWithoutJsonModel(BaseModel):
    """InteractionSchemaWithoutJsonModel

    :param id_: id_, defaults to None
    :type id_: str, optional
    :param display_name: display_name, defaults to None
    :type display_name: str, optional
    """

    def __init__(self, id_: str = None, display_name: str = None):
        if id_ is not None:
            self.id_ = id_
        if display_name is not None:
            self.display_name = display_name
