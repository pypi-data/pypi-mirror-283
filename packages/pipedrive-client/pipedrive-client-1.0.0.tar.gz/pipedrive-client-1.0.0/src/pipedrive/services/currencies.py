from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_currencies_ok_response import GetCurrenciesOkResponse


class CurrenciesService(BaseService):

    @cast_models
    def get_currencies(self, term: str = None) -> GetCurrenciesOkResponse:
        """Returns all supported currencies in given account which should be used when saving monetary values with other objects. The `code` parameter of the returning objects is the currency code according to ISO 4217 for all non-custom currencies.

        :param term: Optional search term that is searched for from currency's name and/or code, defaults to None
        :type term: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The list of supported currencies
        :rtype: GetCurrenciesOkResponse
        """

        Validator(str).is_optional().validate(term)

        serialized_request = (
            Serializer(f"{self.base_url}/currencies", self.get_default_headers())
            .add_query("term", term)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetCurrenciesOkResponse._unmap(response)
