# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.shared import TestCaseResultResponse, TestCaseResultResponseWithViews
from scalegp.types.evaluations import (
    TestCaseResultListResponse,
    TestCaseResultBatchResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTestCaseResults:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        test_case_result = client.evaluations.test_case_results.create(
            "string",
            application_spec_id="string",
            evaluation_dataset_version_num="string",
            test_case_evaluation_data={},
            test_case_evaluation_data_schema="GENERATION",
            test_case_id="string",
        )
        assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        test_case_result = client.evaluations.test_case_results.create(
            "string",
            application_spec_id="string",
            evaluation_dataset_version_num="string",
            test_case_evaluation_data={},
            test_case_evaluation_data_schema="GENERATION",
            test_case_id="string",
            account_id="string",
            annotated_by_user_id="string",
            audit_comment="string",
            audit_required=True,
            audit_status="UNAUDITED",
            result={},
            time_spent_labeling_s=0,
            x_selected_account_id="string",
        )
        assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.evaluations.test_case_results.with_raw_response.create(
            "string",
            application_spec_id="string",
            evaluation_dataset_version_num="string",
            test_case_evaluation_data={},
            test_case_evaluation_data_schema="GENERATION",
            test_case_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = response.parse()
        assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.evaluations.test_case_results.with_streaming_response.create(
            "string",
            application_spec_id="string",
            evaluation_dataset_version_num="string",
            test_case_evaluation_data={},
            test_case_evaluation_data_schema="GENERATION",
            test_case_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = response.parse()
            assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.create(
                "",
                application_spec_id="string",
                evaluation_dataset_version_num="string",
                test_case_evaluation_data={},
                test_case_evaluation_data_schema="GENERATION",
                test_case_id="string",
            )

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        test_case_result = client.evaluations.test_case_results.retrieve(
            "string",
            evaluation_id="string",
        )
        assert_matches_type(TestCaseResultResponseWithViews, test_case_result, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGP) -> None:
        test_case_result = client.evaluations.test_case_results.retrieve(
            "string",
            evaluation_id="string",
            view=["AnnotationResults", "Task", "TestCaseVersion"],
        )
        assert_matches_type(TestCaseResultResponseWithViews, test_case_result, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.evaluations.test_case_results.with_raw_response.retrieve(
            "string",
            evaluation_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = response.parse()
        assert_matches_type(TestCaseResultResponseWithViews, test_case_result, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.evaluations.test_case_results.with_streaming_response.retrieve(
            "string",
            evaluation_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = response.parse()
            assert_matches_type(TestCaseResultResponseWithViews, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.retrieve(
                "string",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_result_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.retrieve(
                "",
                evaluation_id="string",
            )

    @parametrize
    def test_method_update(self, client: SGP) -> None:
        test_case_result = client.evaluations.test_case_results.update(
            "string",
            evaluation_id="string",
        )
        assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGP) -> None:
        test_case_result = client.evaluations.test_case_results.update(
            "string",
            evaluation_id="string",
            annotated_by_user_id="string",
            application_spec_id="string",
            audit_comment="string",
            audit_required=True,
            audit_status="UNAUDITED",
            evaluation_dataset_version_num="string",
            result={},
            test_case_evaluation_data={},
            test_case_evaluation_data_schema="GENERATION",
            test_case_id="string",
            time_spent_labeling_s=0,
        )
        assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGP) -> None:
        response = client.evaluations.test_case_results.with_raw_response.update(
            "string",
            evaluation_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = response.parse()
        assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGP) -> None:
        with client.evaluations.test_case_results.with_streaming_response.update(
            "string",
            evaluation_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = response.parse()
            assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.update(
                "string",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_result_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.update(
                "",
                evaluation_id="string",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        test_case_result = client.evaluations.test_case_results.list(
            "string",
        )
        assert_matches_type(TestCaseResultListResponse, test_case_result, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        test_case_result = client.evaluations.test_case_results.list(
            "string",
            account_id="string",
            include_archived=True,
            limit=1,
            page=1,
            view=["AnnotationResults", "Task", "TestCaseVersion"],
            x_selected_account_id="string",
        )
        assert_matches_type(TestCaseResultListResponse, test_case_result, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.evaluations.test_case_results.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = response.parse()
        assert_matches_type(TestCaseResultListResponse, test_case_result, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.evaluations.test_case_results.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = response.parse()
            assert_matches_type(TestCaseResultListResponse, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_batch(self, client: SGP) -> None:
        test_case_result = client.evaluations.test_case_results.batch(
            "string",
            body=[
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
            ],
        )
        assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

    @parametrize
    def test_method_batch_with_all_params(self, client: SGP) -> None:
        test_case_result = client.evaluations.test_case_results.batch(
            "string",
            body=[
                {
                    "audit_status": "UNAUDITED",
                    "audit_required": True,
                    "audit_comment": "string",
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                    "result": {},
                    "time_spent_labeling_s": 0,
                    "account_id": "string",
                    "annotated_by_user_id": "string",
                },
                {
                    "audit_status": "UNAUDITED",
                    "audit_required": True,
                    "audit_comment": "string",
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                    "result": {},
                    "time_spent_labeling_s": 0,
                    "account_id": "string",
                    "annotated_by_user_id": "string",
                },
                {
                    "audit_status": "UNAUDITED",
                    "audit_required": True,
                    "audit_comment": "string",
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                    "result": {},
                    "time_spent_labeling_s": 0,
                    "account_id": "string",
                    "annotated_by_user_id": "string",
                },
            ],
            x_selected_account_id="string",
        )
        assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

    @parametrize
    def test_raw_response_batch(self, client: SGP) -> None:
        response = client.evaluations.test_case_results.with_raw_response.batch(
            "string",
            body=[
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = response.parse()
        assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

    @parametrize
    def test_streaming_response_batch(self, client: SGP) -> None:
        with client.evaluations.test_case_results.with_streaming_response.batch(
            "string",
            body=[
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = response.parse()
            assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_batch(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.test_case_results.with_raw_response.batch(
                "",
                body=[
                    {
                        "application_spec_id": "string",
                        "evaluation_dataset_version_num": "string",
                        "test_case_id": "string",
                        "test_case_evaluation_data": {},
                        "test_case_evaluation_data_schema": "GENERATION",
                    },
                    {
                        "application_spec_id": "string",
                        "evaluation_dataset_version_num": "string",
                        "test_case_id": "string",
                        "test_case_evaluation_data": {},
                        "test_case_evaluation_data_schema": "GENERATION",
                    },
                    {
                        "application_spec_id": "string",
                        "evaluation_dataset_version_num": "string",
                        "test_case_id": "string",
                        "test_case_evaluation_data": {},
                        "test_case_evaluation_data_schema": "GENERATION",
                    },
                ],
            )


class TestAsyncTestCaseResults:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        test_case_result = await async_client.evaluations.test_case_results.create(
            "string",
            application_spec_id="string",
            evaluation_dataset_version_num="string",
            test_case_evaluation_data={},
            test_case_evaluation_data_schema="GENERATION",
            test_case_id="string",
        )
        assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        test_case_result = await async_client.evaluations.test_case_results.create(
            "string",
            application_spec_id="string",
            evaluation_dataset_version_num="string",
            test_case_evaluation_data={},
            test_case_evaluation_data_schema="GENERATION",
            test_case_id="string",
            account_id="string",
            annotated_by_user_id="string",
            audit_comment="string",
            audit_required=True,
            audit_status="UNAUDITED",
            result={},
            time_spent_labeling_s=0,
            x_selected_account_id="string",
        )
        assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.test_case_results.with_raw_response.create(
            "string",
            application_spec_id="string",
            evaluation_dataset_version_num="string",
            test_case_evaluation_data={},
            test_case_evaluation_data_schema="GENERATION",
            test_case_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = await response.parse()
        assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.test_case_results.with_streaming_response.create(
            "string",
            application_spec_id="string",
            evaluation_dataset_version_num="string",
            test_case_evaluation_data={},
            test_case_evaluation_data_schema="GENERATION",
            test_case_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = await response.parse()
            assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.create(
                "",
                application_spec_id="string",
                evaluation_dataset_version_num="string",
                test_case_evaluation_data={},
                test_case_evaluation_data_schema="GENERATION",
                test_case_id="string",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        test_case_result = await async_client.evaluations.test_case_results.retrieve(
            "string",
            evaluation_id="string",
        )
        assert_matches_type(TestCaseResultResponseWithViews, test_case_result, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGP) -> None:
        test_case_result = await async_client.evaluations.test_case_results.retrieve(
            "string",
            evaluation_id="string",
            view=["AnnotationResults", "Task", "TestCaseVersion"],
        )
        assert_matches_type(TestCaseResultResponseWithViews, test_case_result, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.test_case_results.with_raw_response.retrieve(
            "string",
            evaluation_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = await response.parse()
        assert_matches_type(TestCaseResultResponseWithViews, test_case_result, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.test_case_results.with_streaming_response.retrieve(
            "string",
            evaluation_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = await response.parse()
            assert_matches_type(TestCaseResultResponseWithViews, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.retrieve(
                "string",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_result_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.retrieve(
                "",
                evaluation_id="string",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGP) -> None:
        test_case_result = await async_client.evaluations.test_case_results.update(
            "string",
            evaluation_id="string",
        )
        assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGP) -> None:
        test_case_result = await async_client.evaluations.test_case_results.update(
            "string",
            evaluation_id="string",
            annotated_by_user_id="string",
            application_spec_id="string",
            audit_comment="string",
            audit_required=True,
            audit_status="UNAUDITED",
            evaluation_dataset_version_num="string",
            result={},
            test_case_evaluation_data={},
            test_case_evaluation_data_schema="GENERATION",
            test_case_id="string",
            time_spent_labeling_s=0,
        )
        assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.test_case_results.with_raw_response.update(
            "string",
            evaluation_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = await response.parse()
        assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.test_case_results.with_streaming_response.update(
            "string",
            evaluation_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = await response.parse()
            assert_matches_type(TestCaseResultResponse, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.update(
                "string",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_result_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.update(
                "",
                evaluation_id="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        test_case_result = await async_client.evaluations.test_case_results.list(
            "string",
        )
        assert_matches_type(TestCaseResultListResponse, test_case_result, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        test_case_result = await async_client.evaluations.test_case_results.list(
            "string",
            account_id="string",
            include_archived=True,
            limit=1,
            page=1,
            view=["AnnotationResults", "Task", "TestCaseVersion"],
            x_selected_account_id="string",
        )
        assert_matches_type(TestCaseResultListResponse, test_case_result, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.test_case_results.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = await response.parse()
        assert_matches_type(TestCaseResultListResponse, test_case_result, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.test_case_results.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = await response.parse()
            assert_matches_type(TestCaseResultListResponse, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_batch(self, async_client: AsyncSGP) -> None:
        test_case_result = await async_client.evaluations.test_case_results.batch(
            "string",
            body=[
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
            ],
        )
        assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

    @parametrize
    async def test_method_batch_with_all_params(self, async_client: AsyncSGP) -> None:
        test_case_result = await async_client.evaluations.test_case_results.batch(
            "string",
            body=[
                {
                    "audit_status": "UNAUDITED",
                    "audit_required": True,
                    "audit_comment": "string",
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                    "result": {},
                    "time_spent_labeling_s": 0,
                    "account_id": "string",
                    "annotated_by_user_id": "string",
                },
                {
                    "audit_status": "UNAUDITED",
                    "audit_required": True,
                    "audit_comment": "string",
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                    "result": {},
                    "time_spent_labeling_s": 0,
                    "account_id": "string",
                    "annotated_by_user_id": "string",
                },
                {
                    "audit_status": "UNAUDITED",
                    "audit_required": True,
                    "audit_comment": "string",
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                    "result": {},
                    "time_spent_labeling_s": 0,
                    "account_id": "string",
                    "annotated_by_user_id": "string",
                },
            ],
            x_selected_account_id="string",
        )
        assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

    @parametrize
    async def test_raw_response_batch(self, async_client: AsyncSGP) -> None:
        response = await async_client.evaluations.test_case_results.with_raw_response.batch(
            "string",
            body=[
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case_result = await response.parse()
        assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

    @parametrize
    async def test_streaming_response_batch(self, async_client: AsyncSGP) -> None:
        async with async_client.evaluations.test_case_results.with_streaming_response.batch(
            "string",
            body=[
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
                {
                    "application_spec_id": "string",
                    "evaluation_dataset_version_num": "string",
                    "test_case_id": "string",
                    "test_case_evaluation_data": {},
                    "test_case_evaluation_data_schema": "GENERATION",
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case_result = await response.parse()
            assert_matches_type(TestCaseResultBatchResponse, test_case_result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_batch(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.test_case_results.with_raw_response.batch(
                "",
                body=[
                    {
                        "application_spec_id": "string",
                        "evaluation_dataset_version_num": "string",
                        "test_case_id": "string",
                        "test_case_evaluation_data": {},
                        "test_case_evaluation_data_schema": "GENERATION",
                    },
                    {
                        "application_spec_id": "string",
                        "evaluation_dataset_version_num": "string",
                        "test_case_id": "string",
                        "test_case_evaluation_data": {},
                        "test_case_evaluation_data_schema": "GENERATION",
                    },
                    {
                        "application_spec_id": "string",
                        "evaluation_dataset_version_num": "string",
                        "test_case_id": "string",
                        "test_case_evaluation_data": {},
                        "test_case_evaluation_data_schema": "GENERATION",
                    },
                ],
            )
