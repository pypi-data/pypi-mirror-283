# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import (
    TrainingDatasetResponse,
    PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse,
)
from scalegp.types.shared import DeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTrainingDatasets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        training_dataset = client.training_datasets.create(
            account_id="string",
            file=b"raw file contents",
            name="string",
            schema_type="GENERATION",
        )
        assert_matches_type(TrainingDatasetResponse, training_dataset, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.training_datasets.with_raw_response.create(
            account_id="string",
            file=b"raw file contents",
            name="string",
            schema_type="GENERATION",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = response.parse()
        assert_matches_type(TrainingDatasetResponse, training_dataset, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.training_datasets.with_streaming_response.create(
            account_id="string",
            file=b"raw file contents",
            name="string",
            schema_type="GENERATION",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = response.parse()
            assert_matches_type(TrainingDatasetResponse, training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        training_dataset = client.training_datasets.retrieve(
            "string",
        )
        assert_matches_type(TrainingDatasetResponse, training_dataset, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.training_datasets.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = response.parse()
        assert_matches_type(TrainingDatasetResponse, training_dataset, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.training_datasets.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = response.parse()
            assert_matches_type(TrainingDatasetResponse, training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `training_dataset_id` but received ''"):
            client.training_datasets.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        training_dataset = client.training_datasets.list()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse,
            training_dataset,
            path=["response"],
        )

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        training_dataset = client.training_datasets.list(
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse,
            training_dataset,
            path=["response"],
        )

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.training_datasets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = response.parse()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse,
            training_dataset,
            path=["response"],
        )

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.training_datasets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = response.parse()
            assert_matches_type(
                PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse,
                training_dataset,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        training_dataset = client.training_datasets.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, training_dataset, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.training_datasets.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = response.parse()
        assert_matches_type(DeleteResponse, training_dataset, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.training_datasets.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = response.parse()
            assert_matches_type(DeleteResponse, training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `training_dataset_id` but received ''"):
            client.training_datasets.with_raw_response.delete(
                "",
            )


class TestAsyncTrainingDatasets:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        training_dataset = await async_client.training_datasets.create(
            account_id="string",
            file=b"raw file contents",
            name="string",
            schema_type="GENERATION",
        )
        assert_matches_type(TrainingDatasetResponse, training_dataset, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.training_datasets.with_raw_response.create(
            account_id="string",
            file=b"raw file contents",
            name="string",
            schema_type="GENERATION",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = await response.parse()
        assert_matches_type(TrainingDatasetResponse, training_dataset, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.training_datasets.with_streaming_response.create(
            account_id="string",
            file=b"raw file contents",
            name="string",
            schema_type="GENERATION",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = await response.parse()
            assert_matches_type(TrainingDatasetResponse, training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        training_dataset = await async_client.training_datasets.retrieve(
            "string",
        )
        assert_matches_type(TrainingDatasetResponse, training_dataset, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.training_datasets.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = await response.parse()
        assert_matches_type(TrainingDatasetResponse, training_dataset, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.training_datasets.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = await response.parse()
            assert_matches_type(TrainingDatasetResponse, training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `training_dataset_id` but received ''"):
            await async_client.training_datasets.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        training_dataset = await async_client.training_datasets.list()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse,
            training_dataset,
            path=["response"],
        )

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        training_dataset = await async_client.training_datasets.list(
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse,
            training_dataset,
            path=["response"],
        )

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.training_datasets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = await response.parse()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse,
            training_dataset,
            path=["response"],
        )

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.training_datasets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = await response.parse()
            assert_matches_type(
                PaginationResponseListEgpAPIBackendServerAPIModelsFineTuningJobModelsTrainingDatasetResponse,
                training_dataset,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        training_dataset = await async_client.training_datasets.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, training_dataset, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.training_datasets.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = await response.parse()
        assert_matches_type(DeleteResponse, training_dataset, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.training_datasets.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = await response.parse()
            assert_matches_type(DeleteResponse, training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `training_dataset_id` but received ''"):
            await async_client.training_datasets.with_raw_response.delete(
                "",
            )
