# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import (
    application_variant_report_list_params,
    application_variant_report_create_params,
    application_variant_report_retrieve_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    strip_not_given,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import (
    make_request_options,
)
from ..types.application_variant_report_with_scores_response import ApplicationVariantReportWithScoresResponse
from ..types.application_variant_report_with_scores_response_with_views import (
    ApplicationVariantReportWithScoresResponseWithViews,
)
from ..types.pagination_response_list_pydantic_main_application_variant_report_with_scores_response_with_views import (
    PaginationResponseListPydanticMainApplicationVariantReportWithScoresResponseWithViews,
)

__all__ = ["ApplicationVariantReportsResource", "AsyncApplicationVariantReportsResource"]


class ApplicationVariantReportsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ApplicationVariantReportsResourceWithRawResponse:
        return ApplicationVariantReportsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ApplicationVariantReportsResourceWithStreamingResponse:
        return ApplicationVariantReportsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        application_variant_id: str,
        evaluation_dataset_ids: List[str],
        account_id: str | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVariantReportWithScoresResponse:
        """
        ### Description

        Creates a application variant report

        ### Details

        This API can be used to create a application variant report. To use this API,
        review the request schema and pass in all fields that are required to create a
        application variant report.

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return self._post(
            "/v4/application-variant-reports",
            body=maybe_transform(
                {
                    "application_variant_id": application_variant_id,
                    "evaluation_dataset_ids": evaluation_dataset_ids,
                    "account_id": account_id,
                },
                application_variant_report_create_params.ApplicationVariantReportCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationVariantReportWithScoresResponse,
        )

    def retrieve(
        self,
        application_variant_report_id: str,
        *,
        view: List[Literal["AsyncJobs"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVariantReportWithScoresResponseWithViews:
        """
        ### Description

        Gets the details of a application variant report

        ### Details

        This API can be used to get information about a single application variant
        report by ID. To use this API, pass in the `id` that was returned from your
        Create Application Variant Report API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_report_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_report_id` but received {application_variant_report_id!r}"
            )
        return self._get(
            f"/v4/application-variant-reports/{application_variant_report_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"view": view}, application_variant_report_retrieve_params.ApplicationVariantReportRetrieveParams
                ),
            ),
            cast_to=ApplicationVariantReportWithScoresResponseWithViews,
        )

    def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        application_spec_id: str | NotGiven = NOT_GIVEN,
        application_variant_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        view: List[Literal["AsyncJobs"]] | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaginationResponseListPydanticMainApplicationVariantReportWithScoresResponseWithViews:
        """
        ### Description

        Lists all application variant reports accessible to the user.

        ### Details

        This API can be used to list application variant reports. If a user has access
        to multiple accounts, all application variant reports from all accounts the user
        is associated with will be returned.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return self._get(
            "/v4/application-variant-reports",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "application_spec_id": application_spec_id,
                        "application_variant_id": application_variant_id,
                        "limit": limit,
                        "page": page,
                        "view": view,
                    },
                    application_variant_report_list_params.ApplicationVariantReportListParams,
                ),
            ),
            cast_to=PaginationResponseListPydanticMainApplicationVariantReportWithScoresResponseWithViews,
        )


class AsyncApplicationVariantReportsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncApplicationVariantReportsResourceWithRawResponse:
        return AsyncApplicationVariantReportsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncApplicationVariantReportsResourceWithStreamingResponse:
        return AsyncApplicationVariantReportsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        application_variant_id: str,
        evaluation_dataset_ids: List[str],
        account_id: str | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVariantReportWithScoresResponse:
        """
        ### Description

        Creates a application variant report

        ### Details

        This API can be used to create a application variant report. To use this API,
        review the request schema and pass in all fields that are required to create a
        application variant report.

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return await self._post(
            "/v4/application-variant-reports",
            body=await async_maybe_transform(
                {
                    "application_variant_id": application_variant_id,
                    "evaluation_dataset_ids": evaluation_dataset_ids,
                    "account_id": account_id,
                },
                application_variant_report_create_params.ApplicationVariantReportCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationVariantReportWithScoresResponse,
        )

    async def retrieve(
        self,
        application_variant_report_id: str,
        *,
        view: List[Literal["AsyncJobs"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVariantReportWithScoresResponseWithViews:
        """
        ### Description

        Gets the details of a application variant report

        ### Details

        This API can be used to get information about a single application variant
        report by ID. To use this API, pass in the `id` that was returned from your
        Create Application Variant Report API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_report_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_report_id` but received {application_variant_report_id!r}"
            )
        return await self._get(
            f"/v4/application-variant-reports/{application_variant_report_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"view": view}, application_variant_report_retrieve_params.ApplicationVariantReportRetrieveParams
                ),
            ),
            cast_to=ApplicationVariantReportWithScoresResponseWithViews,
        )

    async def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        application_spec_id: str | NotGiven = NOT_GIVEN,
        application_variant_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        view: List[Literal["AsyncJobs"]] | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaginationResponseListPydanticMainApplicationVariantReportWithScoresResponseWithViews:
        """
        ### Description

        Lists all application variant reports accessible to the user.

        ### Details

        This API can be used to list application variant reports. If a user has access
        to multiple accounts, all application variant reports from all accounts the user
        is associated with will be returned.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return await self._get(
            "/v4/application-variant-reports",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "account_id": account_id,
                        "application_spec_id": application_spec_id,
                        "application_variant_id": application_variant_id,
                        "limit": limit,
                        "page": page,
                        "view": view,
                    },
                    application_variant_report_list_params.ApplicationVariantReportListParams,
                ),
            ),
            cast_to=PaginationResponseListPydanticMainApplicationVariantReportWithScoresResponseWithViews,
        )


class ApplicationVariantReportsResourceWithRawResponse:
    def __init__(self, application_variant_reports: ApplicationVariantReportsResource) -> None:
        self._application_variant_reports = application_variant_reports

        self.create = to_raw_response_wrapper(
            application_variant_reports.create,
        )
        self.retrieve = to_raw_response_wrapper(
            application_variant_reports.retrieve,
        )
        self.list = to_raw_response_wrapper(
            application_variant_reports.list,
        )


class AsyncApplicationVariantReportsResourceWithRawResponse:
    def __init__(self, application_variant_reports: AsyncApplicationVariantReportsResource) -> None:
        self._application_variant_reports = application_variant_reports

        self.create = async_to_raw_response_wrapper(
            application_variant_reports.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            application_variant_reports.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            application_variant_reports.list,
        )


class ApplicationVariantReportsResourceWithStreamingResponse:
    def __init__(self, application_variant_reports: ApplicationVariantReportsResource) -> None:
        self._application_variant_reports = application_variant_reports

        self.create = to_streamed_response_wrapper(
            application_variant_reports.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            application_variant_reports.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            application_variant_reports.list,
        )


class AsyncApplicationVariantReportsResourceWithStreamingResponse:
    def __init__(self, application_variant_reports: AsyncApplicationVariantReportsResource) -> None:
        self._application_variant_reports = application_variant_reports

        self.create = async_to_streamed_response_wrapper(
            application_variant_reports.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            application_variant_reports.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            application_variant_reports.list,
        )
