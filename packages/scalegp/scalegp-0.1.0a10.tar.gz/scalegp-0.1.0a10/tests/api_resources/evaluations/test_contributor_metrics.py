# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.evaluations import (
    ContributorMetricsResponse,
    PaginationResponseContributorMetrics,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestContributorMetrics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        contributor_metric = client.evaluations.contributor_metrics.retrieve(
            "string",
            evaluation_id="string",
        )
        assert_matches_type(ContributorMetricsResponse, contributor_metric, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGP) -> None:
        contributor_metric = client.evaluations.contributor_metrics.retrieve(
            "string",
            evaluation_id="string",
            x_selected_account_id="string",
        )
        assert_matches_type(ContributorMetricsResponse, contributor_metric, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.evaluations.contributor_metrics.with_raw_response.retrieve(
            "string",
            evaluation_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        contributor_metric = response.parse()
        assert_matches_type(ContributorMetricsResponse, contributor_metric, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.evaluations.contributor_metrics.with_streaming_response.retrieve(
            "string",
            evaluation_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            contributor_metric = response.parse()
            assert_matches_type(ContributorMetricsResponse, contributor_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.contributor_metrics.with_raw_response.retrieve(
                "string",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `contributor_id` but received ''"):
            client.evaluations.contributor_metrics.with_raw_response.retrieve(
                "",
                evaluation_id="string",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        contributor_metric = client.evaluations.contributor_metrics.list(
            "string",
        )
        assert_matches_type(PaginationResponseContributorMetrics, contributor_metric, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        contributor_metric = client.evaluations.contributor_metrics.list(
            "string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(PaginationResponseContributorMetrics, contributor_metric, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.evaluations.contributor_metrics.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        contributor_metric = response.parse()
        assert_matches_type(PaginationResponseContributorMetrics, contributor_metric, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.evaluations.contributor_metrics.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            contributor_metric = response.parse()
            assert_matches_type(PaginationResponseContributorMetrics, contributor_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.contributor_metrics.with_raw_response.list(
                "",
            )


class TestAsyncContributorMetrics:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        contributor_metric = await async_client.evaluations.contributor_metrics.retrieve(
            "string",
            evaluation_id="string",
        )
        assert_matches_type(ContributorMetricsResponse, contributor_metric, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGP) -> None:
        contributor_metric = await async_client.evaluations.contributor_metrics.retrieve(
            "string",
            evaluation_id="string",
            x_selected_account_id="string",
        )
        assert_matches_type(ContributorMetricsResponse, contributor_metric, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.contributor_metrics.with_raw_response.retrieve(
            "string",
            evaluation_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        contributor_metric = await response.parse()
        assert_matches_type(ContributorMetricsResponse, contributor_metric, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.contributor_metrics.with_streaming_response.retrieve(
            "string",
            evaluation_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            contributor_metric = await response.parse()
            assert_matches_type(ContributorMetricsResponse, contributor_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.contributor_metrics.with_raw_response.retrieve(
                "string",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `contributor_id` but received ''"):
            await async_client.evaluations.contributor_metrics.with_raw_response.retrieve(
                "",
                evaluation_id="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        contributor_metric = await async_client.evaluations.contributor_metrics.list(
            "string",
        )
        assert_matches_type(PaginationResponseContributorMetrics, contributor_metric, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        contributor_metric = await async_client.evaluations.contributor_metrics.list(
            "string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(PaginationResponseContributorMetrics, contributor_metric, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.contributor_metrics.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        contributor_metric = await response.parse()
        assert_matches_type(PaginationResponseContributorMetrics, contributor_metric, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.contributor_metrics.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            contributor_metric = await response.parse()
            assert_matches_type(PaginationResponseContributorMetrics, contributor_metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.contributor_metrics.with_raw_response.list(
                "",
            )
