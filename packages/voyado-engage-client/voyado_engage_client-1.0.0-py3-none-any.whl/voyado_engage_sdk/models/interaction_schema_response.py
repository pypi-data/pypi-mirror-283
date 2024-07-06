from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .interaction_schema_response_self import InteractionSchemaResponseSelf


@JsonMap({"id_": "id", "self_": "self"})
class InteractionSchemaResponse(BaseModel):
    """InteractionSchemaResponse

    :param id_: id_, defaults to None
    :type id_: str, optional
    :param self_: self_, defaults to None
    :type self_: InteractionSchemaResponseSelf, optional
    """

    def __init__(self, id_: str = None, self_: InteractionSchemaResponseSelf = None):
        if id_ is not None:
            self.id_ = id_
        if self_ is not None:
            self.self_ = self._define_object(self_, InteractionSchemaResponseSelf)
