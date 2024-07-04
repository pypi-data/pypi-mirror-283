# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import (
    EvaluationConfigResponse,
    PaginationResponseEvaluationConfig,
)
from scalegp.types.shared import DeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluationConfigs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        evaluation_config = client.evaluation_configs.create(
            account_id="string",
            evaluation_type="studio",
            question_set_id="string",
        )
        assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        evaluation_config = client.evaluation_configs.create(
            account_id="string",
            evaluation_type="studio",
            question_set_id="string",
            studio_project_id="string",
            x_selected_account_id="string",
        )
        assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.evaluation_configs.with_raw_response.create(
            account_id="string",
            evaluation_type="studio",
            question_set_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = response.parse()
        assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.evaluation_configs.with_streaming_response.create(
            account_id="string",
            evaluation_type="studio",
            question_set_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = response.parse()
            assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        evaluation_config = client.evaluation_configs.retrieve(
            "string",
        )
        assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.evaluation_configs.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = response.parse()
        assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.evaluation_configs.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = response.parse()
            assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_config_id` but received ''"):
            client.evaluation_configs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        evaluation_config = client.evaluation_configs.list()
        assert_matches_type(PaginationResponseEvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        evaluation_config = client.evaluation_configs.list(
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(PaginationResponseEvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.evaluation_configs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = response.parse()
        assert_matches_type(PaginationResponseEvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.evaluation_configs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = response.parse()
            assert_matches_type(PaginationResponseEvaluationConfig, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        evaluation_config = client.evaluation_configs.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, evaluation_config, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.evaluation_configs.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = response.parse()
        assert_matches_type(DeleteResponse, evaluation_config, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.evaluation_configs.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = response.parse()
            assert_matches_type(DeleteResponse, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_config_id` but received ''"):
            client.evaluation_configs.with_raw_response.delete(
                "",
            )


class TestAsyncEvaluationConfigs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        evaluation_config = await async_client.evaluation_configs.create(
            account_id="string",
            evaluation_type="studio",
            question_set_id="string",
        )
        assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        evaluation_config = await async_client.evaluation_configs.create(
            account_id="string",
            evaluation_type="studio",
            question_set_id="string",
            studio_project_id="string",
            x_selected_account_id="string",
        )
        assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_configs.with_raw_response.create(
            account_id="string",
            evaluation_type="studio",
            question_set_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = await response.parse()
        assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_configs.with_streaming_response.create(
            account_id="string",
            evaluation_type="studio",
            question_set_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = await response.parse()
            assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        evaluation_config = await async_client.evaluation_configs.retrieve(
            "string",
        )
        assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_configs.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = await response.parse()
        assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_configs.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = await response.parse()
            assert_matches_type(EvaluationConfigResponse, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_config_id` but received ''"):
            await async_client.evaluation_configs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        evaluation_config = await async_client.evaluation_configs.list()
        assert_matches_type(PaginationResponseEvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        evaluation_config = await async_client.evaluation_configs.list(
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(PaginationResponseEvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_configs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = await response.parse()
        assert_matches_type(PaginationResponseEvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_configs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = await response.parse()
            assert_matches_type(PaginationResponseEvaluationConfig, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        evaluation_config = await async_client.evaluation_configs.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, evaluation_config, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_configs.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = await response.parse()
        assert_matches_type(DeleteResponse, evaluation_config, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_configs.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = await response.parse()
            assert_matches_type(DeleteResponse, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_config_id` but received ''"):
            await async_client.evaluation_configs.with_raw_response.delete(
                "",
            )
