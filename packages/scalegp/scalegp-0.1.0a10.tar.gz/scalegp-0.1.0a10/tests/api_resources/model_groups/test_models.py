# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import ModelInstanceResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestModels:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        model = client.model_groups.models.create(
            "string",
            model_group_id="string",
        )
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.model_groups.models.with_raw_response.create(
            "string",
            model_group_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.model_groups.models.with_streaming_response.create(
            "string",
            model_group_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(ModelInstanceResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_group_id` but received ''"):
            client.model_groups.models.with_raw_response.create(
                "string",
                model_group_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            client.model_groups.models.with_raw_response.create(
                "",
                model_group_id="string",
            )


class TestAsyncModels:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        model = await async_client.model_groups.models.create(
            "string",
            model_group_id="string",
        )
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.model_groups.models.with_raw_response.create(
            "string",
            model_group_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.model_groups.models.with_streaming_response.create(
            "string",
            model_group_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(ModelInstanceResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_group_id` but received ''"):
            await async_client.model_groups.models.with_raw_response.create(
                "string",
                model_group_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            await async_client.model_groups.models.with_raw_response.create(
                "",
                model_group_id="string",
            )
