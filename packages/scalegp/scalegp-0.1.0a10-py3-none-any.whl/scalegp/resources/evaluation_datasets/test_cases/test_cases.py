# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, overload
from typing_extensions import Literal

import httpx

from .history import (
    HistoryResource,
    AsyncHistoryResource,
    HistoryResourceWithRawResponse,
    AsyncHistoryResourceWithRawResponse,
    HistoryResourceWithStreamingResponse,
    AsyncHistoryResourceWithStreamingResponse,
)
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    required_args,
    maybe_transform,
    strip_not_given,
    async_maybe_transform,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import (
    make_request_options,
)
from ....types.evaluation_datasets import (
    test_case_list_params,
    test_case_batch_params,
    test_case_create_params,
    test_case_update_params,
)
from ....types.shared.delete_response import DeleteResponse
from ....types.shared.test_case_version_response import TestCaseVersionResponse
from ....types.evaluation_datasets.test_case_list_response import TestCaseListResponse
from ....types.evaluation_datasets.test_case_batch_response import TestCaseBatchResponse

__all__ = ["TestCasesResource", "AsyncTestCasesResource"]


class TestCasesResource(SyncAPIResource):
    __test__ = False

    @cached_property
    def history(self) -> HistoryResource:
        return HistoryResource(self._client)

    @cached_property
    def with_raw_response(self) -> TestCasesResourceWithRawResponse:
        return TestCasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TestCasesResourceWithStreamingResponse:
        return TestCasesResourceWithStreamingResponse(self)

    def create(
        self,
        evaluation_dataset_id: str,
        *,
        schema_type: Literal["GENERATION"],
        test_case_data: object,
        account_id: str | NotGiven = NOT_GIVEN,
        chat_history: object | NotGiven = NOT_GIVEN,
        test_case_metadata: object | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseVersionResponse:
        """
        ### Description

        Create a test case for a selected dataset.

        Args:
          schema_type: An enumeration.

          test_case_data: The data for the test case in a format matching the provided schema_type

          account_id: The ID of the account that owns the given entity.

          chat_history: Used for tracking previous chat interactions for multi-chat test cases

          test_case_metadata: Metadata for the test case

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
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases",
            body=maybe_transform(
                {
                    "schema_type": schema_type,
                    "test_case_data": test_case_data,
                    "account_id": account_id,
                    "chat_history": chat_history,
                    "test_case_metadata": test_case_metadata,
                },
                test_case_create_params.TestCaseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseVersionResponse,
        )

    def retrieve(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseVersionResponse:
        """
        ### Description

        Get the test case by its id.

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
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return self._get(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseVersionResponse,
        )

    @overload
    def update(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        chat_history: object | NotGiven = NOT_GIVEN,
        restore: Literal[False] | NotGiven = NOT_GIVEN,
        schema_type: Literal["GENERATION"] | NotGiven = NOT_GIVEN,
        test_case_data: object | NotGiven = NOT_GIVEN,
        test_case_metadata: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseVersionResponse:
        """
        ### Description

        Update a test case.

        Args:
          chat_history: Used for tracking previous chat interactions for multi-chat test cases

          restore: Set to true to restore the entity from the database.

          schema_type: An enumeration.

          test_case_data: The data for the test case in a format matching the provided schema_type

          test_case_metadata: Metadata for the test case

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def update(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseVersionResponse:
        """
        ### Description

        Update a test case.

        Args:
          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["evaluation_dataset_id"], ["evaluation_dataset_id", "restore"])
    def update(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        chat_history: object | NotGiven = NOT_GIVEN,
        restore: Literal[False] | Literal[True] | NotGiven = NOT_GIVEN,
        schema_type: Literal["GENERATION"] | NotGiven = NOT_GIVEN,
        test_case_data: object | NotGiven = NOT_GIVEN,
        test_case_metadata: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseVersionResponse:
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return self._patch(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}",
            body=maybe_transform(
                {
                    "chat_history": chat_history,
                    "restore": restore,
                    "schema_type": schema_type,
                    "test_case_data": test_case_data,
                    "test_case_metadata": test_case_metadata,
                },
                test_case_update_params.TestCaseUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseVersionResponse,
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
    ) -> TestCaseListResponse:
        """
        ### Description

        List all test cases for a selected dataset.

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
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases",
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
                    test_case_list_params.TestCaseListParams,
                ),
            ),
            cast_to=TestCaseListResponse,
        )

    def delete(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteResponse:
        """
        ### Description

        Delete a specified test case -- retaining older version belonging to older
        dataset versions.

        ### Details

        This request shouldn't be used when deleting due to compliance reasons. See Wipe
        action.

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
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return self._delete(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    def batch(
        self,
        evaluation_dataset_id: str,
        *,
        body: Iterable[test_case_batch_params.Body],
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseBatchResponse:
        """
        ### Description

        Creates a batch of test cases

        ### Details

        This API can be used to create multiple test cases so users do not have to the
        incur the cost of repeated network calls. To use this API, pass in a list of
        test cases in the request body.

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
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return self._post(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/batch",
            body=maybe_transform(body, test_case_batch_params.TestCaseBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseBatchResponse,
        )


class AsyncTestCasesResource(AsyncAPIResource):
    @cached_property
    def history(self) -> AsyncHistoryResource:
        return AsyncHistoryResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTestCasesResourceWithRawResponse:
        return AsyncTestCasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTestCasesResourceWithStreamingResponse:
        return AsyncTestCasesResourceWithStreamingResponse(self)

    async def create(
        self,
        evaluation_dataset_id: str,
        *,
        schema_type: Literal["GENERATION"],
        test_case_data: object,
        account_id: str | NotGiven = NOT_GIVEN,
        chat_history: object | NotGiven = NOT_GIVEN,
        test_case_metadata: object | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseVersionResponse:
        """
        ### Description

        Create a test case for a selected dataset.

        Args:
          schema_type: An enumeration.

          test_case_data: The data for the test case in a format matching the provided schema_type

          account_id: The ID of the account that owns the given entity.

          chat_history: Used for tracking previous chat interactions for multi-chat test cases

          test_case_metadata: Metadata for the test case

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
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases",
            body=await async_maybe_transform(
                {
                    "schema_type": schema_type,
                    "test_case_data": test_case_data,
                    "account_id": account_id,
                    "chat_history": chat_history,
                    "test_case_metadata": test_case_metadata,
                },
                test_case_create_params.TestCaseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseVersionResponse,
        )

    async def retrieve(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseVersionResponse:
        """
        ### Description

        Get the test case by its id.

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
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return await self._get(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseVersionResponse,
        )

    @overload
    async def update(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        chat_history: object | NotGiven = NOT_GIVEN,
        restore: Literal[False] | NotGiven = NOT_GIVEN,
        schema_type: Literal["GENERATION"] | NotGiven = NOT_GIVEN,
        test_case_data: object | NotGiven = NOT_GIVEN,
        test_case_metadata: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseVersionResponse:
        """
        ### Description

        Update a test case.

        Args:
          chat_history: Used for tracking previous chat interactions for multi-chat test cases

          restore: Set to true to restore the entity from the database.

          schema_type: An enumeration.

          test_case_data: The data for the test case in a format matching the provided schema_type

          test_case_metadata: Metadata for the test case

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def update(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseVersionResponse:
        """
        ### Description

        Update a test case.

        Args:
          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["evaluation_dataset_id"], ["evaluation_dataset_id", "restore"])
    async def update(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        chat_history: object | NotGiven = NOT_GIVEN,
        restore: Literal[False] | Literal[True] | NotGiven = NOT_GIVEN,
        schema_type: Literal["GENERATION"] | NotGiven = NOT_GIVEN,
        test_case_data: object | NotGiven = NOT_GIVEN,
        test_case_metadata: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseVersionResponse:
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return await self._patch(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}",
            body=await async_maybe_transform(
                {
                    "chat_history": chat_history,
                    "restore": restore,
                    "schema_type": schema_type,
                    "test_case_data": test_case_data,
                    "test_case_metadata": test_case_metadata,
                },
                test_case_update_params.TestCaseUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseVersionResponse,
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
    ) -> TestCaseListResponse:
        """
        ### Description

        List all test cases for a selected dataset.

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
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases",
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
                    test_case_list_params.TestCaseListParams,
                ),
            ),
            cast_to=TestCaseListResponse,
        )

    async def delete(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteResponse:
        """
        ### Description

        Delete a specified test case -- retaining older version belonging to older
        dataset versions.

        ### Details

        This request shouldn't be used when deleting due to compliance reasons. See Wipe
        action.

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
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return await self._delete(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    async def batch(
        self,
        evaluation_dataset_id: str,
        *,
        body: Iterable[test_case_batch_params.Body],
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseBatchResponse:
        """
        ### Description

        Creates a batch of test cases

        ### Details

        This API can be used to create multiple test cases so users do not have to the
        incur the cost of repeated network calls. To use this API, pass in a list of
        test cases in the request body.

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
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return await self._post(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/batch",
            body=await async_maybe_transform(body, test_case_batch_params.TestCaseBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseBatchResponse,
        )


class TestCasesResourceWithRawResponse:
    __test__ = False

    def __init__(self, test_cases: TestCasesResource) -> None:
        self._test_cases = test_cases

        self.create = to_raw_response_wrapper(
            test_cases.create,
        )
        self.retrieve = to_raw_response_wrapper(
            test_cases.retrieve,
        )
        self.update = to_raw_response_wrapper(
            test_cases.update,
        )
        self.list = to_raw_response_wrapper(
            test_cases.list,
        )
        self.delete = to_raw_response_wrapper(
            test_cases.delete,
        )
        self.batch = to_raw_response_wrapper(
            test_cases.batch,
        )

    @cached_property
    def history(self) -> HistoryResourceWithRawResponse:
        return HistoryResourceWithRawResponse(self._test_cases.history)


class AsyncTestCasesResourceWithRawResponse:
    def __init__(self, test_cases: AsyncTestCasesResource) -> None:
        self._test_cases = test_cases

        self.create = async_to_raw_response_wrapper(
            test_cases.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            test_cases.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            test_cases.update,
        )
        self.list = async_to_raw_response_wrapper(
            test_cases.list,
        )
        self.delete = async_to_raw_response_wrapper(
            test_cases.delete,
        )
        self.batch = async_to_raw_response_wrapper(
            test_cases.batch,
        )

    @cached_property
    def history(self) -> AsyncHistoryResourceWithRawResponse:
        return AsyncHistoryResourceWithRawResponse(self._test_cases.history)


class TestCasesResourceWithStreamingResponse:
    __test__ = False

    def __init__(self, test_cases: TestCasesResource) -> None:
        self._test_cases = test_cases

        self.create = to_streamed_response_wrapper(
            test_cases.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            test_cases.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            test_cases.update,
        )
        self.list = to_streamed_response_wrapper(
            test_cases.list,
        )
        self.delete = to_streamed_response_wrapper(
            test_cases.delete,
        )
        self.batch = to_streamed_response_wrapper(
            test_cases.batch,
        )

    @cached_property
    def history(self) -> HistoryResourceWithStreamingResponse:
        return HistoryResourceWithStreamingResponse(self._test_cases.history)


class AsyncTestCasesResourceWithStreamingResponse:
    def __init__(self, test_cases: AsyncTestCasesResource) -> None:
        self._test_cases = test_cases

        self.create = async_to_streamed_response_wrapper(
            test_cases.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            test_cases.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            test_cases.update,
        )
        self.list = async_to_streamed_response_wrapper(
            test_cases.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            test_cases.delete,
        )
        self.batch = async_to_streamed_response_wrapper(
            test_cases.batch,
        )

    @cached_property
    def history(self) -> AsyncHistoryResourceWithStreamingResponse:
        return AsyncHistoryResourceWithStreamingResponse(self._test_cases.history)
