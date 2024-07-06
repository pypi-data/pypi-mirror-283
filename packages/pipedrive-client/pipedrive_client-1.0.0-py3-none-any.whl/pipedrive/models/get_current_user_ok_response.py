from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class AccessApp6(Enum):
    """An enumeration representing different categories.

    :cvar SALES: "sales"
    :vartype SALES: str
    :cvar PROJECTS: "projects"
    :vartype PROJECTS: str
    :cvar CAMPAIGNS: "campaigns"
    :vartype CAMPAIGNS: str
    :cvar GLOBAL: "global"
    :vartype GLOBAL: str
    :cvar ACCOUNT_SETTINGS: "account_settings"
    :vartype ACCOUNT_SETTINGS: str
    """

    SALES = "sales"
    PROJECTS = "projects"
    CAMPAIGNS = "campaigns"
    GLOBAL = "global"
    ACCOUNT_SETTINGS = "account_settings"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, AccessApp6._member_map_.values()))


@JsonMap({})
class DataAccess5(BaseModel):
    """DataAccess5

    :param app: app, defaults to None
    :type app: AccessApp6, optional
    :param admin: admin, defaults to None
    :type admin: bool, optional
    :param permission_set_id: permission_set_id, defaults to None
    :type permission_set_id: str, optional
    """

    def __init__(
        self, app: AccessApp6 = None, admin: bool = None, permission_set_id: str = None
    ):
        if app is not None:
            self.app = self._enum_matching(app, AccessApp6.list(), "app")
        if admin is not None:
            self.admin = admin
        if permission_set_id is not None:
            self.permission_set_id = permission_set_id


@JsonMap({})
class Language(BaseModel):
    """The user language details

    :param language_code: The language code. E.g. en, defaults to None
    :type language_code: str, optional
    :param country_code: The country code. E.g. US, defaults to None
    :type country_code: str, optional
    """

    def __init__(self, language_code: str = None, country_code: str = None):
        if language_code is not None:
            self.language_code = language_code
        if country_code is not None:
            self.country_code = country_code


@JsonMap({"id_": "id"})
class GetCurrentUserOkResponseData(BaseModel):
    """GetCurrentUserOkResponseData

    :param id_: The user ID, defaults to None
    :type id_: int, optional
    :param name: The user name, defaults to None
    :type name: str, optional
    :param default_currency: The user default currency, defaults to None
    :type default_currency: str, optional
    :param locale: The user locale, defaults to None
    :type locale: str, optional
    :param lang: The user language ID, defaults to None
    :type lang: int, optional
    :param email: The user email, defaults to None
    :type email: str, optional
    :param phone: The user phone, defaults to None
    :type phone: str, optional
    :param activated: Boolean that indicates whether the user is activated, defaults to None
    :type activated: bool, optional
    :param last_login: The last login date and time of the user. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type last_login: str, optional
    :param created: The creation date and time of the user. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type created: str, optional
    :param modified: The last modification date and time of the user. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type modified: str, optional
    :param has_created_company: Boolean that indicates whether the user has created a company, defaults to None
    :type has_created_company: bool, optional
    :param access: access, defaults to None
    :type access: List[DataAccess5], optional
    :param active_flag: Boolean that indicates whether the user is activated, defaults to None
    :type active_flag: bool, optional
    :param timezone_name: The user timezone name, defaults to None
    :type timezone_name: str, optional
    :param timezone_offset: The user timezone offset, defaults to None
    :type timezone_offset: str, optional
    :param role_id: The ID of the user role, defaults to None
    :type role_id: int, optional
    :param icon_url: The user icon URL, defaults to None
    :type icon_url: str, optional
    :param is_you: Boolean that indicates if the requested user is the same which is logged in (in this case, always true), defaults to None
    :type is_you: bool, optional
    :param is_deleted: Boolean that indicates whether the user is deleted from the company, defaults to None
    :type is_deleted: bool, optional
    :param company_id: The user company ID, defaults to None
    :type company_id: int, optional
    :param company_name: The user company name, defaults to None
    :type company_name: str, optional
    :param company_domain: The user company domain, defaults to None
    :type company_domain: str, optional
    :param company_country: The user company country, defaults to None
    :type company_country: str, optional
    :param company_industry: The user company industry, defaults to None
    :type company_industry: str, optional
    :param language: The user language details, defaults to None
    :type language: Language, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        default_currency: str = None,
        locale: str = None,
        lang: int = None,
        email: str = None,
        phone: str = None,
        activated: bool = None,
        last_login: str = None,
        created: str = None,
        modified: str = None,
        has_created_company: bool = None,
        access: List[DataAccess5] = None,
        active_flag: bool = None,
        timezone_name: str = None,
        timezone_offset: str = None,
        role_id: int = None,
        icon_url: str = None,
        is_you: bool = None,
        is_deleted: bool = None,
        company_id: int = None,
        company_name: str = None,
        company_domain: str = None,
        company_country: str = None,
        company_industry: str = None,
        language: Language = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if default_currency is not None:
            self.default_currency = default_currency
        if locale is not None:
            self.locale = locale
        if lang is not None:
            self.lang = lang
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if activated is not None:
            self.activated = activated
        if last_login is not None:
            self.last_login = last_login
        if created is not None:
            self.created = created
        if modified is not None:
            self.modified = modified
        if has_created_company is not None:
            self.has_created_company = has_created_company
        if access is not None:
            self.access = self._define_list(access, DataAccess5)
        if active_flag is not None:
            self.active_flag = active_flag
        if timezone_name is not None:
            self.timezone_name = timezone_name
        if timezone_offset is not None:
            self.timezone_offset = timezone_offset
        if role_id is not None:
            self.role_id = role_id
        if icon_url is not None:
            self.icon_url = icon_url
        if is_you is not None:
            self.is_you = is_you
        if is_deleted is not None:
            self.is_deleted = is_deleted
        if company_id is not None:
            self.company_id = company_id
        if company_name is not None:
            self.company_name = company_name
        if company_domain is not None:
            self.company_domain = company_domain
        if company_country is not None:
            self.company_country = company_country
        if company_industry is not None:
            self.company_industry = company_industry
        if language is not None:
            self.language = self._define_object(language, Language)


@JsonMap({})
class GetCurrentUserOkResponse(BaseModel):
    """GetCurrentUserOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: GetCurrentUserOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: GetCurrentUserOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetCurrentUserOkResponseData)
