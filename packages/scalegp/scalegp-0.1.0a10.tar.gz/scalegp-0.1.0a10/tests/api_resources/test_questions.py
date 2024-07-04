# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import QuestionResponse, QuestionListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestQuestions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        question = client.questions.create(
            account_id="string",
            prompt="string",
            title="string",
            type="categorical",
        )
        assert_matches_type(QuestionResponse, question, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        question = client.questions.create(
            account_id="string",
            prompt="string",
            title="string",
            type="categorical",
            choices=[{}, {}, {}],
            conditions=[{}, {}, {}],
            dropdown=True,
            multi=True,
            required=True,
            x_selected_account_id="string",
        )
        assert_matches_type(QuestionResponse, question, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.questions.with_raw_response.create(
            account_id="string",
            prompt="string",
            title="string",
            type="categorical",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = response.parse()
        assert_matches_type(QuestionResponse, question, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.questions.with_streaming_response.create(
            account_id="string",
            prompt="string",
            title="string",
            type="categorical",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = response.parse()
            assert_matches_type(QuestionResponse, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        question = client.questions.retrieve(
            "string",
        )
        assert_matches_type(QuestionResponse, question, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.questions.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = response.parse()
        assert_matches_type(QuestionResponse, question, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.questions.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = response.parse()
            assert_matches_type(QuestionResponse, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_id` but received ''"):
            client.questions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        question = client.questions.list()
        assert_matches_type(QuestionListResponse, question, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        question = client.questions.list(
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(QuestionListResponse, question, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.questions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = response.parse()
        assert_matches_type(QuestionListResponse, question, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.questions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = response.parse()
            assert_matches_type(QuestionListResponse, question, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncQuestions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        question = await async_client.questions.create(
            account_id="string",
            prompt="string",
            title="string",
            type="categorical",
        )
        assert_matches_type(QuestionResponse, question, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        question = await async_client.questions.create(
            account_id="string",
            prompt="string",
            title="string",
            type="categorical",
            choices=[{}, {}, {}],
            conditions=[{}, {}, {}],
            dropdown=True,
            multi=True,
            required=True,
            x_selected_account_id="string",
        )
        assert_matches_type(QuestionResponse, question, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.questions.with_raw_response.create(
            account_id="string",
            prompt="string",
            title="string",
            type="categorical",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = await response.parse()
        assert_matches_type(QuestionResponse, question, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.questions.with_streaming_response.create(
            account_id="string",
            prompt="string",
            title="string",
            type="categorical",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = await response.parse()
            assert_matches_type(QuestionResponse, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        question = await async_client.questions.retrieve(
            "string",
        )
        assert_matches_type(QuestionResponse, question, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.questions.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = await response.parse()
        assert_matches_type(QuestionResponse, question, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.questions.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = await response.parse()
            assert_matches_type(QuestionResponse, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_id` but received ''"):
            await async_client.questions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        question = await async_client.questions.list()
        assert_matches_type(QuestionListResponse, question, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        question = await async_client.questions.list(
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(QuestionListResponse, question, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.questions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = await response.parse()
        assert_matches_type(QuestionListResponse, question, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.questions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = await response.parse()
            assert_matches_type(QuestionListResponse, question, path=["response"])

        assert cast(Any, response.is_closed) is True
