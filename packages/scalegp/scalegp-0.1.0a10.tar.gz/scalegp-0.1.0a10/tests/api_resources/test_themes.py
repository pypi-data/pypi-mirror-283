# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import ThemeResponse, ThemeListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestThemes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        theme = client.themes.create(
            account_id="string",
            logo_blob="string",
            theme_vars={},
            title="string",
        )
        assert_matches_type(ThemeResponse, theme, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        theme = client.themes.create(
            account_id="string",
            logo_blob="string",
            theme_vars={
                "accent_primary": "string",
                "accent_secondary": "string",
                "background": "string",
                "foreground": "string",
            },
            title="string",
            x_selected_account_id="string",
        )
        assert_matches_type(ThemeResponse, theme, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.themes.with_raw_response.create(
            account_id="string",
            logo_blob="string",
            theme_vars={},
            title="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        theme = response.parse()
        assert_matches_type(ThemeResponse, theme, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.themes.with_streaming_response.create(
            account_id="string",
            logo_blob="string",
            theme_vars={},
            title="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            theme = response.parse()
            assert_matches_type(ThemeResponse, theme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        theme = client.themes.retrieve(
            "string",
        )
        assert_matches_type(ThemeResponse, theme, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.themes.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        theme = response.parse()
        assert_matches_type(ThemeResponse, theme, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.themes.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            theme = response.parse()
            assert_matches_type(ThemeResponse, theme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `theme_id` but received ''"):
            client.themes.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        theme = client.themes.list()
        assert_matches_type(ThemeListResponse, theme, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        theme = client.themes.list(
            account_id="string",
            include_archived=True,
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(ThemeListResponse, theme, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.themes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        theme = response.parse()
        assert_matches_type(ThemeListResponse, theme, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.themes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            theme = response.parse()
            assert_matches_type(ThemeListResponse, theme, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncThemes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        theme = await async_client.themes.create(
            account_id="string",
            logo_blob="string",
            theme_vars={},
            title="string",
        )
        assert_matches_type(ThemeResponse, theme, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        theme = await async_client.themes.create(
            account_id="string",
            logo_blob="string",
            theme_vars={
                "accent_primary": "string",
                "accent_secondary": "string",
                "background": "string",
                "foreground": "string",
            },
            title="string",
            x_selected_account_id="string",
        )
        assert_matches_type(ThemeResponse, theme, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.themes.with_raw_response.create(
            account_id="string",
            logo_blob="string",
            theme_vars={},
            title="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        theme = await response.parse()
        assert_matches_type(ThemeResponse, theme, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.themes.with_streaming_response.create(
            account_id="string",
            logo_blob="string",
            theme_vars={},
            title="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            theme = await response.parse()
            assert_matches_type(ThemeResponse, theme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        theme = await async_client.themes.retrieve(
            "string",
        )
        assert_matches_type(ThemeResponse, theme, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.themes.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        theme = await response.parse()
        assert_matches_type(ThemeResponse, theme, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.themes.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            theme = await response.parse()
            assert_matches_type(ThemeResponse, theme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `theme_id` but received ''"):
            await async_client.themes.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        theme = await async_client.themes.list()
        assert_matches_type(ThemeListResponse, theme, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        theme = await async_client.themes.list(
            account_id="string",
            include_archived=True,
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(ThemeListResponse, theme, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.themes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        theme = await response.parse()
        assert_matches_type(ThemeListResponse, theme, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.themes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            theme = await response.parse()
            assert_matches_type(ThemeListResponse, theme, path=["response"])

        assert cast(Any, response.is_closed) is True
