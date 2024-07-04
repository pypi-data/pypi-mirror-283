# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.fine_tuning_jobs import EventListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        event = client.fine_tuning_jobs.events.list(
            "string",
        )
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.fine_tuning_jobs.events.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.fine_tuning_jobs.events.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(EventListResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fine_tuning_job_id` but received ''"):
            client.fine_tuning_jobs.events.with_raw_response.list(
                "",
            )


class TestAsyncEvents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        event = await async_client.fine_tuning_jobs.events.list(
            "string",
        )
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.fine_tuning_jobs.events.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.fine_tuning_jobs.events.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(EventListResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fine_tuning_job_id` but received ''"):
            await async_client.fine_tuning_jobs.events.with_raw_response.list(
                "",
            )
