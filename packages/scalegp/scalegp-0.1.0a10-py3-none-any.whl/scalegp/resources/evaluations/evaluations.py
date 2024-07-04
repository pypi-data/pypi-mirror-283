# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, overload
from typing_extensions import Literal

import httpx

from .tasks import (
    TasksResource,
    AsyncTasksResource,
    TasksResourceWithRawResponse,
    AsyncTasksResourceWithRawResponse,
    TasksResourceWithStreamingResponse,
    AsyncTasksResourceWithStreamingResponse,
)
from ...types import (
    evaluation_list_params,
    evaluation_create_params,
    evaluation_update_params,
    evaluation_retrieve_params,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    required_args,
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
from .test_case_results import (
    TestCaseResultsResource,
    AsyncTestCaseResultsResource,
    TestCaseResultsResourceWithRawResponse,
    AsyncTestCaseResultsResourceWithRawResponse,
    TestCaseResultsResourceWithStreamingResponse,
    AsyncTestCaseResultsResourceWithStreamingResponse,
)
from .evaluation_metrics import (
    EvaluationMetricsResource,
    AsyncEvaluationMetricsResource,
    EvaluationMetricsResourceWithRawResponse,
    AsyncEvaluationMetricsResourceWithRawResponse,
    EvaluationMetricsResourceWithStreamingResponse,
    AsyncEvaluationMetricsResourceWithStreamingResponse,
)
from .contributor_metrics import (
    ContributorMetricsResource,
    AsyncContributorMetricsResource,
    ContributorMetricsResourceWithRawResponse,
    AsyncContributorMetricsResourceWithRawResponse,
    ContributorMetricsResourceWithStreamingResponse,
    AsyncContributorMetricsResourceWithStreamingResponse,
)
from .hybrid_eval_metrics import (
    HybridEvalMetricsResource,
    AsyncHybridEvalMetricsResource,
    HybridEvalMetricsResourceWithRawResponse,
    AsyncHybridEvalMetricsResourceWithRawResponse,
    HybridEvalMetricsResourceWithStreamingResponse,
    AsyncHybridEvalMetricsResourceWithStreamingResponse,
)
from ...types.evaluation_response import EvaluationResponse
from ...types.shared.task_response import TaskResponse
from ...types.shared.delete_response import DeleteResponse
from ...types.evaluation_list_response import EvaluationListResponse
from .test_case_results.test_case_results import TestCaseResultsResource, AsyncTestCaseResultsResource
from ...types.evaluation_response_with_views import EvaluationResponseWithViews

__all__ = ["EvaluationsResource", "AsyncEvaluationsResource"]


class EvaluationsResource(SyncAPIResource):
    @cached_property
    def tasks(self) -> TasksResource:
        return TasksResource(self._client)

    @cached_property
    def contributor_metrics(self) -> ContributorMetricsResource:
        return ContributorMetricsResource(self._client)

    @cached_property
    def evaluation_metrics(self) -> EvaluationMetricsResource:
        return EvaluationMetricsResource(self._client)

    @cached_property
    def hybrid_eval_metrics(self) -> HybridEvalMetricsResource:
        return HybridEvalMetricsResource(self._client)

    @cached_property
    def test_case_results(self) -> TestCaseResultsResource:
        return TestCaseResultsResource(self._client)

    @cached_property
    def with_raw_response(self) -> EvaluationsResourceWithRawResponse:
        return EvaluationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluationsResourceWithStreamingResponse:
        return EvaluationsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        application_variant_id: str,
        description: str,
        evaluation_dataset_id: str,
        name: str,
        evaluation_config: object | NotGiven = NOT_GIVEN,
        evaluation_config_id: str | NotGiven = NOT_GIVEN,
        evaluation_dataset_version: int | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        type: Literal["builder"] | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponse:
        """
        ### Description

        Creates a evaluation

        ### Details

        This API can be used to create a evaluation. To use this API, review the request
        schema and pass in all fields that are required to create a evaluation.

        Args:
          account_id: The ID of the account that owns the given entity.

          evaluation_config_id: The ID of the associated evaluation config.

          type: create standalone evaluation or build evaluation which will auto generate test
              case results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        description: str,
        name: str,
        application_variant_id: str | NotGiven = NOT_GIVEN,
        evaluation_config: object | NotGiven = NOT_GIVEN,
        evaluation_config_id: str | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        type: Literal["default"] | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponse:
        """
        ### Description

        Creates a evaluation

        ### Details

        This API can be used to create a evaluation. To use this API, review the request
        schema and pass in all fields that are required to create a evaluation.

        Args:
          account_id: The ID of the account that owns the given entity.

          evaluation_config_id: The ID of the associated evaluation config.

          type: create standalone evaluation or build evaluation which will auto generate test
              case results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["account_id", "application_spec_id", "application_variant_id", "description", "evaluation_dataset_id", "name"],
        ["account_id", "application_spec_id", "description", "name"],
    )
    def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        application_variant_id: str | NotGiven = NOT_GIVEN,
        description: str,
        evaluation_dataset_id: str | NotGiven = NOT_GIVEN,
        name: str,
        evaluation_config: object | NotGiven = NOT_GIVEN,
        evaluation_config_id: str | NotGiven = NOT_GIVEN,
        evaluation_dataset_version: int | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        type: Literal["builder"] | Literal["default"] | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponse:
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return self._post(
            "/v4/evaluations",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "application_spec_id": application_spec_id,
                    "application_variant_id": application_variant_id,
                    "description": description,
                    "evaluation_dataset_id": evaluation_dataset_id,
                    "name": name,
                    "evaluation_config": evaluation_config,
                    "evaluation_config_id": evaluation_config_id,
                    "evaluation_dataset_version": evaluation_dataset_version,
                    "tags": tags,
                    "type": type,
                },
                evaluation_create_params.EvaluationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationResponse,
        )

    def retrieve(
        self,
        evaluation_id: str,
        *,
        view: List[Literal["ApplicationSpec", "AsyncJobs", "EvaluationConfig", "TestCaseResults"]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponseWithViews:
        """
        ### Description

        Gets the details of a evaluation

        ### Details

        This API can be used to get information about a single evaluation by ID. To use
        this API, pass in the `id` that was returned from your Create Evaluation API
        call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._get(
            f"/v4/evaluations/{evaluation_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"view": view}, evaluation_retrieve_params.EvaluationRetrieveParams),
            ),
            cast_to=EvaluationResponseWithViews,
        )

    @overload
    def update(
        self,
        evaluation_id: str,
        *,
        application_spec_id: str | NotGiven = NOT_GIVEN,
        application_variant_id: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        evaluation_config: object | NotGiven = NOT_GIVEN,
        evaluation_config_id: str | NotGiven = NOT_GIVEN,
        evaluation_type: Literal["llm_benchmark"] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        restore: Literal[False] | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponse:
        """
        ### Description

        Updates a evaluation

        ### Details

        This API can be used to update the evaluation that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Evaluation API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          evaluation_config_id: The ID of the associated evaluation config.

          evaluation_type: If llm_benchmark is provided, the evaluation will be updated to a hybrid
              evaluation. No-op on existing hybrid evaluations, and not available for studio
              evaluations.

          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def update(
        self,
        evaluation_id: str,
        *,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponse:
        """
        ### Description

        Updates a evaluation

        ### Details

        This API can be used to update the evaluation that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Evaluation API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    def update(
        self,
        evaluation_id: str,
        *,
        application_spec_id: str | NotGiven = NOT_GIVEN,
        application_variant_id: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        evaluation_config: object | NotGiven = NOT_GIVEN,
        evaluation_config_id: str | NotGiven = NOT_GIVEN,
        evaluation_type: Literal["llm_benchmark"] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        restore: Literal[False] | Literal[True] | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponse:
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._patch(
            f"/v4/evaluations/{evaluation_id}",
            body=maybe_transform(
                {
                    "application_spec_id": application_spec_id,
                    "application_variant_id": application_variant_id,
                    "description": description,
                    "evaluation_config": evaluation_config,
                    "evaluation_config_id": evaluation_config_id,
                    "evaluation_type": evaluation_type,
                    "name": name,
                    "restore": restore,
                    "tags": tags,
                },
                evaluation_update_params.EvaluationUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationResponse,
        )

    def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        include_archived: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        sort_by: List[
            Literal[
                "status:asc",
                "status:desc",
                "application_spec_id:asc",
                "application_spec_id:desc",
                "application_spec:asc",
                "application_spec:desc",
                "application_variant_id:asc",
                "application_variant_id:desc",
                "evaluation_config_id:asc",
                "evaluation_config_id:desc",
                "completed_at:asc",
                "completed_at:desc",
                "total_test_case_result_count:asc",
                "total_test_case_result_count:desc",
                "completed_test_case_result_count:asc",
                "completed_test_case_result_count:desc",
                "evaluation_config_expanded:asc",
                "evaluation_config_expanded:desc",
                "test_case_results:asc",
                "test_case_results:desc",
                "async_jobs:asc",
                "async_jobs:desc",
                "id:asc",
                "id:desc",
                "created_at:asc",
                "created_at:desc",
                "account_id:asc",
                "account_id:desc",
                "created_by_user_id:asc",
                "created_by_user_id:desc",
                "archived_at:asc",
                "archived_at:desc",
                "created_by_user:asc",
                "created_by_user:desc",
                "name:asc",
                "name:desc",
                "description:asc",
                "description:desc",
                "tags:asc",
                "tags:desc",
                "evaluation_config:asc",
                "evaluation_config:desc",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        view: List[Literal["ApplicationSpec", "AsyncJobs", "EvaluationConfig", "TestCaseResults"]]
        | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationListResponse:
        """
        ### Description

        Lists all evaluations accessible to the user.

        ### Details

        This API can be used to list evaluations. If a user has access to multiple
        accounts, all evaluations from all accounts the user is associated with will be
        returned.

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
            "/v4/evaluations",
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
                        "sort_by": sort_by,
                        "view": view,
                    },
                    evaluation_list_params.EvaluationListParams,
                ),
            ),
            cast_to=EvaluationListResponse,
        )

    def delete(
        self,
        evaluation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteResponse:
        """
        ### Description

        Deletes a evaluation

        ### Details

        This API can be used to delete a evaluation by ID. To use this API, pass in the
        `id` that was returned from your Create Evaluation API call as a path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._delete(
            f"/v4/evaluations/{evaluation_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    def claim_task(
        self,
        evaluation_id: str,
        *,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskResponse:
        """
        Claim Evaluation Task

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
            f"/v4/evaluations/{evaluation_id}/claim-task",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskResponse,
        )


class AsyncEvaluationsResource(AsyncAPIResource):
    @cached_property
    def tasks(self) -> AsyncTasksResource:
        return AsyncTasksResource(self._client)

    @cached_property
    def contributor_metrics(self) -> AsyncContributorMetricsResource:
        return AsyncContributorMetricsResource(self._client)

    @cached_property
    def evaluation_metrics(self) -> AsyncEvaluationMetricsResource:
        return AsyncEvaluationMetricsResource(self._client)

    @cached_property
    def hybrid_eval_metrics(self) -> AsyncHybridEvalMetricsResource:
        return AsyncHybridEvalMetricsResource(self._client)

    @cached_property
    def test_case_results(self) -> AsyncTestCaseResultsResource:
        return AsyncTestCaseResultsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEvaluationsResourceWithRawResponse:
        return AsyncEvaluationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluationsResourceWithStreamingResponse:
        return AsyncEvaluationsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        application_variant_id: str,
        description: str,
        evaluation_dataset_id: str,
        name: str,
        evaluation_config: object | NotGiven = NOT_GIVEN,
        evaluation_config_id: str | NotGiven = NOT_GIVEN,
        evaluation_dataset_version: int | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        type: Literal["builder"] | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponse:
        """
        ### Description

        Creates a evaluation

        ### Details

        This API can be used to create a evaluation. To use this API, review the request
        schema and pass in all fields that are required to create a evaluation.

        Args:
          account_id: The ID of the account that owns the given entity.

          evaluation_config_id: The ID of the associated evaluation config.

          type: create standalone evaluation or build evaluation which will auto generate test
              case results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        description: str,
        name: str,
        application_variant_id: str | NotGiven = NOT_GIVEN,
        evaluation_config: object | NotGiven = NOT_GIVEN,
        evaluation_config_id: str | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        type: Literal["default"] | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponse:
        """
        ### Description

        Creates a evaluation

        ### Details

        This API can be used to create a evaluation. To use this API, review the request
        schema and pass in all fields that are required to create a evaluation.

        Args:
          account_id: The ID of the account that owns the given entity.

          evaluation_config_id: The ID of the associated evaluation config.

          type: create standalone evaluation or build evaluation which will auto generate test
              case results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["account_id", "application_spec_id", "application_variant_id", "description", "evaluation_dataset_id", "name"],
        ["account_id", "application_spec_id", "description", "name"],
    )
    async def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        application_variant_id: str | NotGiven = NOT_GIVEN,
        description: str,
        evaluation_dataset_id: str | NotGiven = NOT_GIVEN,
        name: str,
        evaluation_config: object | NotGiven = NOT_GIVEN,
        evaluation_config_id: str | NotGiven = NOT_GIVEN,
        evaluation_dataset_version: int | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        type: Literal["builder"] | Literal["default"] | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponse:
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return await self._post(
            "/v4/evaluations",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "application_spec_id": application_spec_id,
                    "application_variant_id": application_variant_id,
                    "description": description,
                    "evaluation_dataset_id": evaluation_dataset_id,
                    "name": name,
                    "evaluation_config": evaluation_config,
                    "evaluation_config_id": evaluation_config_id,
                    "evaluation_dataset_version": evaluation_dataset_version,
                    "tags": tags,
                    "type": type,
                },
                evaluation_create_params.EvaluationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationResponse,
        )

    async def retrieve(
        self,
        evaluation_id: str,
        *,
        view: List[Literal["ApplicationSpec", "AsyncJobs", "EvaluationConfig", "TestCaseResults"]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponseWithViews:
        """
        ### Description

        Gets the details of a evaluation

        ### Details

        This API can be used to get information about a single evaluation by ID. To use
        this API, pass in the `id` that was returned from your Create Evaluation API
        call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._get(
            f"/v4/evaluations/{evaluation_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"view": view}, evaluation_retrieve_params.EvaluationRetrieveParams),
            ),
            cast_to=EvaluationResponseWithViews,
        )

    @overload
    async def update(
        self,
        evaluation_id: str,
        *,
        application_spec_id: str | NotGiven = NOT_GIVEN,
        application_variant_id: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        evaluation_config: object | NotGiven = NOT_GIVEN,
        evaluation_config_id: str | NotGiven = NOT_GIVEN,
        evaluation_type: Literal["llm_benchmark"] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        restore: Literal[False] | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponse:
        """
        ### Description

        Updates a evaluation

        ### Details

        This API can be used to update the evaluation that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Evaluation API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          evaluation_config_id: The ID of the associated evaluation config.

          evaluation_type: If llm_benchmark is provided, the evaluation will be updated to a hybrid
              evaluation. No-op on existing hybrid evaluations, and not available for studio
              evaluations.

          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def update(
        self,
        evaluation_id: str,
        *,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponse:
        """
        ### Description

        Updates a evaluation

        ### Details

        This API can be used to update the evaluation that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Evaluation API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    async def update(
        self,
        evaluation_id: str,
        *,
        application_spec_id: str | NotGiven = NOT_GIVEN,
        application_variant_id: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        evaluation_config: object | NotGiven = NOT_GIVEN,
        evaluation_config_id: str | NotGiven = NOT_GIVEN,
        evaluation_type: Literal["llm_benchmark"] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        restore: Literal[False] | Literal[True] | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationResponse:
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._patch(
            f"/v4/evaluations/{evaluation_id}",
            body=await async_maybe_transform(
                {
                    "application_spec_id": application_spec_id,
                    "application_variant_id": application_variant_id,
                    "description": description,
                    "evaluation_config": evaluation_config,
                    "evaluation_config_id": evaluation_config_id,
                    "evaluation_type": evaluation_type,
                    "name": name,
                    "restore": restore,
                    "tags": tags,
                },
                evaluation_update_params.EvaluationUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationResponse,
        )

    async def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        include_archived: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        sort_by: List[
            Literal[
                "status:asc",
                "status:desc",
                "application_spec_id:asc",
                "application_spec_id:desc",
                "application_spec:asc",
                "application_spec:desc",
                "application_variant_id:asc",
                "application_variant_id:desc",
                "evaluation_config_id:asc",
                "evaluation_config_id:desc",
                "completed_at:asc",
                "completed_at:desc",
                "total_test_case_result_count:asc",
                "total_test_case_result_count:desc",
                "completed_test_case_result_count:asc",
                "completed_test_case_result_count:desc",
                "evaluation_config_expanded:asc",
                "evaluation_config_expanded:desc",
                "test_case_results:asc",
                "test_case_results:desc",
                "async_jobs:asc",
                "async_jobs:desc",
                "id:asc",
                "id:desc",
                "created_at:asc",
                "created_at:desc",
                "account_id:asc",
                "account_id:desc",
                "created_by_user_id:asc",
                "created_by_user_id:desc",
                "archived_at:asc",
                "archived_at:desc",
                "created_by_user:asc",
                "created_by_user:desc",
                "name:asc",
                "name:desc",
                "description:asc",
                "description:desc",
                "tags:asc",
                "tags:desc",
                "evaluation_config:asc",
                "evaluation_config:desc",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        view: List[Literal["ApplicationSpec", "AsyncJobs", "EvaluationConfig", "TestCaseResults"]]
        | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationListResponse:
        """
        ### Description

        Lists all evaluations accessible to the user.

        ### Details

        This API can be used to list evaluations. If a user has access to multiple
        accounts, all evaluations from all accounts the user is associated with will be
        returned.

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
            "/v4/evaluations",
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
                        "sort_by": sort_by,
                        "view": view,
                    },
                    evaluation_list_params.EvaluationListParams,
                ),
            ),
            cast_to=EvaluationListResponse,
        )

    async def delete(
        self,
        evaluation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteResponse:
        """
        ### Description

        Deletes a evaluation

        ### Details

        This API can be used to delete a evaluation by ID. To use this API, pass in the
        `id` that was returned from your Create Evaluation API call as a path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._delete(
            f"/v4/evaluations/{evaluation_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )

    async def claim_task(
        self,
        evaluation_id: str,
        *,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskResponse:
        """
        Claim Evaluation Task

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
            f"/v4/evaluations/{evaluation_id}/claim-task",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskResponse,
        )


class EvaluationsResourceWithRawResponse:
    def __init__(self, evaluations: EvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = to_raw_response_wrapper(
            evaluations.create,
        )
        self.retrieve = to_raw_response_wrapper(
            evaluations.retrieve,
        )
        self.update = to_raw_response_wrapper(
            evaluations.update,
        )
        self.list = to_raw_response_wrapper(
            evaluations.list,
        )
        self.delete = to_raw_response_wrapper(
            evaluations.delete,
        )
        self.claim_task = to_raw_response_wrapper(
            evaluations.claim_task,
        )

    @cached_property
    def tasks(self) -> TasksResourceWithRawResponse:
        return TasksResourceWithRawResponse(self._evaluations.tasks)

    @cached_property
    def contributor_metrics(self) -> ContributorMetricsResourceWithRawResponse:
        return ContributorMetricsResourceWithRawResponse(self._evaluations.contributor_metrics)

    @cached_property
    def evaluation_metrics(self) -> EvaluationMetricsResourceWithRawResponse:
        return EvaluationMetricsResourceWithRawResponse(self._evaluations.evaluation_metrics)

    @cached_property
    def hybrid_eval_metrics(self) -> HybridEvalMetricsResourceWithRawResponse:
        return HybridEvalMetricsResourceWithRawResponse(self._evaluations.hybrid_eval_metrics)

    @cached_property
    def test_case_results(self) -> TestCaseResultsResourceWithRawResponse:
        return TestCaseResultsResourceWithRawResponse(self._evaluations.test_case_results)


class AsyncEvaluationsResourceWithRawResponse:
    def __init__(self, evaluations: AsyncEvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = async_to_raw_response_wrapper(
            evaluations.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            evaluations.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            evaluations.update,
        )
        self.list = async_to_raw_response_wrapper(
            evaluations.list,
        )
        self.delete = async_to_raw_response_wrapper(
            evaluations.delete,
        )
        self.claim_task = async_to_raw_response_wrapper(
            evaluations.claim_task,
        )

    @cached_property
    def tasks(self) -> AsyncTasksResourceWithRawResponse:
        return AsyncTasksResourceWithRawResponse(self._evaluations.tasks)

    @cached_property
    def contributor_metrics(self) -> AsyncContributorMetricsResourceWithRawResponse:
        return AsyncContributorMetricsResourceWithRawResponse(self._evaluations.contributor_metrics)

    @cached_property
    def evaluation_metrics(self) -> AsyncEvaluationMetricsResourceWithRawResponse:
        return AsyncEvaluationMetricsResourceWithRawResponse(self._evaluations.evaluation_metrics)

    @cached_property
    def hybrid_eval_metrics(self) -> AsyncHybridEvalMetricsResourceWithRawResponse:
        return AsyncHybridEvalMetricsResourceWithRawResponse(self._evaluations.hybrid_eval_metrics)

    @cached_property
    def test_case_results(self) -> AsyncTestCaseResultsResourceWithRawResponse:
        return AsyncTestCaseResultsResourceWithRawResponse(self._evaluations.test_case_results)


class EvaluationsResourceWithStreamingResponse:
    def __init__(self, evaluations: EvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = to_streamed_response_wrapper(
            evaluations.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            evaluations.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            evaluations.update,
        )
        self.list = to_streamed_response_wrapper(
            evaluations.list,
        )
        self.delete = to_streamed_response_wrapper(
            evaluations.delete,
        )
        self.claim_task = to_streamed_response_wrapper(
            evaluations.claim_task,
        )

    @cached_property
    def tasks(self) -> TasksResourceWithStreamingResponse:
        return TasksResourceWithStreamingResponse(self._evaluations.tasks)

    @cached_property
    def contributor_metrics(self) -> ContributorMetricsResourceWithStreamingResponse:
        return ContributorMetricsResourceWithStreamingResponse(self._evaluations.contributor_metrics)

    @cached_property
    def evaluation_metrics(self) -> EvaluationMetricsResourceWithStreamingResponse:
        return EvaluationMetricsResourceWithStreamingResponse(self._evaluations.evaluation_metrics)

    @cached_property
    def hybrid_eval_metrics(self) -> HybridEvalMetricsResourceWithStreamingResponse:
        return HybridEvalMetricsResourceWithStreamingResponse(self._evaluations.hybrid_eval_metrics)

    @cached_property
    def test_case_results(self) -> TestCaseResultsResourceWithStreamingResponse:
        return TestCaseResultsResourceWithStreamingResponse(self._evaluations.test_case_results)


class AsyncEvaluationsResourceWithStreamingResponse:
    def __init__(self, evaluations: AsyncEvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = async_to_streamed_response_wrapper(
            evaluations.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            evaluations.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            evaluations.update,
        )
        self.list = async_to_streamed_response_wrapper(
            evaluations.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            evaluations.delete,
        )
        self.claim_task = async_to_streamed_response_wrapper(
            evaluations.claim_task,
        )

    @cached_property
    def tasks(self) -> AsyncTasksResourceWithStreamingResponse:
        return AsyncTasksResourceWithStreamingResponse(self._evaluations.tasks)

    @cached_property
    def contributor_metrics(self) -> AsyncContributorMetricsResourceWithStreamingResponse:
        return AsyncContributorMetricsResourceWithStreamingResponse(self._evaluations.contributor_metrics)

    @cached_property
    def evaluation_metrics(self) -> AsyncEvaluationMetricsResourceWithStreamingResponse:
        return AsyncEvaluationMetricsResourceWithStreamingResponse(self._evaluations.evaluation_metrics)

    @cached_property
    def hybrid_eval_metrics(self) -> AsyncHybridEvalMetricsResourceWithStreamingResponse:
        return AsyncHybridEvalMetricsResourceWithStreamingResponse(self._evaluations.hybrid_eval_metrics)

    @cached_property
    def test_case_results(self) -> AsyncTestCaseResultsResourceWithStreamingResponse:
        return AsyncTestCaseResultsResourceWithStreamingResponse(self._evaluations.test_case_results)
