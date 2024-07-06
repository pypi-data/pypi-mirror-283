from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"contact_id": "contactId", "external_id": "externalId"})
class SubscriptionRequest(BaseModel):
    """SubscriptionRequest

    :param contact_id: contact_id, defaults to None
    :type contact_id: str, optional
    :param sku: sku, defaults to None
    :type sku: str, optional
    :param locale: locale, defaults to None
    :type locale: str, optional
    :param external_id: external_id, defaults to None
    :type external_id: str, optional
    """

    def __init__(
        self,
        contact_id: str = None,
        sku: str = None,
        locale: str = None,
        external_id: str = None,
    ):
        if contact_id is not None:
            self.contact_id = contact_id
        if sku is not None:
            self.sku = sku
        if locale is not None:
            self.locale = locale
        if external_id is not None:
            self.external_id = external_id
