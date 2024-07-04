# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    strip_not_given,
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
from ...types.evaluation_datasets import (
    evaluation_dataset_version_list_params,
    evaluation_dataset_version_create_params,
)
from ...types.evaluation_datasets.evaluation_dataset_version_response import EvaluationDatasetVersionResponse
from ...types.evaluation_datasets.evaluation_dataset_version_list_response import EvaluationDatasetVersionListResponse

__all__ = ["EvaluationDatasetVersionsResource", "AsyncEvaluationDatasetVersionsResource"]


class EvaluationDatasetVersionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EvaluationDatasetVersionsResourceWithRawResponse:
        return EvaluationDatasetVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluationDatasetVersionsResourceWithStreamingResponse:
        return EvaluationDatasetVersionsResourceWithStreamingResponse(self)

    def create(
        self,
        evaluation_dataset_id: str,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationDatasetVersionResponse:
        """
        ### Description

        Creates a evaluation dataset version

        ### Details

        This API can be used to create a evaluation dataset version. To use this API,
        review the request schema and pass in all fields that are required to create a
        evaluation dataset version.

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return self._post(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions",
            body=maybe_transform(
                {"account_id": account_id},
                evaluation_dataset_version_create_params.EvaluationDatasetVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDatasetVersionResponse,
        )

    def retrieve(
        self,
        evaluation_dataset_version_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationDatasetVersionResponse:
        """
        ### Description

        Gets the details of a evaluation dataset version

        ### Details

        This API can be used to get information about a single evaluation dataset
        version by ID. To use this API, pass in the `id` that was returned from your
        Create Evaluation Dataset Version API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        if not evaluation_dataset_version_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_version_id` but received {evaluation_dataset_version_id!r}"
            )
        return self._get(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions/{evaluation_dataset_version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDatasetVersionResponse,
        )

    def list(
        self,
        evaluation_dataset_id: str,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        include_archived: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationDatasetVersionListResponse:
        """
        ### Description

        Lists all evaluation dataset versions accessible to the user.

        ### Details

        This API can be used to list evaluation dataset versions. If a user has access
        to multiple accounts, all evaluation dataset versions from all accounts the user
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
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return self._get(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                    },
                    evaluation_dataset_version_list_params.EvaluationDatasetVersionListParams,
                ),
            ),
            cast_to=EvaluationDatasetVersionListResponse,
        )


class AsyncEvaluationDatasetVersionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEvaluationDatasetVersionsResourceWithRawResponse:
        return AsyncEvaluationDatasetVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluationDatasetVersionsResourceWithStreamingResponse:
        return AsyncEvaluationDatasetVersionsResourceWithStreamingResponse(self)

    async def create(
        self,
        evaluation_dataset_id: str,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationDatasetVersionResponse:
        """
        ### Description

        Creates a evaluation dataset version

        ### Details

        This API can be used to create a evaluation dataset version. To use this API,
        review the request schema and pass in all fields that are required to create a
        evaluation dataset version.

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return await self._post(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions",
            body=await async_maybe_transform(
                {"account_id": account_id},
                evaluation_dataset_version_create_params.EvaluationDatasetVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDatasetVersionResponse,
        )

    async def retrieve(
        self,
        evaluation_dataset_version_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationDatasetVersionResponse:
        """
        ### Description

        Gets the details of a evaluation dataset version

        ### Details

        This API can be used to get information about a single evaluation dataset
        version by ID. To use this API, pass in the `id` that was returned from your
        Create Evaluation Dataset Version API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        if not evaluation_dataset_version_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_version_id` but received {evaluation_dataset_version_id!r}"
            )
        return await self._get(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions/{evaluation_dataset_version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDatasetVersionResponse,
        )

    async def list(
        self,
        evaluation_dataset_id: str,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        include_archived: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationDatasetVersionListResponse:
        """
        ### Description

        Lists all evaluation dataset versions accessible to the user.

        ### Details

        This API can be used to list evaluation dataset versions. If a user has access
        to multiple accounts, all evaluation dataset versions from all accounts the user
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
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return await self._get(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "account_id": account_id,
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                    },
                    evaluation_dataset_version_list_params.EvaluationDatasetVersionListParams,
                ),
            ),
            cast_to=EvaluationDatasetVersionListResponse,
        )


class EvaluationDatasetVersionsResourceWithRawResponse:
    def __init__(self, evaluation_dataset_versions: EvaluationDatasetVersionsResource) -> None:
        self._evaluation_dataset_versions = evaluation_dataset_versions

        self.create = to_raw_response_wrapper(
            evaluation_dataset_versions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            evaluation_dataset_versions.retrieve,
        )
        self.list = to_raw_response_wrapper(
            evaluation_dataset_versions.list,
        )


class AsyncEvaluationDatasetVersionsResourceWithRawResponse:
    def __init__(self, evaluation_dataset_versions: AsyncEvaluationDatasetVersionsResource) -> None:
        self._evaluation_dataset_versions = evaluation_dataset_versions

        self.create = async_to_raw_response_wrapper(
            evaluation_dataset_versions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            evaluation_dataset_versions.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            evaluation_dataset_versions.list,
        )


class EvaluationDatasetVersionsResourceWithStreamingResponse:
    def __init__(self, evaluation_dataset_versions: EvaluationDatasetVersionsResource) -> None:
        self._evaluation_dataset_versions = evaluation_dataset_versions

        self.create = to_streamed_response_wrapper(
            evaluation_dataset_versions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            evaluation_dataset_versions.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            evaluation_dataset_versions.list,
        )


class AsyncEvaluationDatasetVersionsResourceWithStreamingResponse:
    def __init__(self, evaluation_dataset_versions: AsyncEvaluationDatasetVersionsResource) -> None:
        self._evaluation_dataset_versions = evaluation_dataset_versions

        self.create = async_to_streamed_response_wrapper(
            evaluation_dataset_versions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            evaluation_dataset_versions.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            evaluation_dataset_versions.list,
        )
