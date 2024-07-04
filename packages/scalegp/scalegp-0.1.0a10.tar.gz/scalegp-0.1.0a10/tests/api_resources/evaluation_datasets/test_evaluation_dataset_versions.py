# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.evaluation_datasets import (
    EvaluationDatasetVersionResponse,
    EvaluationDatasetVersionListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluationDatasetVersions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        evaluation_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.create(
            "string",
        )
        assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        evaluation_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.create(
            "string",
            account_id="string",
            x_selected_account_id="string",
        )
        assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.create(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = response.parse()
        assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.create(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = response.parse()
            assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.create(
                "",
            )

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        evaluation_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.retrieve(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.retrieve(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = response.parse()
        assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.retrieve(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = response.parse()
            assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.retrieve(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `evaluation_dataset_version_id` but received ''"
        ):
            client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.retrieve(
                "",
                evaluation_dataset_id="string",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        evaluation_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.list(
            "string",
        )
        assert_matches_type(EvaluationDatasetVersionListResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        evaluation_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.list(
            "string",
            account_id="string",
            include_archived=True,
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(EvaluationDatasetVersionListResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = response.parse()
        assert_matches_type(EvaluationDatasetVersionListResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = response.parse()
            assert_matches_type(EvaluationDatasetVersionListResponse, evaluation_dataset_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.list(
                "",
            )


class TestAsyncEvaluationDatasetVersions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        evaluation_dataset_version = await async_client.evaluation_datasets.evaluation_dataset_versions.create(
            "string",
        )
        assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        evaluation_dataset_version = await async_client.evaluation_datasets.evaluation_dataset_versions.create(
            "string",
            account_id="string",
            x_selected_account_id="string",
        )
        assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.create(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = await response.parse()
        assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.create(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = await response.parse()
            assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.create(
                "",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        evaluation_dataset_version = await async_client.evaluation_datasets.evaluation_dataset_versions.retrieve(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.retrieve(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = await response.parse()
        assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.retrieve(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = await response.parse()
            assert_matches_type(EvaluationDatasetVersionResponse, evaluation_dataset_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.retrieve(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `evaluation_dataset_version_id` but received ''"
        ):
            await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.retrieve(
                "",
                evaluation_dataset_id="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        evaluation_dataset_version = await async_client.evaluation_datasets.evaluation_dataset_versions.list(
            "string",
        )
        assert_matches_type(EvaluationDatasetVersionListResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        evaluation_dataset_version = await async_client.evaluation_datasets.evaluation_dataset_versions.list(
            "string",
            account_id="string",
            include_archived=True,
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(EvaluationDatasetVersionListResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = await response.parse()
        assert_matches_type(EvaluationDatasetVersionListResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = await response.parse()
            assert_matches_type(EvaluationDatasetVersionListResponse, evaluation_dataset_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.list(
                "",
            )
