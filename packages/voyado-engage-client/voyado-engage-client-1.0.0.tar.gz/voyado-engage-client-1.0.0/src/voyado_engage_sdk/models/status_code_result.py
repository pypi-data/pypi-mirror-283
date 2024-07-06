from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class StatusCode(Enum):
    """An enumeration representing different categories.

    :cvar CONTINUE: "Continue"
    :vartype CONTINUE: str
    :cvar SWITCHINGPROTOCOLS: "SwitchingProtocols"
    :vartype SWITCHINGPROTOCOLS: str
    :cvar OK: "OK"
    :vartype OK: str
    :cvar CREATED: "Created"
    :vartype CREATED: str
    :cvar ACCEPTED: "Accepted"
    :vartype ACCEPTED: str
    :cvar NONAUTHORITATIVEINFORMATION: "NonAuthoritativeInformation"
    :vartype NONAUTHORITATIVEINFORMATION: str
    :cvar NOCONTENT: "NoContent"
    :vartype NOCONTENT: str
    :cvar RESETCONTENT: "ResetContent"
    :vartype RESETCONTENT: str
    :cvar PARTIALCONTENT: "PartialContent"
    :vartype PARTIALCONTENT: str
    :cvar MULTIPLECHOICES: "MultipleChoices"
    :vartype MULTIPLECHOICES: str
    :cvar AMBIGUOUS: "Ambiguous"
    :vartype AMBIGUOUS: str
    :cvar MOVEDPERMANENTLY: "MovedPermanently"
    :vartype MOVEDPERMANENTLY: str
    :cvar MOVED: "Moved"
    :vartype MOVED: str
    :cvar FOUND: "Found"
    :vartype FOUND: str
    :cvar REDIRECT: "Redirect"
    :vartype REDIRECT: str
    :cvar SEEOTHER: "SeeOther"
    :vartype SEEOTHER: str
    :cvar REDIRECTMETHOD: "RedirectMethod"
    :vartype REDIRECTMETHOD: str
    :cvar NOTMODIFIED: "NotModified"
    :vartype NOTMODIFIED: str
    :cvar USEPROXY: "UseProxy"
    :vartype USEPROXY: str
    :cvar UNUSED: "Unused"
    :vartype UNUSED: str
    :cvar TEMPORARYREDIRECT: "TemporaryRedirect"
    :vartype TEMPORARYREDIRECT: str
    :cvar REDIRECTKEEPVERB: "RedirectKeepVerb"
    :vartype REDIRECTKEEPVERB: str
    :cvar BADREQUEST: "BadRequest"
    :vartype BADREQUEST: str
    :cvar UNAUTHORIZED: "Unauthorized"
    :vartype UNAUTHORIZED: str
    :cvar PAYMENTREQUIRED: "PaymentRequired"
    :vartype PAYMENTREQUIRED: str
    :cvar FORBIDDEN: "Forbidden"
    :vartype FORBIDDEN: str
    :cvar NOTFOUND: "NotFound"
    :vartype NOTFOUND: str
    :cvar METHODNOTALLOWED: "MethodNotAllowed"
    :vartype METHODNOTALLOWED: str
    :cvar NOTACCEPTABLE: "NotAcceptable"
    :vartype NOTACCEPTABLE: str
    :cvar PROXYAUTHENTICATIONREQUIRED: "ProxyAuthenticationRequired"
    :vartype PROXYAUTHENTICATIONREQUIRED: str
    :cvar REQUESTTIMEOUT: "RequestTimeout"
    :vartype REQUESTTIMEOUT: str
    :cvar CONFLICT: "Conflict"
    :vartype CONFLICT: str
    :cvar GONE: "Gone"
    :vartype GONE: str
    :cvar LENGTHREQUIRED: "LengthRequired"
    :vartype LENGTHREQUIRED: str
    :cvar PRECONDITIONFAILED: "PreconditionFailed"
    :vartype PRECONDITIONFAILED: str
    :cvar REQUESTENTITYTOOLARGE: "RequestEntityTooLarge"
    :vartype REQUESTENTITYTOOLARGE: str
    :cvar REQUESTURITOOLONG: "RequestUriTooLong"
    :vartype REQUESTURITOOLONG: str
    :cvar UNSUPPORTEDMEDIATYPE: "UnsupportedMediaType"
    :vartype UNSUPPORTEDMEDIATYPE: str
    :cvar REQUESTEDRANGENOTSATISFIABLE: "RequestedRangeNotSatisfiable"
    :vartype REQUESTEDRANGENOTSATISFIABLE: str
    :cvar EXPECTATIONFAILED: "ExpectationFailed"
    :vartype EXPECTATIONFAILED: str
    :cvar UPGRADEREQUIRED: "UpgradeRequired"
    :vartype UPGRADEREQUIRED: str
    :cvar INTERNALSERVERERROR: "InternalServerError"
    :vartype INTERNALSERVERERROR: str
    :cvar NOTIMPLEMENTED: "NotImplemented"
    :vartype NOTIMPLEMENTED: str
    :cvar BADGATEWAY: "BadGateway"
    :vartype BADGATEWAY: str
    :cvar SERVICEUNAVAILABLE: "ServiceUnavailable"
    :vartype SERVICEUNAVAILABLE: str
    :cvar GATEWAYTIMEOUT: "GatewayTimeout"
    :vartype GATEWAYTIMEOUT: str
    :cvar HTTPVERSIONNOTSUPPORTED: "HttpVersionNotSupported"
    :vartype HTTPVERSIONNOTSUPPORTED: str
    """

    CONTINUE = "Continue"
    SWITCHINGPROTOCOLS = "SwitchingProtocols"
    OK = "OK"
    CREATED = "Created"
    ACCEPTED = "Accepted"
    NONAUTHORITATIVEINFORMATION = "NonAuthoritativeInformation"
    NOCONTENT = "NoContent"
    RESETCONTENT = "ResetContent"
    PARTIALCONTENT = "PartialContent"
    MULTIPLECHOICES = "MultipleChoices"
    AMBIGUOUS = "Ambiguous"
    MOVEDPERMANENTLY = "MovedPermanently"
    MOVED = "Moved"
    FOUND = "Found"
    REDIRECT = "Redirect"
    SEEOTHER = "SeeOther"
    REDIRECTMETHOD = "RedirectMethod"
    NOTMODIFIED = "NotModified"
    USEPROXY = "UseProxy"
    UNUSED = "Unused"
    TEMPORARYREDIRECT = "TemporaryRedirect"
    REDIRECTKEEPVERB = "RedirectKeepVerb"
    BADREQUEST = "BadRequest"
    UNAUTHORIZED = "Unauthorized"
    PAYMENTREQUIRED = "PaymentRequired"
    FORBIDDEN = "Forbidden"
    NOTFOUND = "NotFound"
    METHODNOTALLOWED = "MethodNotAllowed"
    NOTACCEPTABLE = "NotAcceptable"
    PROXYAUTHENTICATIONREQUIRED = "ProxyAuthenticationRequired"
    REQUESTTIMEOUT = "RequestTimeout"
    CONFLICT = "Conflict"
    GONE = "Gone"
    LENGTHREQUIRED = "LengthRequired"
    PRECONDITIONFAILED = "PreconditionFailed"
    REQUESTENTITYTOOLARGE = "RequestEntityTooLarge"
    REQUESTURITOOLONG = "RequestUriTooLong"
    UNSUPPORTEDMEDIATYPE = "UnsupportedMediaType"
    REQUESTEDRANGENOTSATISFIABLE = "RequestedRangeNotSatisfiable"
    EXPECTATIONFAILED = "ExpectationFailed"
    UPGRADEREQUIRED = "UpgradeRequired"
    INTERNALSERVERERROR = "InternalServerError"
    NOTIMPLEMENTED = "NotImplemented"
    BADGATEWAY = "BadGateway"
    SERVICEUNAVAILABLE = "ServiceUnavailable"
    GATEWAYTIMEOUT = "GatewayTimeout"
    HTTPVERSIONNOTSUPPORTED = "HttpVersionNotSupported"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, StatusCode._member_map_.values()))


@JsonMap({"status_code": "statusCode"})
class StatusCodeResult(BaseModel):
    """StatusCodeResult

    :param status_code: status_code, defaults to None
    :type status_code: StatusCode, optional
    :param request: request, defaults to None
    :type request: dict, optional
    """

    def __init__(self, status_code: StatusCode = None, request: dict = None):
        if status_code is not None:
            self.status_code = self._enum_matching(
                status_code, StatusCode.list(), "status_code"
            )
        if request is not None:
            self.request = request
