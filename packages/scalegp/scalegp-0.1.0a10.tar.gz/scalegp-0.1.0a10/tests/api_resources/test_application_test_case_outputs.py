# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import (
    ApplicationTestCaseOutput,
    ApplicationTestCaseOutputListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplicationTestCaseOutputs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        application_test_case_output = client.application_test_case_outputs.retrieve(
            "string",
        )
        assert_matches_type(ApplicationTestCaseOutput, application_test_case_output, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGP) -> None:
        application_test_case_output = client.application_test_case_outputs.retrieve(
            "string",
            view=["MetricScores", "TestCaseVersion", "Trace"],
        )
        assert_matches_type(ApplicationTestCaseOutput, application_test_case_output, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.application_test_case_outputs.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_test_case_output = response.parse()
        assert_matches_type(ApplicationTestCaseOutput, application_test_case_output, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.application_test_case_outputs.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_test_case_output = response.parse()
            assert_matches_type(ApplicationTestCaseOutput, application_test_case_output, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_test_case_output_id` but received ''"
        ):
            client.application_test_case_outputs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        application_test_case_output = client.application_test_case_outputs.list()
        assert_matches_type(ApplicationTestCaseOutputListResponse, application_test_case_output, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        application_test_case_output = client.application_test_case_outputs.list(
            account_id="string",
            application_variant_report_id="string",
            limit=1,
            page=1,
            view=["MetricScores", "TestCaseVersion", "Trace"],
            x_selected_account_id="string",
        )
        assert_matches_type(ApplicationTestCaseOutputListResponse, application_test_case_output, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.application_test_case_outputs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_test_case_output = response.parse()
        assert_matches_type(ApplicationTestCaseOutputListResponse, application_test_case_output, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.application_test_case_outputs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_test_case_output = response.parse()
            assert_matches_type(ApplicationTestCaseOutputListResponse, application_test_case_output, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncApplicationTestCaseOutputs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        application_test_case_output = await async_client.application_test_case_outputs.retrieve(
            "string",
        )
        assert_matches_type(ApplicationTestCaseOutput, application_test_case_output, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGP) -> None:
        application_test_case_output = await async_client.application_test_case_outputs.retrieve(
            "string",
            view=["MetricScores", "TestCaseVersion", "Trace"],
        )
        assert_matches_type(ApplicationTestCaseOutput, application_test_case_output, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.application_test_case_outputs.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_test_case_output = await response.parse()
        assert_matches_type(ApplicationTestCaseOutput, application_test_case_output, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.application_test_case_outputs.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_test_case_output = await response.parse()
            assert_matches_type(ApplicationTestCaseOutput, application_test_case_output, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_test_case_output_id` but received ''"
        ):
            await async_client.application_test_case_outputs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        application_test_case_output = await async_client.application_test_case_outputs.list()
        assert_matches_type(ApplicationTestCaseOutputListResponse, application_test_case_output, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        application_test_case_output = await async_client.application_test_case_outputs.list(
            account_id="string",
            application_variant_report_id="string",
            limit=1,
            page=1,
            view=["MetricScores", "TestCaseVersion", "Trace"],
            x_selected_account_id="string",
        )
        assert_matches_type(ApplicationTestCaseOutputListResponse, application_test_case_output, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.application_test_case_outputs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_test_case_output = await response.parse()
        assert_matches_type(ApplicationTestCaseOutputListResponse, application_test_case_output, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.application_test_case_outputs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_test_case_output = await response.parse()
            assert_matches_type(ApplicationTestCaseOutputListResponse, application_test_case_output, path=["response"])

        assert cast(Any, response.is_closed) is True
