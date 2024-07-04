# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.applications import ApplicationInteractionEntry

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInteractions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        interaction = client.applications.interactions.list(
            "string",
        )
        assert_matches_type(ApplicationInteractionEntry, interaction, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        interaction = client.applications.interactions.list(
            "string",
            from_ts=1,
            limit=1,
            page=1,
            search_text="string",
            to_ts=1,
            variants=["string", "string", "string"],
        )
        assert_matches_type(ApplicationInteractionEntry, interaction, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.applications.interactions.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        interaction = response.parse()
        assert_matches_type(ApplicationInteractionEntry, interaction, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.applications.interactions.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            interaction = response.parse()
            assert_matches_type(ApplicationInteractionEntry, interaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            client.applications.interactions.with_raw_response.list(
                "",
            )


class TestAsyncInteractions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        interaction = await async_client.applications.interactions.list(
            "string",
        )
        assert_matches_type(ApplicationInteractionEntry, interaction, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        interaction = await async_client.applications.interactions.list(
            "string",
            from_ts=1,
            limit=1,
            page=1,
            search_text="string",
            to_ts=1,
            variants=["string", "string", "string"],
        )
        assert_matches_type(ApplicationInteractionEntry, interaction, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.applications.interactions.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        interaction = await response.parse()
        assert_matches_type(ApplicationInteractionEntry, interaction, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.applications.interactions.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            interaction = await response.parse()
            assert_matches_type(ApplicationInteractionEntry, interaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            await async_client.applications.interactions.with_raw_response.list(
                "",
            )
