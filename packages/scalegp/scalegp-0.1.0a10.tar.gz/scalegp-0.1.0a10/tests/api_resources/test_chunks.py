# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import ChunksRankResponse, SynthesizeChunksResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChunks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_rank(self, client: SGP) -> None:
        chunk = client.chunks.rank(
            query="string",
            rank_strategy={},
            relevant_chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
            ],
        )
        assert_matches_type(ChunksRankResponse, chunk, path=["response"])

    @parametrize
    def test_method_rank_with_all_params(self, client: SGP) -> None:
        chunk = client.chunks.rank(
            query="string",
            rank_strategy={
                "method": "cross_encoder",
                "params": {"cross_encoder_model": "cross-encoder/ms-marco-MiniLM-L-12-v2"},
            },
            relevant_chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "embedding": [0, 0, 0],
                    "metadata": {},
                    "user_supplied_metadata": {},
                    "attachment_url": "string",
                    "title": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "embedding": [0, 0, 0],
                    "metadata": {},
                    "user_supplied_metadata": {},
                    "attachment_url": "string",
                    "title": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "embedding": [0, 0, 0],
                    "metadata": {},
                    "user_supplied_metadata": {},
                    "attachment_url": "string",
                    "title": "string",
                    "score": 0,
                },
            ],
            account_id="string",
            top_k=1,
        )
        assert_matches_type(ChunksRankResponse, chunk, path=["response"])

    @parametrize
    def test_raw_response_rank(self, client: SGP) -> None:
        response = client.chunks.with_raw_response.rank(
            query="string",
            rank_strategy={},
            relevant_chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = response.parse()
        assert_matches_type(ChunksRankResponse, chunk, path=["response"])

    @parametrize
    def test_streaming_response_rank(self, client: SGP) -> None:
        with client.chunks.with_streaming_response.rank(
            query="string",
            rank_strategy={},
            relevant_chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = response.parse()
            assert_matches_type(ChunksRankResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_synthesis(self, client: SGP) -> None:
        chunk = client.chunks.synthesis(
            chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
            ],
            query="string",
        )
        assert_matches_type(SynthesizeChunksResponse, chunk, path=["response"])

    @parametrize
    def test_raw_response_synthesis(self, client: SGP) -> None:
        response = client.chunks.with_raw_response.synthesis(
            chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
            ],
            query="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = response.parse()
        assert_matches_type(SynthesizeChunksResponse, chunk, path=["response"])

    @parametrize
    def test_streaming_response_synthesis(self, client: SGP) -> None:
        with client.chunks.with_streaming_response.synthesis(
            chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
            ],
            query="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = response.parse()
            assert_matches_type(SynthesizeChunksResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncChunks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_rank(self, async_client: AsyncSGP) -> None:
        chunk = await async_client.chunks.rank(
            query="string",
            rank_strategy={},
            relevant_chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
            ],
        )
        assert_matches_type(ChunksRankResponse, chunk, path=["response"])

    @parametrize
    async def test_method_rank_with_all_params(self, async_client: AsyncSGP) -> None:
        chunk = await async_client.chunks.rank(
            query="string",
            rank_strategy={
                "method": "cross_encoder",
                "params": {"cross_encoder_model": "cross-encoder/ms-marco-MiniLM-L-12-v2"},
            },
            relevant_chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "embedding": [0, 0, 0],
                    "metadata": {},
                    "user_supplied_metadata": {},
                    "attachment_url": "string",
                    "title": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "embedding": [0, 0, 0],
                    "metadata": {},
                    "user_supplied_metadata": {},
                    "attachment_url": "string",
                    "title": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "embedding": [0, 0, 0],
                    "metadata": {},
                    "user_supplied_metadata": {},
                    "attachment_url": "string",
                    "title": "string",
                    "score": 0,
                },
            ],
            account_id="string",
            top_k=1,
        )
        assert_matches_type(ChunksRankResponse, chunk, path=["response"])

    @parametrize
    async def test_raw_response_rank(self, async_client: AsyncSGP) -> None:
        response = await async_client.chunks.with_raw_response.rank(
            query="string",
            rank_strategy={},
            relevant_chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = await response.parse()
        assert_matches_type(ChunksRankResponse, chunk, path=["response"])

    @parametrize
    async def test_streaming_response_rank(self, async_client: AsyncSGP) -> None:
        async with async_client.chunks.with_streaming_response.rank(
            query="string",
            rank_strategy={},
            relevant_chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = await response.parse()
            assert_matches_type(ChunksRankResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_synthesis(self, async_client: AsyncSGP) -> None:
        chunk = await async_client.chunks.synthesis(
            chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
            ],
            query="string",
        )
        assert_matches_type(SynthesizeChunksResponse, chunk, path=["response"])

    @parametrize
    async def test_raw_response_synthesis(self, async_client: AsyncSGP) -> None:
        response = await async_client.chunks.with_raw_response.synthesis(
            chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
            ],
            query="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = await response.parse()
        assert_matches_type(SynthesizeChunksResponse, chunk, path=["response"])

    @parametrize
    async def test_streaming_response_synthesis(self, async_client: AsyncSGP) -> None:
        async with async_client.chunks.with_streaming_response.synthesis(
            chunks=[
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
                {
                    "chunk_id": "string",
                    "text": "string",
                    "score": 0,
                },
            ],
            query="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = await response.parse()
            assert_matches_type(SynthesizeChunksResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True
