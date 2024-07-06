from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap(
    {
        "country_code": "countryCode",
        "adjacent_zip_codes": "adjacentZipCodes",
        "email_unsubscribe_text": "emailUnsubscribeText",
        "email_view_online_text": "emailViewOnlineText",
        "external_id": "externalId",
        "footer_html": "footerHtml",
        "header_html": "headerHtml",
        "phone_number": "phoneNumber",
        "sender_address": "senderAddress",
        "sender_name": "senderName",
        "type_": "type",
        "zip_code": "zipCode",
        "time_zone": "timeZone",
    }
)
class ApiStore(BaseModel):
    """ApiStore

    :param name: name, defaults to None
    :type name: str, optional
    :param city: city, defaults to None
    :type city: str, optional
    :param country_code: country_code, defaults to None
    :type country_code: str, optional
    :param county: county, defaults to None
    :type county: str, optional
    :param email: email, defaults to None
    :type email: str, optional
    :param adjacent_zip_codes: adjacent_zip_codes, defaults to None
    :type adjacent_zip_codes: str, optional
    :param email_unsubscribe_text: email_unsubscribe_text, defaults to None
    :type email_unsubscribe_text: str, optional
    :param email_view_online_text: email_view_online_text, defaults to None
    :type email_view_online_text: str, optional
    :param external_id: external_id, defaults to None
    :type external_id: str, optional
    :param footer_html: footer_html, defaults to None
    :type footer_html: str, optional
    :param header_html: header_html, defaults to None
    :type header_html: str, optional
    :param homepage: homepage, defaults to None
    :type homepage: str, optional
    :param phone_number: phone_number, defaults to None
    :type phone_number: str, optional
    :param region: region, defaults to None
    :type region: str, optional
    :param sender_address: sender_address, defaults to None
    :type sender_address: str, optional
    :param sender_name: sender_name, defaults to None
    :type sender_name: str, optional
    :param street: street, defaults to None
    :type street: str, optional
    :param type_: type_, defaults to None
    :type type_: str, optional
    :param zip_code: zip_code, defaults to None
    :type zip_code: str, optional
    :param active: active, defaults to None
    :type active: bool, optional
    :param time_zone: time_zone, defaults to None
    :type time_zone: str, optional
    """

    def __init__(
        self,
        name: str = None,
        city: str = None,
        country_code: str = None,
        county: str = None,
        email: str = None,
        adjacent_zip_codes: str = None,
        email_unsubscribe_text: str = None,
        email_view_online_text: str = None,
        external_id: str = None,
        footer_html: str = None,
        header_html: str = None,
        homepage: str = None,
        phone_number: str = None,
        region: str = None,
        sender_address: str = None,
        sender_name: str = None,
        street: str = None,
        type_: str = None,
        zip_code: str = None,
        active: bool = None,
        time_zone: str = None,
    ):
        if name is not None:
            self.name = name
        if city is not None:
            self.city = city
        if country_code is not None:
            self.country_code = country_code
        if county is not None:
            self.county = county
        if email is not None:
            self.email = email
        if adjacent_zip_codes is not None:
            self.adjacent_zip_codes = adjacent_zip_codes
        if email_unsubscribe_text is not None:
            self.email_unsubscribe_text = email_unsubscribe_text
        if email_view_online_text is not None:
            self.email_view_online_text = email_view_online_text
        if external_id is not None:
            self.external_id = external_id
        if footer_html is not None:
            self.footer_html = footer_html
        if header_html is not None:
            self.header_html = header_html
        if homepage is not None:
            self.homepage = homepage
        if phone_number is not None:
            self.phone_number = phone_number
        if region is not None:
            self.region = region
        if sender_address is not None:
            self.sender_address = sender_address
        if sender_name is not None:
            self.sender_name = sender_name
        if street is not None:
            self.street = street
        if type_ is not None:
            self.type_ = type_
        if zip_code is not None:
            self.zip_code = zip_code
        if active is not None:
            self.active = active
        if time_zone is not None:
            self.time_zone = time_zone
