from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"date_": "date", "new_social_security_number": "newSocialSecurityNumber"})
class UnregisteredFromOnlineRegisterInformation(BaseModel):
    """UnregisteredFromOnlineRegisterInformation

    :param reason: reason, defaults to None
    :type reason: str, optional
    :param date_: date_, defaults to None
    :type date_: str, optional
    :param new_social_security_number: new_social_security_number, defaults to None
    :type new_social_security_number: str, optional
    """

    def __init__(
        self,
        reason: str = None,
        date_: str = None,
        new_social_security_number: str = None,
    ):
        if reason is not None:
            self.reason = reason
        if date_ is not None:
            self.date_ = date_
        if new_social_security_number is not None:
            self.new_social_security_number = new_social_security_number
