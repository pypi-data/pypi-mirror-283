from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"json_schema": "jsonSchema", "id_": "id", "display_name": "displayName"})
class InteractionSchemaModel(BaseModel):
    """InteractionSchemaModel

    :param json_schema: json_schema, defaults to None
    :type json_schema: dict, optional
    :param id_: id_, defaults to None
    :type id_: str, optional
    :param display_name: display_name, defaults to None
    :type display_name: str, optional
    """

    def __init__(
        self, json_schema: dict = None, id_: str = None, display_name: str = None
    ):
        if json_schema is not None:
            self.json_schema = json_schema
        if id_ is not None:
            self.id_ = id_
        if display_name is not None:
            self.display_name = display_name
