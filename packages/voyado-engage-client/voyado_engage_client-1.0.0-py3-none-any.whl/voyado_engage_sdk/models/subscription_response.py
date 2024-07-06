from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap(
    {
        "id_": "id",
        "contact_id": "contactId",
        "external_id": "externalId",
        "created_on": "createdOn",
    }
)
class SubscriptionResponse(BaseModel):
    """SubscriptionResponse

    :param id_: id_, defaults to None
    :type id_: str, optional
    :param contact_id: contact_id, defaults to None
    :type contact_id: str, optional
    :param sku: sku, defaults to None
    :type sku: str, optional
    :param locale: locale, defaults to None
    :type locale: str, optional
    :param external_id: external_id, defaults to None
    :type external_id: str, optional
    :param created_on: created_on, defaults to None
    :type created_on: str, optional
    """

    def __init__(
        self,
        id_: str = None,
        contact_id: str = None,
        sku: str = None,
        locale: str = None,
        external_id: str = None,
        created_on: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if contact_id is not None:
            self.contact_id = contact_id
        if sku is not None:
            self.sku = sku
        if locale is not None:
            self.locale = locale
        if external_id is not None:
            self.external_id = external_id
        if created_on is not None:
            self.created_on = created_on
