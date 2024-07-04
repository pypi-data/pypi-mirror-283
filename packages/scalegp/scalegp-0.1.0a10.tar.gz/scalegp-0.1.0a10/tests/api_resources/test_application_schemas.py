# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import ApplicationSchemaListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplicationSchemas:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        application_schema = client.application_schemas.list(
            version="V0",
        )
        assert_matches_type(ApplicationSchemaListResponse, application_schema, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.application_schemas.with_raw_response.list(
            version="V0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_schema = response.parse()
        assert_matches_type(ApplicationSchemaListResponse, application_schema, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.application_schemas.with_streaming_response.list(
            version="V0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_schema = response.parse()
            assert_matches_type(ApplicationSchemaListResponse, application_schema, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncApplicationSchemas:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        application_schema = await async_client.application_schemas.list(
            version="V0",
        )
        assert_matches_type(ApplicationSchemaListResponse, application_schema, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.application_schemas.with_raw_response.list(
            version="V0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_schema = await response.parse()
        assert_matches_type(ApplicationSchemaListResponse, application_schema, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.application_schemas.with_streaming_response.list(
            version="V0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_schema = await response.parse()
            assert_matches_type(ApplicationSchemaListResponse, application_schema, path=["response"])

        assert cast(Any, response.is_closed) is True
