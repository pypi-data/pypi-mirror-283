# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import (
    EvaluationResponse,
    EvaluationListResponse,
    EvaluationResponseWithViews,
)
from scalegp.types.shared import TaskResponse, DeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_overload_1(self, client: SGP) -> None:
        evaluation = client.evaluations.create(
            account_id="string",
            application_spec_id="string",
            application_variant_id="string",
            description="string",
            evaluation_dataset_id="string",
            name="string",
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: SGP) -> None:
        evaluation = client.evaluations.create(
            account_id="string",
            application_spec_id="string",
            application_variant_id="string",
            description="string",
            evaluation_dataset_id="string",
            name="string",
            evaluation_config={},
            evaluation_config_id="string",
            evaluation_dataset_version=0,
            tags={},
            type="builder",
            x_selected_account_id="string",
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_create_overload_1(self, client: SGP) -> None:
        response = client.evaluations.with_raw_response.create(
            account_id="string",
            application_spec_id="string",
            application_variant_id="string",
            description="string",
            evaluation_dataset_id="string",
            name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_1(self, client: SGP) -> None:
        with client.evaluations.with_streaming_response.create(
            account_id="string",
            application_spec_id="string",
            application_variant_id="string",
            description="string",
            evaluation_dataset_id="string",
            name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_overload_2(self, client: SGP) -> None:
        evaluation = client.evaluations.create(
            account_id="string",
            application_spec_id="string",
            description="string",
            name="string",
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: SGP) -> None:
        evaluation = client.evaluations.create(
            account_id="string",
            application_spec_id="string",
            description="string",
            name="string",
            application_variant_id="string",
            evaluation_config={},
            evaluation_config_id="string",
            tags={},
            type="default",
            x_selected_account_id="string",
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_create_overload_2(self, client: SGP) -> None:
        response = client.evaluations.with_raw_response.create(
            account_id="string",
            application_spec_id="string",
            description="string",
            name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_2(self, client: SGP) -> None:
        with client.evaluations.with_streaming_response.create(
            account_id="string",
            application_spec_id="string",
            description="string",
            name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        evaluation = client.evaluations.retrieve(
            "string",
        )
        assert_matches_type(EvaluationResponseWithViews, evaluation, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGP) -> None:
        evaluation = client.evaluations.retrieve(
            "string",
            view=["ApplicationSpec", "AsyncJobs", "EvaluationConfig"],
        )
        assert_matches_type(EvaluationResponseWithViews, evaluation, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.evaluations.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationResponseWithViews, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.evaluations.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationResponseWithViews, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update_overload_1(self, client: SGP) -> None:
        evaluation = client.evaluations.update(
            "string",
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    def test_method_update_with_all_params_overload_1(self, client: SGP) -> None:
        evaluation = client.evaluations.update(
            "string",
            application_spec_id="string",
            application_variant_id="string",
            description="string",
            evaluation_config={},
            evaluation_config_id="string",
            evaluation_type="llm_benchmark",
            name="string",
            restore=True,
            tags={},
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_update_overload_1(self, client: SGP) -> None:
        response = client.evaluations.with_raw_response.update(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_update_overload_1(self, client: SGP) -> None:
        with client.evaluations.with_streaming_response.update(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_overload_1(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.update(
                "",
            )

    @parametrize
    def test_method_update_overload_2(self, client: SGP) -> None:
        evaluation = client.evaluations.update(
            "string",
            restore=True,
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_update_overload_2(self, client: SGP) -> None:
        response = client.evaluations.with_raw_response.update(
            "string",
            restore=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_update_overload_2(self, client: SGP) -> None:
        with client.evaluations.with_streaming_response.update(
            "string",
            restore=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_overload_2(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.update(
                "",
                restore=True,
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        evaluation = client.evaluations.list()
        assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        evaluation = client.evaluations.list(
            account_id="string",
            include_archived=True,
            limit=1,
            page=1,
            sort_by=["status:asc", "status:desc", "application_spec_id:asc"],
            view=["ApplicationSpec", "AsyncJobs", "EvaluationConfig"],
            x_selected_account_id="string",
        )
        assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.evaluations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.evaluations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        evaluation = client.evaluations.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.evaluations.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(DeleteResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.evaluations.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(DeleteResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_claim_task(self, client: SGP) -> None:
        evaluation = client.evaluations.claim_task(
            "string",
        )
        assert_matches_type(TaskResponse, evaluation, path=["response"])

    @parametrize
    def test_method_claim_task_with_all_params(self, client: SGP) -> None:
        evaluation = client.evaluations.claim_task(
            "string",
            x_selected_account_id="string",
        )
        assert_matches_type(TaskResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_claim_task(self, client: SGP) -> None:
        response = client.evaluations.with_raw_response.claim_task(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(TaskResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_claim_task(self, client: SGP) -> None:
        with client.evaluations.with_streaming_response.claim_task(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(TaskResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_claim_task(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.claim_task(
                "",
            )


class TestAsyncEvaluations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.create(
            account_id="string",
            application_spec_id="string",
            application_variant_id="string",
            description="string",
            evaluation_dataset_id="string",
            name="string",
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.create(
            account_id="string",
            application_spec_id="string",
            application_variant_id="string",
            description="string",
            evaluation_dataset_id="string",
            name="string",
            evaluation_config={},
            evaluation_config_id="string",
            evaluation_dataset_version=0,
            tags={},
            type="builder",
            x_selected_account_id="string",
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.with_raw_response.create(
            account_id="string",
            application_spec_id="string",
            application_variant_id="string",
            description="string",
            evaluation_dataset_id="string",
            name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.with_streaming_response.create(
            account_id="string",
            application_spec_id="string",
            application_variant_id="string",
            description="string",
            evaluation_dataset_id="string",
            name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.create(
            account_id="string",
            application_spec_id="string",
            description="string",
            name="string",
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.create(
            account_id="string",
            application_spec_id="string",
            description="string",
            name="string",
            application_variant_id="string",
            evaluation_config={},
            evaluation_config_id="string",
            tags={},
            type="default",
            x_selected_account_id="string",
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.with_raw_response.create(
            account_id="string",
            application_spec_id="string",
            description="string",
            name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.with_streaming_response.create(
            account_id="string",
            application_spec_id="string",
            description="string",
            name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.retrieve(
            "string",
        )
        assert_matches_type(EvaluationResponseWithViews, evaluation, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.retrieve(
            "string",
            view=["ApplicationSpec", "AsyncJobs", "EvaluationConfig"],
        )
        assert_matches_type(EvaluationResponseWithViews, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationResponseWithViews, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationResponseWithViews, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update_overload_1(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.update(
            "string",
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    async def test_method_update_with_all_params_overload_1(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.update(
            "string",
            application_spec_id="string",
            application_variant_id="string",
            description="string",
            evaluation_config={},
            evaluation_config_id="string",
            evaluation_type="llm_benchmark",
            name="string",
            restore=True,
            tags={},
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_update_overload_1(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.with_raw_response.update(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_update_overload_1(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.with_streaming_response.update(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_overload_1(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.update(
                "",
            )

    @parametrize
    async def test_method_update_overload_2(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.update(
            "string",
            restore=True,
        )
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_update_overload_2(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.with_raw_response.update(
            "string",
            restore=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_update_overload_2(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.with_streaming_response.update(
            "string",
            restore=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_overload_2(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.update(
                "",
                restore=True,
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.list()
        assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.list(
            account_id="string",
            include_archived=True,
            limit=1,
            page=1,
            sort_by=["status:asc", "status:desc", "application_spec_id:asc"],
            view=["ApplicationSpec", "AsyncJobs", "EvaluationConfig"],
            x_selected_account_id="string",
        )
        assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(DeleteResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(DeleteResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_claim_task(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.claim_task(
            "string",
        )
        assert_matches_type(TaskResponse, evaluation, path=["response"])

    @parametrize
    async def test_method_claim_task_with_all_params(self, async_client: AsyncSGP) -> None:
        evaluation = await async_client.evaluations.claim_task(
            "string",
            x_selected_account_id="string",
        )
        assert_matches_type(TaskResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_claim_task(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.with_raw_response.claim_task(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(TaskResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_claim_task(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.with_streaming_response.claim_task(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(TaskResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_claim_task(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.claim_task(
                "",
            )
