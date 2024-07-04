# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.shared import TaskResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTasks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update(self, client: SGP) -> None:
        task = client.evaluations.tasks.update(
            "string",
            evaluation_id="string",
        )
        assert_matches_type(TaskResponse, task, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGP) -> None:
        task = client.evaluations.tasks.update(
            "string",
            evaluation_id="string",
            assigned_to="string",
            x_selected_account_id="string",
        )
        assert_matches_type(TaskResponse, task, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGP) -> None:
        response = client.evaluations.tasks.with_raw_response.update(
            "string",
            evaluation_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskResponse, task, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGP) -> None:
        with client.evaluations.tasks.with_streaming_response.update(
            "string",
            evaluation_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.tasks.with_raw_response.update(
                "string",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.evaluations.tasks.with_raw_response.update(
                "",
                evaluation_id="string",
            )


class TestAsyncTasks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_update(self, async_client: AsyncSGP) -> None:
        task = await async_client.evaluations.tasks.update(
            "string",
            evaluation_id="string",
        )
        assert_matches_type(TaskResponse, task, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGP) -> None:
        task = await async_client.evaluations.tasks.update(
            "string",
            evaluation_id="string",
            assigned_to="string",
            x_selected_account_id="string",
        )
        assert_matches_type(TaskResponse, task, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.tasks.with_raw_response.update(
            "string",
            evaluation_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskResponse, task, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.tasks.with_streaming_response.update(
            "string",
            evaluation_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.tasks.with_raw_response.update(
                "string",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.evaluations.tasks.with_raw_response.update(
                "",
                evaluation_id="string",
            )
