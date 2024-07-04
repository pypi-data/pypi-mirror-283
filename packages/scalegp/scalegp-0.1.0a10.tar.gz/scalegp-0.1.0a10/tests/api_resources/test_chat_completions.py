# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import CreateChatCompletionResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChatCompletions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        chat_completion = client.chat_completions.create(
            messages=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            model="gpt-4",
        )
        assert_matches_type(CreateChatCompletionResponse, chat_completion, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        chat_completion = client.chat_completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "string",
                },
                {
                    "role": "user",
                    "content": "string",
                },
                {
                    "role": "user",
                    "content": "string",
                },
            ],
            model="gpt-4",
            chat_template="string",
            instructions="string",
            memory_strategy={
                "name": "last_k",
                "params": {"k": 1},
            },
            model_parameters={
                "temperature": 0,
                "stop_sequences": ["string", "string", "string"],
                "max_tokens": 0,
                "top_p": 0,
                "top_k": 0,
                "frequency_penalty": 0,
                "presence_penalty": 0,
            },
            stream=True,
        )
        assert_matches_type(CreateChatCompletionResponse, chat_completion, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.chat_completions.with_raw_response.create(
            messages=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            model="gpt-4",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat_completion = response.parse()
        assert_matches_type(CreateChatCompletionResponse, chat_completion, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.chat_completions.with_streaming_response.create(
            messages=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            model="gpt-4",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat_completion = response.parse()
            assert_matches_type(CreateChatCompletionResponse, chat_completion, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncChatCompletions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        chat_completion = await async_client.chat_completions.create(
            messages=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            model="gpt-4",
        )
        assert_matches_type(CreateChatCompletionResponse, chat_completion, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        chat_completion = await async_client.chat_completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "string",
                },
                {
                    "role": "user",
                    "content": "string",
                },
                {
                    "role": "user",
                    "content": "string",
                },
            ],
            model="gpt-4",
            chat_template="string",
            instructions="string",
            memory_strategy={
                "name": "last_k",
                "params": {"k": 1},
            },
            model_parameters={
                "temperature": 0,
                "stop_sequences": ["string", "string", "string"],
                "max_tokens": 0,
                "top_p": 0,
                "top_k": 0,
                "frequency_penalty": 0,
                "presence_penalty": 0,
            },
            stream=True,
        )
        assert_matches_type(CreateChatCompletionResponse, chat_completion, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.chat_completions.with_raw_response.create(
            messages=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            model="gpt-4",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat_completion = await response.parse()
        assert_matches_type(CreateChatCompletionResponse, chat_completion, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.chat_completions.with_streaming_response.create(
            messages=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            model="gpt-4",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat_completion = await response.parse()
            assert_matches_type(CreateChatCompletionResponse, chat_completion, path=["response"])

        assert cast(Any, response.is_closed) is True
