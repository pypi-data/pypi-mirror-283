# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Mapping, cast
from typing_extensions import Literal

import httpx

from ...types import training_dataset_list_params, training_dataset_create_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven, FileTypes
from ..._utils import (
    extract_files,
    maybe_transform,
    strip_not_given,
    deepcopy_minimal,
    async_maybe_transform,
)
from .contents import (
    ContentsResource,
    AsyncContentsResource,
    ContentsResourceWithRawResponse,
    AsyncContentsResourceWithRawResponse,
    ContentsResourceWithStreamingResponse,
    AsyncContentsResourceWithStreamingResponse,
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
from ...types.shared.delete_response import DeleteResponse
from ...types.training_dataset_response import TrainingDatasetResponse
from ...types.pagination_response_list_egp_api_backend_server_api_models_fine_tuning_job_models_training_dataset_response import (
    PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse,
)

__all__ = ["TrainingDatasetsResource", "AsyncTrainingDatasetsResource"]


class TrainingDatasetsResource(SyncAPIResource):
    @cached_property
    def contents(self) -> ContentsResource:
        return ContentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> TrainingDatasetsResourceWithRawResponse:
        return TrainingDatasetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TrainingDatasetsResourceWithStreamingResponse:
        return TrainingDatasetsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        file: FileTypes,
        name: str,
        schema_type: Literal["GENERATION", "RERANKING_QUESTIONS"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TrainingDatasetResponse:
        """
        Create Training Dataset

        Args:
          account_id: The ID of the account that owns the given entity.

          file: The file to upload as the training dataset

          name: The name of the dataset

          schema_type: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal(
            {
                "account_id": account_id,
                "file": file,
                "name": name,
                "schema_type": schema_type,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/v4/training-datasets",
            body=maybe_transform(body, training_dataset_create_params.TrainingDatasetCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrainingDatasetResponse,
        )

    def retrieve(
        self,
        training_dataset_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TrainingDatasetResponse:
        """
        ### Description

        Gets the details of a training dataset

        ### Details

        This API can be used to get information about a single training dataset by ID.
        To use this API, pass in the `id` that was returned from your Create Training
        Dataset API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `training_dataset_id` but received {training_dataset_id!r}"
            )
        return self._get(
            f"/v4/training-datasets/{training_dataset_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrainingDatasetResponse,
        )

    def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse:
        """
        ### Description

        Lists all training datasets accessible to the user.

        ### Details

        This API can be used to list training datasets. If a user has access to multiple
        accounts, all training datasets from all accounts the user is associated with
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
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return self._get(
            "/v4/training-datasets",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                    },
                    training_dataset_list_params.TrainingDatasetListParams,
                ),
            ),
            cast_to=PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse,
        )

    def delete(
        self,
        training_dataset_id: str,
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

        Deletes a training dataset

        ### Details

        This API can be used to delete a training dataset by ID. To use this API, pass
        in the `id` that was returned from your Create Training Dataset API call as a
        path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `training_dataset_id` but received {training_dataset_id!r}"
            )
        return self._delete(
            f"/v4/training-datasets/{training_dataset_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )


class AsyncTrainingDatasetsResource(AsyncAPIResource):
    @cached_property
    def contents(self) -> AsyncContentsResource:
        return AsyncContentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTrainingDatasetsResourceWithRawResponse:
        return AsyncTrainingDatasetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTrainingDatasetsResourceWithStreamingResponse:
        return AsyncTrainingDatasetsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        file: FileTypes,
        name: str,
        schema_type: Literal["GENERATION", "RERANKING_QUESTIONS"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TrainingDatasetResponse:
        """
        Create Training Dataset

        Args:
          account_id: The ID of the account that owns the given entity.

          file: The file to upload as the training dataset

          name: The name of the dataset

          schema_type: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal(
            {
                "account_id": account_id,
                "file": file,
                "name": name,
                "schema_type": schema_type,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/v4/training-datasets",
            body=await async_maybe_transform(body, training_dataset_create_params.TrainingDatasetCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrainingDatasetResponse,
        )

    async def retrieve(
        self,
        training_dataset_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TrainingDatasetResponse:
        """
        ### Description

        Gets the details of a training dataset

        ### Details

        This API can be used to get information about a single training dataset by ID.
        To use this API, pass in the `id` that was returned from your Create Training
        Dataset API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `training_dataset_id` but received {training_dataset_id!r}"
            )
        return await self._get(
            f"/v4/training-datasets/{training_dataset_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrainingDatasetResponse,
        )

    async def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse:
        """
        ### Description

        Lists all training datasets accessible to the user.

        ### Details

        This API can be used to list training datasets. If a user has access to multiple
        accounts, all training datasets from all accounts the user is associated with
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
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return await self._get(
            "/v4/training-datasets",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                    },
                    training_dataset_list_params.TrainingDatasetListParams,
                ),
            ),
            cast_to=PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse,
        )

    async def delete(
        self,
        training_dataset_id: str,
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

        Deletes a training dataset

        ### Details

        This API can be used to delete a training dataset by ID. To use this API, pass
        in the `id` that was returned from your Create Training Dataset API call as a
        path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `training_dataset_id` but received {training_dataset_id!r}"
            )
        return await self._delete(
            f"/v4/training-datasets/{training_dataset_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )


class TrainingDatasetsResourceWithRawResponse:
    def __init__(self, training_datasets: TrainingDatasetsResource) -> None:
        self._training_datasets = training_datasets

        self.create = to_raw_response_wrapper(
            training_datasets.create,
        )
        self.retrieve = to_raw_response_wrapper(
            training_datasets.retrieve,
        )
        self.list = to_raw_response_wrapper(
            training_datasets.list,
        )
        self.delete = to_raw_response_wrapper(
            training_datasets.delete,
        )

    @cached_property
    def contents(self) -> ContentsResourceWithRawResponse:
        return ContentsResourceWithRawResponse(self._training_datasets.contents)


class AsyncTrainingDatasetsResourceWithRawResponse:
    def __init__(self, training_datasets: AsyncTrainingDatasetsResource) -> None:
        self._training_datasets = training_datasets

        self.create = async_to_raw_response_wrapper(
            training_datasets.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            training_datasets.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            training_datasets.list,
        )
        self.delete = async_to_raw_response_wrapper(
            training_datasets.delete,
        )

    @cached_property
    def contents(self) -> AsyncContentsResourceWithRawResponse:
        return AsyncContentsResourceWithRawResponse(self._training_datasets.contents)


class TrainingDatasetsResourceWithStreamingResponse:
    def __init__(self, training_datasets: TrainingDatasetsResource) -> None:
        self._training_datasets = training_datasets

        self.create = to_streamed_response_wrapper(
            training_datasets.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            training_datasets.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            training_datasets.list,
        )
        self.delete = to_streamed_response_wrapper(
            training_datasets.delete,
        )

    @cached_property
    def contents(self) -> ContentsResourceWithStreamingResponse:
        return ContentsResourceWithStreamingResponse(self._training_datasets.contents)


class AsyncTrainingDatasetsResourceWithStreamingResponse:
    def __init__(self, training_datasets: AsyncTrainingDatasetsResource) -> None:
        self._training_datasets = training_datasets

        self.create = async_to_streamed_response_wrapper(
            training_datasets.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            training_datasets.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            training_datasets.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            training_datasets.delete,
        )

    @cached_property
    def contents(self) -> AsyncContentsResourceWithStreamingResponse:
        return AsyncContentsResourceWithStreamingResponse(self._training_datasets.contents)
