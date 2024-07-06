from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap(
    {
        "id_": "id",
        "contact_id": "contactId",
        "schema_id": "schemaId",
        "created_date": "createdDate",
    }
)
class InteractionModel(BaseModel):
    """InteractionModel

    :param id_: id_, defaults to None
    :type id_: str, optional
    :param contact_id: contact_id, defaults to None
    :type contact_id: str, optional
    :param schema_id: schema_id, defaults to None
    :type schema_id: str, optional
    :param created_date: created_date, defaults to None
    :type created_date: str, optional
    :param payload: payload, defaults to None
    :type payload: dict, optional
    """

    def __init__(
        self,
        id_: str = None,
        contact_id: str = None,
        schema_id: str = None,
        created_date: str = None,
        payload: dict = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if contact_id is not None:
            self.contact_id = contact_id
        if schema_id is not None:
            self.schema_id = schema_id
        if created_date is not None:
            self.created_date = created_date
        if payload is not None:
            self.payload = payload
