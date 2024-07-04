# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.evaluation_datasets import (
    GetEvaluationDatasetGenerationJobResponse,
    ListEvaluationDatasetGenerationJobsResponse,
    CreateEvaluationDatasetGenerationJobResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestGenerationJobs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        generation_job = client.evaluation_datasets.generation_jobs.create(
            "string",
        )
        assert_matches_type(CreateEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        generation_job = client.evaluation_datasets.generation_jobs.create(
            "string",
            num_test_cases=0,
            x_selected_account_id="string",
        )
        assert_matches_type(CreateEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.evaluation_datasets.generation_jobs.with_raw_response.create(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = response.parse()
        assert_matches_type(CreateEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.evaluation_datasets.generation_jobs.with_streaming_response.create(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = response.parse()
            assert_matches_type(CreateEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.generation_jobs.with_raw_response.create(
                "",
            )

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        generation_job = client.evaluation_datasets.generation_jobs.retrieve(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(GetEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGP) -> None:
        generation_job = client.evaluation_datasets.generation_jobs.retrieve(
            "string",
            evaluation_dataset_id="string",
            x_selected_account_id="string",
        )
        assert_matches_type(GetEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.evaluation_datasets.generation_jobs.with_raw_response.retrieve(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = response.parse()
        assert_matches_type(GetEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.evaluation_datasets.generation_jobs.with_streaming_response.retrieve(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = response.parse()
            assert_matches_type(GetEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.generation_jobs.with_raw_response.retrieve(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `generation_job_id` but received ''"):
            client.evaluation_datasets.generation_jobs.with_raw_response.retrieve(
                "",
                evaluation_dataset_id="string",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        generation_job = client.evaluation_datasets.generation_jobs.list(
            "string",
        )
        assert_matches_type(ListEvaluationDatasetGenerationJobsResponse, generation_job, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        generation_job = client.evaluation_datasets.generation_jobs.list(
            "string",
            x_selected_account_id="string",
        )
        assert_matches_type(ListEvaluationDatasetGenerationJobsResponse, generation_job, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.evaluation_datasets.generation_jobs.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = response.parse()
        assert_matches_type(ListEvaluationDatasetGenerationJobsResponse, generation_job, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.evaluation_datasets.generation_jobs.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = response.parse()
            assert_matches_type(ListEvaluationDatasetGenerationJobsResponse, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.generation_jobs.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_cancel(self, client: SGP) -> None:
        generation_job = client.evaluation_datasets.generation_jobs.cancel(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(object, generation_job, path=["response"])

    @parametrize
    def test_method_cancel_with_all_params(self, client: SGP) -> None:
        generation_job = client.evaluation_datasets.generation_jobs.cancel(
            "string",
            evaluation_dataset_id="string",
            x_selected_account_id="string",
        )
        assert_matches_type(object, generation_job, path=["response"])

    @parametrize
    def test_raw_response_cancel(self, client: SGP) -> None:
        response = client.evaluation_datasets.generation_jobs.with_raw_response.cancel(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = response.parse()
        assert_matches_type(object, generation_job, path=["response"])

    @parametrize
    def test_streaming_response_cancel(self, client: SGP) -> None:
        with client.evaluation_datasets.generation_jobs.with_streaming_response.cancel(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = response.parse()
            assert_matches_type(object, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_cancel(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.generation_jobs.with_raw_response.cancel(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `generation_job_id` but received ''"):
            client.evaluation_datasets.generation_jobs.with_raw_response.cancel(
                "",
                evaluation_dataset_id="string",
            )


class TestAsyncGenerationJobs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        generation_job = await async_client.evaluation_datasets.generation_jobs.create(
            "string",
        )
        assert_matches_type(CreateEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        generation_job = await async_client.evaluation_datasets.generation_jobs.create(
            "string",
            num_test_cases=0,
            x_selected_account_id="string",
        )
        assert_matches_type(CreateEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.generation_jobs.with_raw_response.create(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = await response.parse()
        assert_matches_type(CreateEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.generation_jobs.with_streaming_response.create(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = await response.parse()
            assert_matches_type(CreateEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.generation_jobs.with_raw_response.create(
                "",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        generation_job = await async_client.evaluation_datasets.generation_jobs.retrieve(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(GetEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGP) -> None:
        generation_job = await async_client.evaluation_datasets.generation_jobs.retrieve(
            "string",
            evaluation_dataset_id="string",
            x_selected_account_id="string",
        )
        assert_matches_type(GetEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.generation_jobs.with_raw_response.retrieve(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = await response.parse()
        assert_matches_type(GetEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.generation_jobs.with_streaming_response.retrieve(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = await response.parse()
            assert_matches_type(GetEvaluationDatasetGenerationJobResponse, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.generation_jobs.with_raw_response.retrieve(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `generation_job_id` but received ''"):
            await async_client.evaluation_datasets.generation_jobs.with_raw_response.retrieve(
                "",
                evaluation_dataset_id="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        generation_job = await async_client.evaluation_datasets.generation_jobs.list(
            "string",
        )
        assert_matches_type(ListEvaluationDatasetGenerationJobsResponse, generation_job, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        generation_job = await async_client.evaluation_datasets.generation_jobs.list(
            "string",
            x_selected_account_id="string",
        )
        assert_matches_type(ListEvaluationDatasetGenerationJobsResponse, generation_job, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.generation_jobs.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = await response.parse()
        assert_matches_type(ListEvaluationDatasetGenerationJobsResponse, generation_job, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.generation_jobs.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = await response.parse()
            assert_matches_type(ListEvaluationDatasetGenerationJobsResponse, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.generation_jobs.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_cancel(self, async_client: AsyncSGP) -> None:
        generation_job = await async_client.evaluation_datasets.generation_jobs.cancel(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(object, generation_job, path=["response"])

    @parametrize
    async def test_method_cancel_with_all_params(self, async_client: AsyncSGP) -> None:
        generation_job = await async_client.evaluation_datasets.generation_jobs.cancel(
            "string",
            evaluation_dataset_id="string",
            x_selected_account_id="string",
        )
        assert_matches_type(object, generation_job, path=["response"])

    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.generation_jobs.with_raw_response.cancel(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        generation_job = await response.parse()
        assert_matches_type(object, generation_job, path=["response"])

    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.generation_jobs.with_streaming_response.cancel(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            generation_job = await response.parse()
            assert_matches_type(object, generation_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.generation_jobs.with_raw_response.cancel(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `generation_job_id` but received ''"):
            await async_client.evaluation_datasets.generation_jobs.with_raw_response.cancel(
                "",
                evaluation_dataset_id="string",
            )
