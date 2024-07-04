# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVariant:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_process(self, client: SGP) -> None:
        variant = client.applications.variant.process(
            "string",
            inputs={"foo": {}},
        )
        assert_matches_type(object, variant, path=["response"])

    @parametrize
    def test_method_process_with_all_params(self, client: SGP) -> None:
        variant = client.applications.variant.process(
            "string",
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
        )
        assert_matches_type(object, variant, path=["response"])

    @parametrize
    def test_raw_response_process(self, client: SGP) -> None:
        response = client.applications.variant.with_raw_response.process(
            "string",
            inputs={"foo": {}},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        variant = response.parse()
        assert_matches_type(object, variant, path=["response"])

    @parametrize
    def test_streaming_response_process(self, client: SGP) -> None:
        with client.applications.variant.with_streaming_response.process(
            "string",
            inputs={"foo": {}},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            variant = response.parse()
            assert_matches_type(object, variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_process(self, client: SGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            client.applications.variant.with_raw_response.process(
                "",
                inputs={"foo": {}},
            )


class TestAsyncVariant:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_process(self, async_client: AsyncSGP) -> None:
        variant = await async_client.applications.variant.process(
            "string",
            inputs={"foo": {}},
        )
        assert_matches_type(object, variant, path=["response"])

    @parametrize
    async def test_method_process_with_all_params(self, async_client: AsyncSGP) -> None:
        variant = await async_client.applications.variant.process(
            "string",
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
        )
        assert_matches_type(object, variant, path=["response"])

    @parametrize
    async def test_raw_response_process(self, async_client: AsyncSGP) -> None:
        response = await async_client.applications.variant.with_raw_response.process(
            "string",
            inputs={"foo": {}},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        variant = await response.parse()
        assert_matches_type(object, variant, path=["response"])

    @parametrize
    async def test_streaming_response_process(self, async_client: AsyncSGP) -> None:
        async with async_client.applications.variant.with_streaming_response.process(
            "string",
            inputs={"foo": {}},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            variant = await response.parse()
            assert_matches_type(object, variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_process(self, async_client: AsyncSGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            await async_client.applications.variant.with_raw_response.process(
                "",
                inputs={"foo": {}},
            )
