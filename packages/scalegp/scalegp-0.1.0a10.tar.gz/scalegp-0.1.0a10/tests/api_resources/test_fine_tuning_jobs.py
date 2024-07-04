# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import (
    FineTuningJobResponse,
    PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsFineTuningJobResponse,
)
from scalegp.types.shared import DeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFineTuningJobs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        fine_tuning_job = client.fine_tuning_jobs.create(
            account_id="string",
            training_dataset_id="string",
        )
        assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        fine_tuning_job = client.fine_tuning_jobs.create(
            account_id="string",
            training_dataset_id="string",
            base_model_id="string",
            fine_tuned_model_id="string",
            validation_dataset_id="string",
            vendor_configuration={
                "vendor": "LAUNCH",
                "hyperparameters": {},
                "wandb_config": {},
                "suffix": "string",
                "output": "string",
            },
            x_selected_account_id="string",
        )
        assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.fine_tuning_jobs.with_raw_response.create(
            account_id="string",
            training_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = response.parse()
        assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.fine_tuning_jobs.with_streaming_response.create(
            account_id="string",
            training_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = response.parse()
            assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        fine_tuning_job = client.fine_tuning_jobs.retrieve(
            "string",
        )
        assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.fine_tuning_jobs.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = response.parse()
        assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.fine_tuning_jobs.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = response.parse()
            assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fine_tuning_job_id` but received ''"):
            client.fine_tuning_jobs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        fine_tuning_job = client.fine_tuning_jobs.list()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsFineTuningJobResponse,
            fine_tuning_job,
            path=["response"],
        )

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        fine_tuning_job = client.fine_tuning_jobs.list(
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsFineTuningJobResponse,
            fine_tuning_job,
            path=["response"],
        )

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.fine_tuning_jobs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = response.parse()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsFineTuningJobResponse,
            fine_tuning_job,
            path=["response"],
        )

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.fine_tuning_jobs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = response.parse()
            assert_matches_type(
                PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsFineTuningJobResponse,
                fine_tuning_job,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        fine_tuning_job = client.fine_tuning_jobs.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, fine_tuning_job, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.fine_tuning_jobs.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = response.parse()
        assert_matches_type(DeleteResponse, fine_tuning_job, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.fine_tuning_jobs.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = response.parse()
            assert_matches_type(DeleteResponse, fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fine_tuning_job_id` but received ''"):
            client.fine_tuning_jobs.with_raw_response.delete(
                "",
            )


class TestAsyncFineTuningJobs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        fine_tuning_job = await async_client.fine_tuning_jobs.create(
            account_id="string",
            training_dataset_id="string",
        )
        assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        fine_tuning_job = await async_client.fine_tuning_jobs.create(
            account_id="string",
            training_dataset_id="string",
            base_model_id="string",
            fine_tuned_model_id="string",
            validation_dataset_id="string",
            vendor_configuration={
                "vendor": "LAUNCH",
                "hyperparameters": {},
                "wandb_config": {},
                "suffix": "string",
                "output": "string",
            },
            x_selected_account_id="string",
        )
        assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.fine_tuning_jobs.with_raw_response.create(
            account_id="string",
            training_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = await response.parse()
        assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.fine_tuning_jobs.with_streaming_response.create(
            account_id="string",
            training_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = await response.parse()
            assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        fine_tuning_job = await async_client.fine_tuning_jobs.retrieve(
            "string",
        )
        assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.fine_tuning_jobs.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = await response.parse()
        assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.fine_tuning_jobs.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = await response.parse()
            assert_matches_type(FineTuningJobResponse, fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fine_tuning_job_id` but received ''"):
            await async_client.fine_tuning_jobs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        fine_tuning_job = await async_client.fine_tuning_jobs.list()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsFineTuningJobResponse,
            fine_tuning_job,
            path=["response"],
        )

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        fine_tuning_job = await async_client.fine_tuning_jobs.list(
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsFineTuningJobResponse,
            fine_tuning_job,
            path=["response"],
        )

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.fine_tuning_jobs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = await response.parse()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsFineTuningJobResponse,
            fine_tuning_job,
            path=["response"],
        )

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.fine_tuning_jobs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = await response.parse()
            assert_matches_type(
                PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsFineTuningJobResponse,
                fine_tuning_job,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        fine_tuning_job = await async_client.fine_tuning_jobs.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, fine_tuning_job, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.fine_tuning_jobs.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tuning_job = await response.parse()
        assert_matches_type(DeleteResponse, fine_tuning_job, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.fine_tuning_jobs.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tuning_job = await response.parse()
            assert_matches_type(DeleteResponse, fine_tuning_job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fine_tuning_job_id` but received ''"):
            await async_client.fine_tuning_jobs.with_raw_response.delete(
                "",
            )
