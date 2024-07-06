from __future__ import annotations
from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel
from .unregistered_from_online_register_information import (
    UnregisteredFromOnlineRegisterInformation,
)


class SearchKey(Enum):
    """An enumeration representing different categories.

    :cvar MOBILEPHONE: "MobilePhone"
    :vartype MOBILEPHONE: str
    :cvar SOCIALSECURITYNUMBER: "SocialSecurityNumber"
    :vartype SOCIALSECURITYNUMBER: str
    """

    MOBILEPHONE = "MobilePhone"
    SOCIALSECURITYNUMBER = "SocialSecurityNumber"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SearchKey._member_map_.values()))


@JsonMap(
    {
        "first_name": "firstName",
        "last_name": "lastName",
        "care_of": "careOf",
        "zip_code": "zipCode",
        "birth_day": "birthDay",
        "phone_number": "phoneNumber",
        "mobile_phone_number": "mobilePhoneNumber",
        "search_key": "searchKey",
        "unregistered_from_online_register_information": "unregisteredFromOnlineRegisterInformation",
    }
)
class ContactSearchResult(BaseModel):
    """ContactSearchResult

    :param first_name: first_name, defaults to None
    :type first_name: str, optional
    :param last_name: last_name, defaults to None
    :type last_name: str, optional
    :param care_of: care_of, defaults to None
    :type care_of: str, optional
    :param street: street, defaults to None
    :type street: str, optional
    :param zip_code: zip_code, defaults to None
    :type zip_code: str, optional
    :param city: city, defaults to None
    :type city: str, optional
    :param birth_day: birth_day, defaults to None
    :type birth_day: str, optional
    :param status: status, defaults to None
    :type status: str, optional
    :param country: country, defaults to None
    :type country: str, optional
    :param phone_number: phone_number, defaults to None
    :type phone_number: str, optional
    :param mobile_phone_number: mobile_phone_number, defaults to None
    :type mobile_phone_number: str, optional
    :param gender: gender, defaults to None
    :type gender: str, optional
    :param search_key: search_key, defaults to None
    :type search_key: SearchKey, optional
    :param unregistered_from_online_register_information: unregistered_from_online_register_information, defaults to None
    :type unregistered_from_online_register_information: UnregisteredFromOnlineRegisterInformation, optional
    """

    def __init__(
        self,
        first_name: str = None,
        last_name: str = None,
        care_of: str = None,
        street: str = None,
        zip_code: str = None,
        city: str = None,
        birth_day: str = None,
        status: str = None,
        country: str = None,
        phone_number: str = None,
        mobile_phone_number: str = None,
        gender: str = None,
        search_key: SearchKey = None,
        unregistered_from_online_register_information: UnregisteredFromOnlineRegisterInformation = None,
    ):
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if care_of is not None:
            self.care_of = care_of
        if street is not None:
            self.street = street
        if zip_code is not None:
            self.zip_code = zip_code
        if city is not None:
            self.city = city
        if birth_day is not None:
            self.birth_day = birth_day
        if status is not None:
            self.status = status
        if country is not None:
            self.country = country
        if phone_number is not None:
            self.phone_number = phone_number
        if mobile_phone_number is not None:
            self.mobile_phone_number = mobile_phone_number
        if gender is not None:
            self.gender = gender
        if search_key is not None:
            self.search_key = self._enum_matching(
                search_key, SearchKey.list(), "search_key"
            )
        if unregistered_from_online_register_information is not None:
            self.unregistered_from_online_register_information = self._define_object(
                unregistered_from_online_register_information,
                UnregisteredFromOnlineRegisterInformation,
            )
