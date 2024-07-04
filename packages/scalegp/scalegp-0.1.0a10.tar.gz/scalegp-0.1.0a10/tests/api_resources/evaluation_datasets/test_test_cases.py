# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.shared import DeleteResponse, TestCaseVersionResponse
from scalegp.types.evaluation_datasets import (
    TestCaseListResponse,
    TestCaseBatchResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTestCases:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        test_case = client.evaluation_datasets.test_cases.create(
            "string",
            schema_type="GENERATION",
            test_case_data={},
        )
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        test_case = client.evaluation_datasets.test_cases.create(
            "string",
            schema_type="GENERATION",
            test_case_data={},
            account_id="string",
            chat_history={},
            test_case_metadata={},
            x_selected_account_id="string",
        )
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.evaluation_datasets.test_cases.with_raw_response.create(
            "string",
            schema_type="GENERATION",
            test_case_data={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.evaluation_datasets.test_cases.with_streaming_response.create(
            "string",
            schema_type="GENERATION",
            test_case_data={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.test_cases.with_raw_response.create(
                "",
                schema_type="GENERATION",
                test_case_data={},
            )

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        test_case = client.evaluation_datasets.test_cases.retrieve(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.evaluation_datasets.test_cases.with_raw_response.retrieve(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.evaluation_datasets.test_cases.with_streaming_response.retrieve(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.test_cases.with_raw_response.retrieve(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            client.evaluation_datasets.test_cases.with_raw_response.retrieve(
                "",
                evaluation_dataset_id="string",
            )

    @parametrize
    def test_method_update_overload_1(self, client: SGP) -> None:
        test_case = client.evaluation_datasets.test_cases.update(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    def test_method_update_with_all_params_overload_1(self, client: SGP) -> None:
        test_case = client.evaluation_datasets.test_cases.update(
            "string",
            evaluation_dataset_id="string",
            chat_history={},
            restore=True,
            schema_type="GENERATION",
            test_case_data={},
            test_case_metadata={},
        )
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    def test_raw_response_update_overload_1(self, client: SGP) -> None:
        response = client.evaluation_datasets.test_cases.with_raw_response.update(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    def test_streaming_response_update_overload_1(self, client: SGP) -> None:
        with client.evaluation_datasets.test_cases.with_streaming_response.update(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_overload_1(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.test_cases.with_raw_response.update(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            client.evaluation_datasets.test_cases.with_raw_response.update(
                "",
                evaluation_dataset_id="string",
            )

    @parametrize
    def test_method_update_overload_2(self, client: SGP) -> None:
        test_case = client.evaluation_datasets.test_cases.update(
            "string",
            evaluation_dataset_id="string",
            restore=True,
        )
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    def test_raw_response_update_overload_2(self, client: SGP) -> None:
        response = client.evaluation_datasets.test_cases.with_raw_response.update(
            "string",
            evaluation_dataset_id="string",
            restore=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    def test_streaming_response_update_overload_2(self, client: SGP) -> None:
        with client.evaluation_datasets.test_cases.with_streaming_response.update(
            "string",
            evaluation_dataset_id="string",
            restore=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_overload_2(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.test_cases.with_raw_response.update(
                "string",
                evaluation_dataset_id="",
                restore=True,
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            client.evaluation_datasets.test_cases.with_raw_response.update(
                "",
                evaluation_dataset_id="string",
                restore=True,
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        test_case = client.evaluation_datasets.test_cases.list(
            "string",
        )
        assert_matches_type(TestCaseListResponse, test_case, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        test_case = client.evaluation_datasets.test_cases.list(
            "string",
            account_id="string",
            include_archived=True,
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(TestCaseListResponse, test_case, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.evaluation_datasets.test_cases.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(TestCaseListResponse, test_case, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.evaluation_datasets.test_cases.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(TestCaseListResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.test_cases.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        test_case = client.evaluation_datasets.test_cases.delete(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(DeleteResponse, test_case, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.evaluation_datasets.test_cases.with_raw_response.delete(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(DeleteResponse, test_case, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.evaluation_datasets.test_cases.with_streaming_response.delete(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(DeleteResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.test_cases.with_raw_response.delete(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            client.evaluation_datasets.test_cases.with_raw_response.delete(
                "",
                evaluation_dataset_id="string",
            )

    @parametrize
    def test_method_batch(self, client: SGP) -> None:
        test_case = client.evaluation_datasets.test_cases.batch(
            "string",
            body=[
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
            ],
        )
        assert_matches_type(TestCaseBatchResponse, test_case, path=["response"])

    @parametrize
    def test_method_batch_with_all_params(self, client: SGP) -> None:
        test_case = client.evaluation_datasets.test_cases.batch(
            "string",
            body=[
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                    "chat_history": {},
                    "test_case_metadata": {},
                    "account_id": "string",
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                    "chat_history": {},
                    "test_case_metadata": {},
                    "account_id": "string",
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                    "chat_history": {},
                    "test_case_metadata": {},
                    "account_id": "string",
                },
            ],
            x_selected_account_id="string",
        )
        assert_matches_type(TestCaseBatchResponse, test_case, path=["response"])

    @parametrize
    def test_raw_response_batch(self, client: SGP) -> None:
        response = client.evaluation_datasets.test_cases.with_raw_response.batch(
            "string",
            body=[
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(TestCaseBatchResponse, test_case, path=["response"])

    @parametrize
    def test_streaming_response_batch(self, client: SGP) -> None:
        with client.evaluation_datasets.test_cases.with_streaming_response.batch(
            "string",
            body=[
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(TestCaseBatchResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_batch(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.test_cases.with_raw_response.batch(
                "",
                body=[
                    {
                        "schema_type": "GENERATION",
                        "test_case_data": {},
                    },
                    {
                        "schema_type": "GENERATION",
                        "test_case_data": {},
                    },
                    {
                        "schema_type": "GENERATION",
                        "test_case_data": {},
                    },
                ],
            )


class TestAsyncTestCases:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        test_case = await async_client.evaluation_datasets.test_cases.create(
            "string",
            schema_type="GENERATION",
            test_case_data={},
        )
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        test_case = await async_client.evaluation_datasets.test_cases.create(
            "string",
            schema_type="GENERATION",
            test_case_data={},
            account_id="string",
            chat_history={},
            test_case_metadata={},
            x_selected_account_id="string",
        )
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.test_cases.with_raw_response.create(
            "string",
            schema_type="GENERATION",
            test_case_data={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.test_cases.with_streaming_response.create(
            "string",
            schema_type="GENERATION",
            test_case_data={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.with_raw_response.create(
                "",
                schema_type="GENERATION",
                test_case_data={},
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        test_case = await async_client.evaluation_datasets.test_cases.retrieve(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.test_cases.with_raw_response.retrieve(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.test_cases.with_streaming_response.retrieve(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.with_raw_response.retrieve(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.with_raw_response.retrieve(
                "",
                evaluation_dataset_id="string",
            )

    @parametrize
    async def test_method_update_overload_1(self, async_client: AsyncSGP) -> None:
        test_case = await async_client.evaluation_datasets.test_cases.update(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    async def test_method_update_with_all_params_overload_1(self, async_client: AsyncSGP) -> None:
        test_case = await async_client.evaluation_datasets.test_cases.update(
            "string",
            evaluation_dataset_id="string",
            chat_history={},
            restore=True,
            schema_type="GENERATION",
            test_case_data={},
            test_case_metadata={},
        )
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    async def test_raw_response_update_overload_1(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.test_cases.with_raw_response.update(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    async def test_streaming_response_update_overload_1(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.test_cases.with_streaming_response.update(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_overload_1(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.with_raw_response.update(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.with_raw_response.update(
                "",
                evaluation_dataset_id="string",
            )

    @parametrize
    async def test_method_update_overload_2(self, async_client: AsyncSGP) -> None:
        test_case = await async_client.evaluation_datasets.test_cases.update(
            "string",
            evaluation_dataset_id="string",
            restore=True,
        )
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    async def test_raw_response_update_overload_2(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.test_cases.with_raw_response.update(
            "string",
            evaluation_dataset_id="string",
            restore=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

    @parametrize
    async def test_streaming_response_update_overload_2(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.test_cases.with_streaming_response.update(
            "string",
            evaluation_dataset_id="string",
            restore=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(TestCaseVersionResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_overload_2(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.with_raw_response.update(
                "string",
                evaluation_dataset_id="",
                restore=True,
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.with_raw_response.update(
                "",
                evaluation_dataset_id="string",
                restore=True,
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        test_case = await async_client.evaluation_datasets.test_cases.list(
            "string",
        )
        assert_matches_type(TestCaseListResponse, test_case, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        test_case = await async_client.evaluation_datasets.test_cases.list(
            "string",
            account_id="string",
            include_archived=True,
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(TestCaseListResponse, test_case, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.test_cases.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(TestCaseListResponse, test_case, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.test_cases.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(TestCaseListResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        test_case = await async_client.evaluation_datasets.test_cases.delete(
            "string",
            evaluation_dataset_id="string",
        )
        assert_matches_type(DeleteResponse, test_case, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.test_cases.with_raw_response.delete(
            "string",
            evaluation_dataset_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(DeleteResponse, test_case, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.test_cases.with_streaming_response.delete(
            "string",
            evaluation_dataset_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(DeleteResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.with_raw_response.delete(
                "string",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.with_raw_response.delete(
                "",
                evaluation_dataset_id="string",
            )

    @parametrize
    async def test_method_batch(self, async_client: AsyncSGP) -> None:
        test_case = await async_client.evaluation_datasets.test_cases.batch(
            "string",
            body=[
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
            ],
        )
        assert_matches_type(TestCaseBatchResponse, test_case, path=["response"])

    @parametrize
    async def test_method_batch_with_all_params(self, async_client: AsyncSGP) -> None:
        test_case = await async_client.evaluation_datasets.test_cases.batch(
            "string",
            body=[
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                    "chat_history": {},
                    "test_case_metadata": {},
                    "account_id": "string",
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                    "chat_history": {},
                    "test_case_metadata": {},
                    "account_id": "string",
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                    "chat_history": {},
                    "test_case_metadata": {},
                    "account_id": "string",
                },
            ],
            x_selected_account_id="string",
        )
        assert_matches_type(TestCaseBatchResponse, test_case, path=["response"])

    @parametrize
    async def test_raw_response_batch(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluation_datasets.test_cases.with_raw_response.batch(
            "string",
            body=[
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(TestCaseBatchResponse, test_case, path=["response"])

    @parametrize
    async def test_streaming_response_batch(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluation_datasets.test_cases.with_streaming_response.batch(
            "string",
            body=[
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
                {
                    "schema_type": "GENERATION",
                    "test_case_data": {},
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(TestCaseBatchResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_batch(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.with_raw_response.batch(
                "",
                body=[
                    {
                        "schema_type": "GENERATION",
                        "test_case_data": {},
                    },
                    {
                        "schema_type": "GENERATION",
                        "test_case_data": {},
                    },
                    {
                        "schema_type": "GENERATION",
                        "test_case_data": {},
                    },
                ],
            )
