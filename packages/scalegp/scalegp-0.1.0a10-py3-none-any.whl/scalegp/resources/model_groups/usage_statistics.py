# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import (
    make_request_options,
)
from ...types.model_groups import usage_statistic_list_params
from ...types.shared.model_usage_response import ModelUsageResponse

__all__ = ["UsageStatisticsResource", "AsyncUsageStatisticsResource"]


class UsageStatisticsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UsageStatisticsResourceWithRawResponse:
        return UsageStatisticsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UsageStatisticsResourceWithStreamingResponse:
        return UsageStatisticsResourceWithStreamingResponse(self)

    def list(
        self,
        model_group_id: str,
        *,
        chunks: int,
        end_date: Union[str, datetime],
        start_date: Union[str, datetime],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelUsageResponse:
        """
        Get Model usage for a group

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_group_id:
            raise ValueError(f"Expected a non-empty value for `model_group_id` but received {model_group_id!r}")
        return self._get(
            f"/v4/model-groups/{model_group_id}/usage-statistics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "chunks": chunks,
                        "end_date": end_date,
                        "start_date": start_date,
                    },
                    usage_statistic_list_params.UsageStatisticListParams,
                ),
            ),
            cast_to=ModelUsageResponse,
        )


class AsyncUsageStatisticsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUsageStatisticsResourceWithRawResponse:
        return AsyncUsageStatisticsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUsageStatisticsResourceWithStreamingResponse:
        return AsyncUsageStatisticsResourceWithStreamingResponse(self)

    async def list(
        self,
        model_group_id: str,
        *,
        chunks: int,
        end_date: Union[str, datetime],
        start_date: Union[str, datetime],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelUsageResponse:
        """
        Get Model usage for a group

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_group_id:
            raise ValueError(f"Expected a non-empty value for `model_group_id` but received {model_group_id!r}")
        return await self._get(
            f"/v4/model-groups/{model_group_id}/usage-statistics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "chunks": chunks,
                        "end_date": end_date,
                        "start_date": start_date,
                    },
                    usage_statistic_list_params.UsageStatisticListParams,
                ),
            ),
            cast_to=ModelUsageResponse,
        )


class UsageStatisticsResourceWithRawResponse:
    def __init__(self, usage_statistics: UsageStatisticsResource) -> None:
        self._usage_statistics = usage_statistics

        self.list = to_raw_response_wrapper(
            usage_statistics.list,
        )


class AsyncUsageStatisticsResourceWithRawResponse:
    def __init__(self, usage_statistics: AsyncUsageStatisticsResource) -> None:
        self._usage_statistics = usage_statistics

        self.list = async_to_raw_response_wrapper(
            usage_statistics.list,
        )


class UsageStatisticsResourceWithStreamingResponse:
    def __init__(self, usage_statistics: UsageStatisticsResource) -> None:
        self._usage_statistics = usage_statistics

        self.list = to_streamed_response_wrapper(
            usage_statistics.list,
        )


class AsyncUsageStatisticsResourceWithStreamingResponse:
    def __init__(self, usage_statistics: AsyncUsageStatisticsResource) -> None:
        self._usage_statistics = usage_statistics

        self.list = async_to_streamed_response_wrapper(
            usage_statistics.list,
        )
