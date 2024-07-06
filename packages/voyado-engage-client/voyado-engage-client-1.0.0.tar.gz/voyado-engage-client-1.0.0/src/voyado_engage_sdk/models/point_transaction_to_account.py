from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap(
    {
        "contact_id": "contactId",
        "definition_id": "definitionId",
        "time_stamp": "timeStamp",
        "valid_from": "validFrom",
        "valid_to": "validTo",
    }
)
class PointTransactionToAccount(BaseModel):
    """PointTransactionToAccount

    :param contact_id: contact_id, defaults to None
    :type contact_id: str, optional
    :param amount: amount, defaults to None
    :type amount: float, optional
    :param definition_id: definition_id, defaults to None
    :type definition_id: int, optional
    :param time_stamp: time_stamp, defaults to None
    :type time_stamp: str, optional
    :param source: source, defaults to None
    :type source: str, optional
    :param description: description, defaults to None
    :type description: str, optional
    :param valid_from: valid_from, defaults to None
    :type valid_from: str, optional
    :param valid_to: valid_to, defaults to None
    :type valid_to: str, optional
    """

    def __init__(
        self,
        contact_id: str = None,
        amount: float = None,
        definition_id: int = None,
        time_stamp: str = None,
        source: str = None,
        description: str = None,
        valid_from: str = None,
        valid_to: str = None,
    ):
        if contact_id is not None:
            self.contact_id = contact_id
        if amount is not None:
            self.amount = amount
        if definition_id is not None:
            self.definition_id = definition_id
        if time_stamp is not None:
            self.time_stamp = time_stamp
        if source is not None:
            self.source = source
        if description is not None:
            self.description = description
        if valid_from is not None:
            self.valid_from = valid_from
        if valid_to is not None:
            self.valid_to = valid_to
