# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp._utils import parse_datetime
from scalegp.types.shared import ModelUsageResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUsageStatistics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        usage_statistic = client.model_deployments.usage_statistics.retrieve(
            "string",
            chunks=0,
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(ModelUsageResponse, usage_statistic, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.model_deployments.usage_statistics.with_raw_response.retrieve(
            "string",
            chunks=0,
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        usage_statistic = response.parse()
        assert_matches_type(ModelUsageResponse, usage_statistic, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.model_deployments.usage_statistics.with_streaming_response.retrieve(
            "string",
            chunks=0,
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            usage_statistic = response.parse()
            assert_matches_type(ModelUsageResponse, usage_statistic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            client.model_deployments.usage_statistics.with_raw_response.retrieve(
                "",
                chunks=0,
                end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
                start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            )


class TestAsyncUsageStatistics:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        usage_statistic = await async_client.model_deployments.usage_statistics.retrieve(
            "string",
            chunks=0,
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(ModelUsageResponse, usage_statistic, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.model_deployments.usage_statistics.with_raw_response.retrieve(
            "string",
            chunks=0,
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        usage_statistic = await response.parse()
        assert_matches_type(ModelUsageResponse, usage_statistic, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.model_deployments.usage_statistics.with_streaming_response.retrieve(
            "string",
            chunks=0,
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            usage_statistic = await response.parse()
            assert_matches_type(ModelUsageResponse, usage_statistic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            await async_client.model_deployments.usage_statistics.with_raw_response.retrieve(
                "",
                chunks=0,
                end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
                start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            )
