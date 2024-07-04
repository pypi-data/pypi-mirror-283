# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.applications.variant import (
    ChatThread,
    ThreadListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestThreads:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        thread = client.applications.variant.threads.create(
            path_application_variant_id="string",
            account_id="string",
            body_application_variant_id="string",
            title="string",
        )
        assert_matches_type(ChatThread, thread, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.applications.variant.threads.with_raw_response.create(
            path_application_variant_id="string",
            account_id="string",
            body_application_variant_id="string",
            title="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(ChatThread, thread, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.applications.variant.threads.with_streaming_response.create(
            path_application_variant_id="string",
            account_id="string",
            body_application_variant_id="string",
            title="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(ChatThread, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_application_variant_id` but received ''"
        ):
            client.applications.variant.threads.with_raw_response.create(
                path_application_variant_id="",
                account_id="string",
                body_application_variant_id="",
                title="string",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        thread = client.applications.variant.threads.list(
            "string",
        )
        assert_matches_type(ThreadListResponse, thread, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.applications.variant.threads.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(ThreadListResponse, thread, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.applications.variant.threads.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(ThreadListResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            client.applications.variant.threads.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_process(self, client: SGP) -> None:
        thread = client.applications.variant.threads.process(
            "string",
            application_variant_id="string",
            inputs={"foo": {}},
        )
        assert_matches_type(object, thread, path=["response"])

    @parametrize
    def test_method_process_with_all_params(self, client: SGP) -> None:
        thread = client.applications.variant.threads.process(
            "string",
            application_variant_id="string",
            inputs={"foo": {}},
            history=[
                {
                    "request": "string",
                    "response": "string",
                },
                {
                    "request": "string",
                    "response": "string",
                },
                {
                    "request": "string",
                    "response": "string",
                },
            ],
            x_selected_account_id="string",
        )
        assert_matches_type(object, thread, path=["response"])

    @parametrize
    def test_raw_response_process(self, client: SGP) -> None:
        response = client.applications.variant.threads.with_raw_response.process(
            "string",
            application_variant_id="string",
            inputs={"foo": {}},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(object, thread, path=["response"])

    @parametrize
    def test_streaming_response_process(self, client: SGP) -> None:
        with client.applications.variant.threads.with_streaming_response.process(
            "string",
            application_variant_id="string",
            inputs={"foo": {}},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(object, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_process(self, client: SGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            client.applications.variant.threads.with_raw_response.process(
                "string",
                application_variant_id="",
                inputs={"foo": {}},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.applications.variant.threads.with_raw_response.process(
                "",
                application_variant_id="string",
                inputs={"foo": {}},
            )


class TestAsyncThreads:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        thread = await async_client.applications.variant.threads.create(
            path_application_variant_id="string",
            account_id="string",
            body_application_variant_id="string",
            title="string",
        )
        assert_matches_type(ChatThread, thread, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.applications.variant.threads.with_raw_response.create(
            path_application_variant_id="string",
            account_id="string",
            body_application_variant_id="string",
            title="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(ChatThread, thread, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.applications.variant.threads.with_streaming_response.create(
            path_application_variant_id="string",
            account_id="string",
            body_application_variant_id="string",
            title="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(ChatThread, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_application_variant_id` but received ''"
        ):
            await async_client.applications.variant.threads.with_raw_response.create(
                path_application_variant_id="",
                account_id="string",
                body_application_variant_id="",
                title="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        thread = await async_client.applications.variant.threads.list(
            "string",
        )
        assert_matches_type(ThreadListResponse, thread, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.applications.variant.threads.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(ThreadListResponse, thread, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.applications.variant.threads.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(ThreadListResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            await async_client.applications.variant.threads.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_process(self, async_client: AsyncSGP) -> None:
        thread = await async_client.applications.variant.threads.process(
            "string",
            application_variant_id="string",
            inputs={"foo": {}},
        )
        assert_matches_type(object, thread, path=["response"])

    @parametrize
    async def test_method_process_with_all_params(self, async_client: AsyncSGP) -> None:
        thread = await async_client.applications.variant.threads.process(
            "string",
            application_variant_id="string",
            inputs={"foo": {}},
            history=[
                {
                    "request": "string",
                    "response": "string",
                },
                {
                    "request": "string",
                    "response": "string",
                },
                {
                    "request": "string",
                    "response": "string",
                },
            ],
            x_selected_account_id="string",
        )
        assert_matches_type(object, thread, path=["response"])

    @parametrize
    async def test_raw_response_process(self, async_client: AsyncSGP) -> None:
        response = await async_client.applications.variant.threads.with_raw_response.process(
            "string",
            application_variant_id="string",
            inputs={"foo": {}},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(object, thread, path=["response"])

    @parametrize
    async def test_streaming_response_process(self, async_client: AsyncSGP) -> None:
        async with async_client.applications.variant.threads.with_streaming_response.process(
            "string",
            application_variant_id="string",
            inputs={"foo": {}},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(object, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_process(self, async_client: AsyncSGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            await async_client.applications.variant.threads.with_raw_response.process(
                "string",
                application_variant_id="",
                inputs={"foo": {}},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.applications.variant.threads.with_raw_response.process(
                "",
                application_variant_id="string",
                inputs={"foo": {}},
            )
