from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class ReceiptContactMatchKeyType(Enum):
    """An enumeration representing different categories.

    :cvar EMAIL: "Email"
    :vartype EMAIL: str
    :cvar SOCIALSECURITYNUMBER: "SocialSecurityNumber"
    :vartype SOCIALSECURITYNUMBER: str
    :cvar MOBILEPHONE: "MobilePhone"
    :vartype MOBILEPHONE: str
    :cvar CARDID: "CardId"
    :vartype CARDID: str
    :cvar EXTERNALID: "ExternalId"
    :vartype EXTERNALID: str
    :cvar MEMBERNUMBER: "MemberNumber"
    :vartype MEMBERNUMBER: str
    :cvar CONTACTID: "ContactId"
    :vartype CONTACTID: str
    :cvar MEMBERNUMBERWITHCARDNUMBERASFALLBACK: "MemberNumberWithCardNumberAsFallback"
    :vartype MEMBERNUMBERWITHCARDNUMBERASFALLBACK: str
    """

    EMAIL = "Email"
    SOCIALSECURITYNUMBER = "SocialSecurityNumber"
    MOBILEPHONE = "MobilePhone"
    CARDID = "CardId"
    EXTERNALID = "ExternalId"
    MEMBERNUMBER = "MemberNumber"
    CONTACTID = "ContactId"
    MEMBERNUMBERWITHCARDNUMBERASFALLBACK = "MemberNumberWithCardNumberAsFallback"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, ReceiptContactMatchKeyType._member_map_.values())
        )


@JsonMap(
    {
        "match_key": "matchKey",
        "match_key_type": "matchKeyType",
        "contact_type": "contactType",
    }
)
class ReceiptContact(BaseModel):
    """ReceiptContact

    :param match_key: match_key
    :type match_key: str
    :param match_key_type: match_key_type
    :type match_key_type: ReceiptContactMatchKeyType
    :param contact_type: contact_type, defaults to None
    :type contact_type: str, optional
    """

    def __init__(
        self,
        match_key: str,
        match_key_type: ReceiptContactMatchKeyType,
        contact_type: str = None,
    ):
        self.match_key = match_key
        self.match_key_type = self._enum_matching(
            match_key_type, ReceiptContactMatchKeyType.list(), "match_key_type"
        )
        if contact_type is not None:
            self.contact_type = contact_type
