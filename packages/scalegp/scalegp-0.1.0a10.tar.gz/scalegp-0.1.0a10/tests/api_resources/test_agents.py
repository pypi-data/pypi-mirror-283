# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import ExecuteAgentResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAgents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_execute(self, client: SGP) -> None:
        agent = client.agents.execute(
            messages=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            model="gpt-4",
            tools=[
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
            ],
        )
        assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

    @parametrize
    def test_method_execute_with_all_params(self, client: SGP) -> None:
        agent = client.agents.execute(
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
            tools=[
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {
                        "type": "object",
                        "properties": {
                            "foo": {
                                "type": "string",
                                "description": "string",
                                "default": "string",
                                "examples": ["string", "string", "string"],
                            }
                        },
                    },
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {
                        "type": "object",
                        "properties": {
                            "foo": {
                                "type": "string",
                                "description": "string",
                                "default": "string",
                                "examples": ["string", "string", "string"],
                            }
                        },
                    },
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {
                        "type": "object",
                        "properties": {
                            "foo": {
                                "type": "string",
                                "description": "string",
                                "default": "string",
                                "examples": ["string", "string", "string"],
                            }
                        },
                    },
                },
            ],
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
        )
        assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

    @parametrize
    def test_raw_response_execute(self, client: SGP) -> None:
        response = client.agents.with_raw_response.execute(
            messages=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            model="gpt-4",
            tools=[
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

    @parametrize
    def test_streaming_response_execute(self, client: SGP) -> None:
        with client.agents.with_streaming_response.execute(
            messages=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            model="gpt-4",
            tools=[
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAgents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_execute(self, async_client: AsyncSGP) -> None:
        agent = await async_client.agents.execute(
            messages=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            model="gpt-4",
            tools=[
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
            ],
        )
        assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

    @parametrize
    async def test_method_execute_with_all_params(self, async_client: AsyncSGP) -> None:
        agent = await async_client.agents.execute(
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
            tools=[
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {
                        "type": "object",
                        "properties": {
                            "foo": {
                                "type": "string",
                                "description": "string",
                                "default": "string",
                                "examples": ["string", "string", "string"],
                            }
                        },
                    },
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {
                        "type": "object",
                        "properties": {
                            "foo": {
                                "type": "string",
                                "description": "string",
                                "default": "string",
                                "examples": ["string", "string", "string"],
                            }
                        },
                    },
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {
                        "type": "object",
                        "properties": {
                            "foo": {
                                "type": "string",
                                "description": "string",
                                "default": "string",
                                "examples": ["string", "string", "string"],
                            }
                        },
                    },
                },
            ],
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
        )
        assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

    @parametrize
    async def test_raw_response_execute(self, async_client: AsyncSGP) -> None:
        response = await async_client.agents.with_raw_response.execute(
            messages=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            model="gpt-4",
            tools=[
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

    @parametrize
    async def test_streaming_response_execute(self, async_client: AsyncSGP) -> None:
        async with async_client.agents.with_streaming_response.execute(
            messages=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            model="gpt-4",
            tools=[
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
                {
                    "name": "string",
                    "description": "string",
                    "arguments": {"type": "object"},
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(ExecuteAgentResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True
