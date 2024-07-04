# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.shared import DeleteResponse, TestCaseVersionResponse
from scalegp.types.evaluation_datasets.test_cases import HistoryListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestHistory:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        history = client.evaluation_datasets.test_cases.history.retrieve(
            "string",
            evaluation_dataset_id="string",
            test_case_id="string",
        )
        assert_matches_type(TestCaseVersionResponse, history, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
            "string",
            evaluation_dataset_id="string",
            test_case_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        history = response.parse()
        assert_matches_type(TestCaseVersionResponse, history, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.evaluation_datasets.test_cases.history.with_streaming_response.retrieve(
            "string",
            evaluation_dataset_id="string",
            test_case_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            history = response.parse()
            assert_matches_type(TestCaseVersionResponse, history, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
                "string",
                evaluation_dataset_id="",
                test_case_id="string",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
                "string",
                evaluation_dataset_id="string",
                test_case_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `num` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
                "",
                evaluation_dataset_id="string",
                test_case_id="string",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        history = client.evaluation_datasets.test_cases.history.list(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(HistoryListResponse, history, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        history = client.evaluation_datasets.test_cases.history.list(
            "string",
            evaluation_dataset_id="string",
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(HistoryListResponse, history, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.evaluation_datasets.test_cases.history.with_raw_response.list(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        history = response.parse()
        assert_matches_type(HistoryListResponse, history, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.evaluation_datasets.test_cases.history.with_streaming_response.list(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            history = response.parse()
            assert_matches_type(HistoryListResponse, history, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.list(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `num` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.list(
                "",
                evaluation_dataset_id="string",
            )

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        history = client.evaluation_datasets.test_cases.history.delete(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(DeleteResponse, history, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.evaluation_datasets.test_cases.history.with_raw_response.delete(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        history = response.parse()
        assert_matches_type(DeleteResponse, history, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.evaluation_datasets.test_cases.history.with_streaming_response.delete(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            history = response.parse()
            assert_matches_type(DeleteResponse, history, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.delete(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.delete(
                "",
                evaluation_dataset_id="string",
            )


class TestAsyncHistory:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        history = await async_client.evaluation_datasets.test_cases.history.retrieve(
            "string",
            evaluation_dataset_id="string",
            test_case_id="string",
        )
        assert_matches_type(TestCaseVersionResponse, history, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
            "string",
            evaluation_dataset_id="string",
            test_case_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        history = await response.parse()
        assert_matches_type(TestCaseVersionResponse, history, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.test_cases.history.with_streaming_response.retrieve(
            "string",
            evaluation_dataset_id="string",
            test_case_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            history = await response.parse()
            assert_matches_type(TestCaseVersionResponse, history, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
                "string",
                evaluation_dataset_id="",
                test_case_id="string",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
                "string",
                evaluation_dataset_id="string",
                test_case_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `num` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
                "",
                evaluation_dataset_id="string",
                test_case_id="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        history = await async_client.evaluation_datasets.test_cases.history.list(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(HistoryListResponse, history, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        history = await async_client.evaluation_datasets.test_cases.history.list(
            "string",
            evaluation_dataset_id="string",
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(HistoryListResponse, history, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.test_cases.history.with_raw_response.list(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        history = await response.parse()
        assert_matches_type(HistoryListResponse, history, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.test_cases.history.with_streaming_response.list(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            history = await response.parse()
            assert_matches_type(HistoryListResponse, history, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.list(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `num` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.list(
                "",
                evaluation_dataset_id="string",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        history = await async_client.evaluation_datasets.test_cases.history.delete(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(DeleteResponse, history, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.test_cases.history.with_raw_response.delete(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        history = await response.parse()
        assert_matches_type(DeleteResponse, history, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.test_cases.history.with_streaming_response.delete(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            history = await response.parse()
            assert_matches_type(DeleteResponse, history, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.delete(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.delete(
                "",
                evaluation_dataset_id="string",
            )
