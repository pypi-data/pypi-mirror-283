from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.share_type import ShareType
from ..models.get_viewed_period_json_period import GetViewedPeriodJsonPeriod
from ..models.get_viewed_period_json_ok_response import GetViewedPeriodJsonOkResponse
from ..models.get_shared_period_json_period import GetSharedPeriodJsonPeriod
from ..models.get_shared_period_json_ok_response import GetSharedPeriodJsonOkResponse
from ..models.get_shared_by_period_share_type_json_period import (
    GetSharedByPeriodShareTypeJsonPeriod,
)
from ..models.get_shared_by_period_share_type_json_ok_response import (
    GetSharedByPeriodShareTypeJsonOkResponse,
)
from ..models.get_emailed_period_json_period import GetEmailedPeriodJsonPeriod
from ..models.get_emailed_period_json_ok_response import GetEmailedPeriodJsonOkResponse


class MostPopularService(BaseService):

    @cast_models
    def get_emailed_period_json(
        self, period: GetEmailedPeriodJsonPeriod
    ) -> GetEmailedPeriodJsonOkResponse:
        """Returns an array of the most emailed articles on NYTimes.com for specified period of time (1 day, 7 days, or 30 days).

        :param period: Time period: 1, 7, or 30 days.
        :type period: GetEmailedPeriodJsonPeriod
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: An array of articles.
        :rtype: GetEmailedPeriodJsonOkResponse
        """

        Validator(GetEmailedPeriodJsonPeriod).validate(period)

        serialized_request = (
            Serializer(
                f"{self.base_url}/emailed/{{period}}.json", self.get_default_headers()
            )
            .add_path("period", period)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetEmailedPeriodJsonOkResponse._unmap(response)

    @cast_models
    def get_shared_period_json(
        self, period: GetSharedPeriodJsonPeriod
    ) -> GetSharedPeriodJsonOkResponse:
        """Returns an array of the most shared articles on NYTimes.com for specified period of time (1 day, 7 days, or 30 days).

        :param period: Time period: 1, 7, or 30 days.
        :type period: GetSharedPeriodJsonPeriod
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: An array of articles.
        :rtype: GetSharedPeriodJsonOkResponse
        """

        Validator(GetSharedPeriodJsonPeriod).validate(period)

        serialized_request = (
            Serializer(
                f"{self.base_url}/shared/{{period}}.json", self.get_default_headers()
            )
            .add_path("period", period)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetSharedPeriodJsonOkResponse._unmap(response)

    @cast_models
    def get_shared_by_period_share_type_json(
        self, period: GetSharedByPeriodShareTypeJsonPeriod, share_type: ShareType
    ) -> GetSharedByPeriodShareTypeJsonOkResponse:
        """Returns an array of the most shared articles by share type on NYTimes.com for specified period of time (1 day, 7 days, or 30 days).

        :param period: Time period: 1, 7, or 30 days.
        :type period: GetSharedByPeriodShareTypeJsonPeriod
        :param share_type: Share type: facebook.
        :type share_type: ShareType
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: An array of articles.
        :rtype: GetSharedByPeriodShareTypeJsonOkResponse
        """

        Validator(GetSharedByPeriodShareTypeJsonPeriod).validate(period)
        Validator(ShareType).validate(share_type)

        serialized_request = (
            Serializer(
                f"{self.base_url}/shared/{{period}}/{{share_type}}.json",
                self.get_default_headers(),
            )
            .add_path("period", period)
            .add_path("share_type", share_type)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetSharedByPeriodShareTypeJsonOkResponse._unmap(response)

    @cast_models
    def get_viewed_period_json(
        self, period: GetViewedPeriodJsonPeriod
    ) -> GetViewedPeriodJsonOkResponse:
        """Returns an array of the most viewed articles on NYTimes.com for specified period of time (1 day, 7 days, or 30 days).

        :param period: Time period: 1, 7, or 30 days.
        :type period: GetViewedPeriodJsonPeriod
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: An array of articles.
        :rtype: GetViewedPeriodJsonOkResponse
        """

        Validator(GetViewedPeriodJsonPeriod).validate(period)

        serialized_request = (
            Serializer(
                f"{self.base_url}/viewed/{{period}}.json", self.get_default_headers()
            )
            .add_path("period", period)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetViewedPeriodJsonOkResponse._unmap(response)
