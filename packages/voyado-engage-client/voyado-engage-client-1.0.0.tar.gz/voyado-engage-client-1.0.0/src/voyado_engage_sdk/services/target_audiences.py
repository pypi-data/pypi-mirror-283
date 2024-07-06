from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.id_name import IdName


class TargetAudiencesService(BaseService):

    @cast_models
    def target_audience_get_target_audiences(self) -> List[IdName]:
        """target_audience_get_target_audiences

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List of all target audiences
        :rtype: List[IdName]
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/target-audiences", self.get_default_headers()
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return [IdName._unmap(item) for item in response]
