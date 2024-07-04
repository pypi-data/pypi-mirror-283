# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.applications.variant import ChatThread

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestThreads:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update(self, client: SGP) -> None:
        thread = client.threads.update(
            "string",
        )
        assert_matches_type(ChatThread, thread, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGP) -> None:
        thread = client.threads.update(
            "string",
            archived_at="string",
            title="string",
        )
        assert_matches_type(ChatThread, thread, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGP) -> None:
        response = client.threads.with_raw_response.update(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(ChatThread, thread, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGP) -> None:
        with client.threads.with_streaming_response.update(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(ChatThread, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.with_raw_response.update(
                "",
            )

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        thread = client.threads.delete(
            "string",
        )
        assert_matches_type(object, thread, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.threads.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(object, thread, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.threads.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(object, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.with_raw_response.delete(
                "",
            )


class TestAsyncThreads:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_update(self, async_client: AsyncSGP) -> None:
        thread = await async_client.threads.update(
            "string",
        )
        assert_matches_type(ChatThread, thread, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGP) -> None:
        thread = await async_client.threads.update(
            "string",
            archived_at="string",
            title="string",
        )
        assert_matches_type(ChatThread, thread, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGP) -> None:
        response = await async_client.threads.with_raw_response.update(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(ChatThread, thread, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGP) -> None:
        async with async_client.threads.with_streaming_response.update(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(ChatThread, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.with_raw_response.update(
                "",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        thread = await async_client.threads.delete(
            "string",
        )
        assert_matches_type(object, thread, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.threads.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(object, thread, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.threads.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(object, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.with_raw_response.delete(
                "",
            )
