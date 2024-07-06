from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap(
    {
        "definition_id": "definitionId",
        "contact_id": "contactId",
        "checkpoint_amount": "checkpointAmount",
    }
)
class ChallengeCheckPointDto(BaseModel):
    """ChallengeCheckPointDto

    :param definition_id: definition_id, defaults to None
    :type definition_id: str, optional
    :param contact_id: contact_id, defaults to None
    :type contact_id: str, optional
    :param checkpoint_amount: checkpoint_amount, defaults to None
    :type checkpoint_amount: int, optional
    """

    def __init__(
        self,
        definition_id: str = None,
        contact_id: str = None,
        checkpoint_amount: int = None,
    ):
        if definition_id is not None:
            self.definition_id = definition_id
        if contact_id is not None:
            self.contact_id = contact_id
        if checkpoint_amount is not None:
            self.checkpoint_amount = checkpoint_amount
