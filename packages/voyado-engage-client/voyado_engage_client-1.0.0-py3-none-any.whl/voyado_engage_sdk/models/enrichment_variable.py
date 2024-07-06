from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap(
    {
        "bci_variable_id": "bciVariableId",
        "bci_value": "bciValue",
        "variable_name": "variableName",
    }
)
class EnrichmentVariable(BaseModel):
    """An enrichment value for a certain BCI variable

    :param bci_variable_id: BCI variable identifier, defaults to None
    :type bci_variable_id: str, optional
    :param bci_value: BCI Value, defaults to None
    :type bci_value: str, optional
    :param variable_name: Variable name in Voyado, defaults to None
    :type variable_name: str, optional
    :param value: Mapped value in Voyado, defaults to None
    :type value: str, optional
    :param precision: Value precision from BCI, defaults to None
    :type precision: str, optional
    """

    def __init__(
        self,
        bci_variable_id: str = None,
        bci_value: str = None,
        variable_name: str = None,
        value: str = None,
        precision: str = None,
    ):
        if bci_variable_id is not None:
            self.bci_variable_id = bci_variable_id
        if bci_value is not None:
            self.bci_value = bci_value
        if variable_name is not None:
            self.variable_name = variable_name
        if value is not None:
            self.value = value
        if precision is not None:
            self.precision = precision
