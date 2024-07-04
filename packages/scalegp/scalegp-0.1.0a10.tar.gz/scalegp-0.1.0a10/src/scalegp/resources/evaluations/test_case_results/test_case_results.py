# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
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
from ....types.evaluations import (
    test_case_result_list_params,
    test_case_result_batch_params,
    test_case_result_create_params,
    test_case_result_update_params,
    test_case_result_retrieve_params,
)
from ....types.shared.test_case_result_response import TestCaseResultResponse
from ....types.evaluations.test_case_result_list_response import TestCaseResultListResponse
from ....types.evaluations.test_case_result_batch_response import TestCaseResultBatchResponse
from ....types.shared.test_case_result_response_with_views import TestCaseResultResponseWithViews

__all__ = ["TestCaseResultsResource", "AsyncTestCaseResultsResource"]


class TestCaseResultsResource(SyncAPIResource):
    __test__ = False

    @cached_property
    def history(self) -> HistoryResource:
        return HistoryResource(self._client)

    @cached_property
    def with_raw_response(self) -> TestCaseResultsResourceWithRawResponse:
        return TestCaseResultsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TestCaseResultsResourceWithStreamingResponse:
        return TestCaseResultsResourceWithStreamingResponse(self)

    def create(
        self,
        evaluation_id: str,
        *,
        application_spec_id: str,
        evaluation_dataset_version_num: str,
        test_case_evaluation_data: object,
        test_case_evaluation_data_schema: Literal["GENERATION"],
        test_case_id: str,
        account_id: str | NotGiven = NOT_GIVEN,
        annotated_by_user_id: str | NotGiven = NOT_GIVEN,
        audit_comment: str | NotGiven = NOT_GIVEN,
        audit_required: bool | NotGiven = NOT_GIVEN,
        audit_status: Literal["UNAUDITED", "FIXED", "APPROVED"] | NotGiven = NOT_GIVEN,
        result: object | NotGiven = NOT_GIVEN,
        time_spent_labeling_s: int | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseResultResponse:
        """
        ### Description

        Creates a test case result

        ### Details

        This API can be used to create a test case result. To use this API, review the
        request schema and pass in all fields that are required to create a test case
        result.

        Args:
          test_case_evaluation_data_schema: An enumeration.

          account_id: The ID of the account that owns the given entity.

          annotated_by_user_id: The user who annotated the task.

          audit_status: An enumeration.

          time_spent_labeling_s: The time spent labeling in seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return self._post(
            f"/v4/evaluations/{evaluation_id}/test-case-results",
            body=maybe_transform(
                {
                    "application_spec_id": application_spec_id,
                    "evaluation_dataset_version_num": evaluation_dataset_version_num,
                    "test_case_evaluation_data": test_case_evaluation_data,
                    "test_case_evaluation_data_schema": test_case_evaluation_data_schema,
                    "test_case_id": test_case_id,
                    "account_id": account_id,
                    "annotated_by_user_id": annotated_by_user_id,
                    "audit_comment": audit_comment,
                    "audit_required": audit_required,
                    "audit_status": audit_status,
                    "result": result,
                    "time_spent_labeling_s": time_spent_labeling_s,
                },
                test_case_result_create_params.TestCaseResultCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseResultResponse,
        )

    def retrieve(
        self,
        test_case_result_id: str,
        *,
        evaluation_id: str,
        view: List[Literal["AnnotationResults", "Task", "TestCaseVersion"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseResultResponseWithViews:
        """
        ### Description

        Gets the details of a test case result

        ### Details

        This API can be used to get information about a single test case result by ID.
        To use this API, pass in the `id` that was returned from your Create Test Case
        Result API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        if not test_case_result_id:
            raise ValueError(
                f"Expected a non-empty value for `test_case_result_id` but received {test_case_result_id!r}"
            )
        return self._get(
            f"/v4/evaluations/{evaluation_id}/test-case-results/{test_case_result_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"view": view}, test_case_result_retrieve_params.TestCaseResultRetrieveParams),
            ),
            cast_to=TestCaseResultResponseWithViews,
        )

    def update(
        self,
        test_case_result_id: str,
        *,
        evaluation_id: str,
        annotated_by_user_id: str | NotGiven = NOT_GIVEN,
        application_spec_id: str | NotGiven = NOT_GIVEN,
        audit_comment: str | NotGiven = NOT_GIVEN,
        audit_required: bool | NotGiven = NOT_GIVEN,
        audit_status: Literal["UNAUDITED", "FIXED", "APPROVED"] | NotGiven = NOT_GIVEN,
        evaluation_dataset_version_num: str | NotGiven = NOT_GIVEN,
        result: object | NotGiven = NOT_GIVEN,
        test_case_evaluation_data: object | NotGiven = NOT_GIVEN,
        test_case_evaluation_data_schema: Literal["GENERATION"] | NotGiven = NOT_GIVEN,
        test_case_id: str | NotGiven = NOT_GIVEN,
        time_spent_labeling_s: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseResultResponse:
        """
        ### Description

        Updates a test case result

        ### Details

        This API can be used to update the test case result that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Test Case Result API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          annotated_by_user_id: The user who annotated the task.

          audit_status: An enumeration.

          test_case_evaluation_data_schema: An enumeration.

          time_spent_labeling_s: The time spent labeling in seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        if not test_case_result_id:
            raise ValueError(
                f"Expected a non-empty value for `test_case_result_id` but received {test_case_result_id!r}"
            )
        return self._patch(
            f"/v4/evaluations/{evaluation_id}/test-case-results/{test_case_result_id}",
            body=maybe_transform(
                {
                    "annotated_by_user_id": annotated_by_user_id,
                    "application_spec_id": application_spec_id,
                    "audit_comment": audit_comment,
                    "audit_required": audit_required,
                    "audit_status": audit_status,
                    "evaluation_dataset_version_num": evaluation_dataset_version_num,
                    "result": result,
                    "test_case_evaluation_data": test_case_evaluation_data,
                    "test_case_evaluation_data_schema": test_case_evaluation_data_schema,
                    "test_case_id": test_case_id,
                    "time_spent_labeling_s": time_spent_labeling_s,
                },
                test_case_result_update_params.TestCaseResultUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseResultResponse,
        )

    def list(
        self,
        evaluation_id: str,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        include_archived: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        view: List[Literal["AnnotationResults", "Task", "TestCaseVersion"]] | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseResultListResponse:
        """
        ### Description

        Lists all test case results accessible to the user.

        ### Details

        This API can be used to list test case results. If a user has access to multiple
        accounts, all test case results from all accounts the user is associated with
        will be returned.

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
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return self._get(
            f"/v4/evaluations/{evaluation_id}/test-case-results",
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
                        "view": view,
                    },
                    test_case_result_list_params.TestCaseResultListParams,
                ),
            ),
            cast_to=TestCaseResultListResponse,
        )

    def batch(
        self,
        evaluation_id: str,
        *,
        body: Iterable[test_case_result_batch_params.Body],
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseResultBatchResponse:
        """
        ### Description

        Creates a batch of test case results

        ### Details

        This API can be used to create multiple test case results so users do not have
        to the incur the cost of repeated network calls. To use this API, pass in a list
        of test case results in the request body.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return self._post(
            f"/v4/evaluations/{evaluation_id}/test-case-results/batch",
            body=maybe_transform(body, test_case_result_batch_params.TestCaseResultBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseResultBatchResponse,
        )


class AsyncTestCaseResultsResource(AsyncAPIResource):
    @cached_property
    def history(self) -> AsyncHistoryResource:
        return AsyncHistoryResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTestCaseResultsResourceWithRawResponse:
        return AsyncTestCaseResultsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTestCaseResultsResourceWithStreamingResponse:
        return AsyncTestCaseResultsResourceWithStreamingResponse(self)

    async def create(
        self,
        evaluation_id: str,
        *,
        application_spec_id: str,
        evaluation_dataset_version_num: str,
        test_case_evaluation_data: object,
        test_case_evaluation_data_schema: Literal["GENERATION"],
        test_case_id: str,
        account_id: str | NotGiven = NOT_GIVEN,
        annotated_by_user_id: str | NotGiven = NOT_GIVEN,
        audit_comment: str | NotGiven = NOT_GIVEN,
        audit_required: bool | NotGiven = NOT_GIVEN,
        audit_status: Literal["UNAUDITED", "FIXED", "APPROVED"] | NotGiven = NOT_GIVEN,
        result: object | NotGiven = NOT_GIVEN,
        time_spent_labeling_s: int | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseResultResponse:
        """
        ### Description

        Creates a test case result

        ### Details

        This API can be used to create a test case result. To use this API, review the
        request schema and pass in all fields that are required to create a test case
        result.

        Args:
          test_case_evaluation_data_schema: An enumeration.

          account_id: The ID of the account that owns the given entity.

          annotated_by_user_id: The user who annotated the task.

          audit_status: An enumeration.

          time_spent_labeling_s: The time spent labeling in seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return await self._post(
            f"/v4/evaluations/{evaluation_id}/test-case-results",
            body=await async_maybe_transform(
                {
                    "application_spec_id": application_spec_id,
                    "evaluation_dataset_version_num": evaluation_dataset_version_num,
                    "test_case_evaluation_data": test_case_evaluation_data,
                    "test_case_evaluation_data_schema": test_case_evaluation_data_schema,
                    "test_case_id": test_case_id,
                    "account_id": account_id,
                    "annotated_by_user_id": annotated_by_user_id,
                    "audit_comment": audit_comment,
                    "audit_required": audit_required,
                    "audit_status": audit_status,
                    "result": result,
                    "time_spent_labeling_s": time_spent_labeling_s,
                },
                test_case_result_create_params.TestCaseResultCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseResultResponse,
        )

    async def retrieve(
        self,
        test_case_result_id: str,
        *,
        evaluation_id: str,
        view: List[Literal["AnnotationResults", "Task", "TestCaseVersion"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseResultResponseWithViews:
        """
        ### Description

        Gets the details of a test case result

        ### Details

        This API can be used to get information about a single test case result by ID.
        To use this API, pass in the `id` that was returned from your Create Test Case
        Result API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        if not test_case_result_id:
            raise ValueError(
                f"Expected a non-empty value for `test_case_result_id` but received {test_case_result_id!r}"
            )
        return await self._get(
            f"/v4/evaluations/{evaluation_id}/test-case-results/{test_case_result_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"view": view}, test_case_result_retrieve_params.TestCaseResultRetrieveParams
                ),
            ),
            cast_to=TestCaseResultResponseWithViews,
        )

    async def update(
        self,
        test_case_result_id: str,
        *,
        evaluation_id: str,
        annotated_by_user_id: str | NotGiven = NOT_GIVEN,
        application_spec_id: str | NotGiven = NOT_GIVEN,
        audit_comment: str | NotGiven = NOT_GIVEN,
        audit_required: bool | NotGiven = NOT_GIVEN,
        audit_status: Literal["UNAUDITED", "FIXED", "APPROVED"] | NotGiven = NOT_GIVEN,
        evaluation_dataset_version_num: str | NotGiven = NOT_GIVEN,
        result: object | NotGiven = NOT_GIVEN,
        test_case_evaluation_data: object | NotGiven = NOT_GIVEN,
        test_case_evaluation_data_schema: Literal["GENERATION"] | NotGiven = NOT_GIVEN,
        test_case_id: str | NotGiven = NOT_GIVEN,
        time_spent_labeling_s: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseResultResponse:
        """
        ### Description

        Updates a test case result

        ### Details

        This API can be used to update the test case result that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Test Case Result API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          annotated_by_user_id: The user who annotated the task.

          audit_status: An enumeration.

          test_case_evaluation_data_schema: An enumeration.

          time_spent_labeling_s: The time spent labeling in seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        if not test_case_result_id:
            raise ValueError(
                f"Expected a non-empty value for `test_case_result_id` but received {test_case_result_id!r}"
            )
        return await self._patch(
            f"/v4/evaluations/{evaluation_id}/test-case-results/{test_case_result_id}",
            body=await async_maybe_transform(
                {
                    "annotated_by_user_id": annotated_by_user_id,
                    "application_spec_id": application_spec_id,
                    "audit_comment": audit_comment,
                    "audit_required": audit_required,
                    "audit_status": audit_status,
                    "evaluation_dataset_version_num": evaluation_dataset_version_num,
                    "result": result,
                    "test_case_evaluation_data": test_case_evaluation_data,
                    "test_case_evaluation_data_schema": test_case_evaluation_data_schema,
                    "test_case_id": test_case_id,
                    "time_spent_labeling_s": time_spent_labeling_s,
                },
                test_case_result_update_params.TestCaseResultUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseResultResponse,
        )

    async def list(
        self,
        evaluation_id: str,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        include_archived: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        view: List[Literal["AnnotationResults", "Task", "TestCaseVersion"]] | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseResultListResponse:
        """
        ### Description

        Lists all test case results accessible to the user.

        ### Details

        This API can be used to list test case results. If a user has access to multiple
        accounts, all test case results from all accounts the user is associated with
        will be returned.

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
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return await self._get(
            f"/v4/evaluations/{evaluation_id}/test-case-results",
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
                        "view": view,
                    },
                    test_case_result_list_params.TestCaseResultListParams,
                ),
            ),
            cast_to=TestCaseResultListResponse,
        )

    async def batch(
        self,
        evaluation_id: str,
        *,
        body: Iterable[test_case_result_batch_params.Body],
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseResultBatchResponse:
        """
        ### Description

        Creates a batch of test case results

        ### Details

        This API can be used to create multiple test case results so users do not have
        to the incur the cost of repeated network calls. To use this API, pass in a list
        of test case results in the request body.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return await self._post(
            f"/v4/evaluations/{evaluation_id}/test-case-results/batch",
            body=await async_maybe_transform(body, test_case_result_batch_params.TestCaseResultBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseResultBatchResponse,
        )


class TestCaseResultsResourceWithRawResponse:
    __test__ = False

    def __init__(self, test_case_results: TestCaseResultsResource) -> None:
        self._test_case_results = test_case_results

        self.create = to_raw_response_wrapper(
            test_case_results.create,
        )
        self.retrieve = to_raw_response_wrapper(
            test_case_results.retrieve,
        )
        self.update = to_raw_response_wrapper(
            test_case_results.update,
        )
        self.list = to_raw_response_wrapper(
            test_case_results.list,
        )
        self.batch = to_raw_response_wrapper(
            test_case_results.batch,
        )

    @cached_property
    def history(self) -> HistoryResourceWithRawResponse:
        return HistoryResourceWithRawResponse(self._test_case_results.history)


class AsyncTestCaseResultsResourceWithRawResponse:
    def __init__(self, test_case_results: AsyncTestCaseResultsResource) -> None:
        self._test_case_results = test_case_results

        self.create = async_to_raw_response_wrapper(
            test_case_results.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            test_case_results.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            test_case_results.update,
        )
        self.list = async_to_raw_response_wrapper(
            test_case_results.list,
        )
        self.batch = async_to_raw_response_wrapper(
            test_case_results.batch,
        )

    @cached_property
    def history(self) -> AsyncHistoryResourceWithRawResponse:
        return AsyncHistoryResourceWithRawResponse(self._test_case_results.history)


class TestCaseResultsResourceWithStreamingResponse:
    __test__ = False

    def __init__(self, test_case_results: TestCaseResultsResource) -> None:
        self._test_case_results = test_case_results

        self.create = to_streamed_response_wrapper(
            test_case_results.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            test_case_results.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            test_case_results.update,
        )
        self.list = to_streamed_response_wrapper(
            test_case_results.list,
        )
        self.batch = to_streamed_response_wrapper(
            test_case_results.batch,
        )

    @cached_property
    def history(self) -> HistoryResourceWithStreamingResponse:
        return HistoryResourceWithStreamingResponse(self._test_case_results.history)


class AsyncTestCaseResultsResourceWithStreamingResponse:
    def __init__(self, test_case_results: AsyncTestCaseResultsResource) -> None:
        self._test_case_results = test_case_results

        self.create = async_to_streamed_response_wrapper(
            test_case_results.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            test_case_results.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            test_case_results.update,
        )
        self.list = async_to_streamed_response_wrapper(
            test_case_results.list,
        )
        self.batch = async_to_streamed_response_wrapper(
            test_case_results.batch,
        )

    @cached_property
    def history(self) -> AsyncHistoryResourceWithStreamingResponse:
        return AsyncHistoryResourceWithStreamingResponse(self._test_case_results.history)
