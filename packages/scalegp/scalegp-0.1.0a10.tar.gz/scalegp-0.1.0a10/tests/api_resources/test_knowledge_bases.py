# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import (
    KnowledgeBaseItemV2,
    KnowledgeBaseItemV2List,
    CreateKnowledgeBaseResponse,
    DeleteKnowledgeBaseResponseV2,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestKnowledgeBases:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        knowledge_base = client.knowledge_bases.create(
            embedding_config={
                "type": "models_api",
                "model_deployment_id": "string",
            },
            knowledge_base_name="string",
        )
        assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        knowledge_base = client.knowledge_bases.create(
            embedding_config={
                "type": "models_api",
                "model_deployment_id": "string",
            },
            knowledge_base_name="string",
            account_id="string",
            metadata={},
        )
        assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.knowledge_bases.with_raw_response.create(
            embedding_config={
                "type": "models_api",
                "model_deployment_id": "string",
            },
            knowledge_base_name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = response.parse()
        assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.knowledge_bases.with_streaming_response.create(
            embedding_config={
                "type": "models_api",
                "model_deployment_id": "string",
            },
            knowledge_base_name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = response.parse()
            assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        knowledge_base = client.knowledge_bases.retrieve(
            "string",
        )
        assert_matches_type(KnowledgeBaseItemV2, knowledge_base, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGP) -> None:
        knowledge_base = client.knowledge_bases.retrieve(
            "string",
            include_artifacts_status=True,
            view=["Connections", "ArtifactCount"],
        )
        assert_matches_type(KnowledgeBaseItemV2, knowledge_base, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.knowledge_bases.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = response.parse()
        assert_matches_type(KnowledgeBaseItemV2, knowledge_base, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.knowledge_bases.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = response.parse()
            assert_matches_type(KnowledgeBaseItemV2, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        knowledge_base = client.knowledge_bases.list()
        assert_matches_type(KnowledgeBaseItemV2List, knowledge_base, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        knowledge_base = client.knowledge_bases.list(
            account_id="string",
            limit=1,
            page=1,
            view=["Connections", "ArtifactCount"],
        )
        assert_matches_type(KnowledgeBaseItemV2List, knowledge_base, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.knowledge_bases.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = response.parse()
        assert_matches_type(KnowledgeBaseItemV2List, knowledge_base, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.knowledge_bases.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = response.parse()
            assert_matches_type(KnowledgeBaseItemV2List, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        knowledge_base = client.knowledge_bases.delete(
            "string",
        )
        assert_matches_type(DeleteKnowledgeBaseResponseV2, knowledge_base, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.knowledge_bases.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = response.parse()
        assert_matches_type(DeleteKnowledgeBaseResponseV2, knowledge_base, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.knowledge_bases.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = response.parse()
            assert_matches_type(DeleteKnowledgeBaseResponseV2, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_query(self, client: SGP) -> None:
        knowledge_base = client.knowledge_bases.query(
            "string",
            query="string",
            top_k=1,
        )
        assert_matches_type(object, knowledge_base, path=["response"])

    @parametrize
    def test_method_query_with_all_params(self, client: SGP) -> None:
        knowledge_base = client.knowledge_bases.query(
            "string",
            query="string",
            top_k=1,
            include_embeddings=True,
            metadata_filters={},
            verbose=True,
        )
        assert_matches_type(object, knowledge_base, path=["response"])

    @parametrize
    def test_raw_response_query(self, client: SGP) -> None:
        response = client.knowledge_bases.with_raw_response.query(
            "string",
            query="string",
            top_k=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = response.parse()
        assert_matches_type(object, knowledge_base, path=["response"])

    @parametrize
    def test_streaming_response_query(self, client: SGP) -> None:
        with client.knowledge_bases.with_streaming_response.query(
            "string",
            query="string",
            top_k=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = response.parse()
            assert_matches_type(object, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_query(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.with_raw_response.query(
                "",
                query="string",
                top_k=1,
            )


class TestAsyncKnowledgeBases:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        knowledge_base = await async_client.knowledge_bases.create(
            embedding_config={
                "type": "models_api",
                "model_deployment_id": "string",
            },
            knowledge_base_name="string",
        )
        assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        knowledge_base = await async_client.knowledge_bases.create(
            embedding_config={
                "type": "models_api",
                "model_deployment_id": "string",
            },
            knowledge_base_name="string",
            account_id="string",
            metadata={},
        )
        assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.with_raw_response.create(
            embedding_config={
                "type": "models_api",
                "model_deployment_id": "string",
            },
            knowledge_base_name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = await response.parse()
        assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.with_streaming_response.create(
            embedding_config={
                "type": "models_api",
                "model_deployment_id": "string",
            },
            knowledge_base_name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = await response.parse()
            assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        knowledge_base = await async_client.knowledge_bases.retrieve(
            "string",
        )
        assert_matches_type(KnowledgeBaseItemV2, knowledge_base, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGP) -> None:
        knowledge_base = await async_client.knowledge_bases.retrieve(
            "string",
            include_artifacts_status=True,
            view=["Connections", "ArtifactCount"],
        )
        assert_matches_type(KnowledgeBaseItemV2, knowledge_base, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = await response.parse()
        assert_matches_type(KnowledgeBaseItemV2, knowledge_base, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = await response.parse()
            assert_matches_type(KnowledgeBaseItemV2, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        knowledge_base = await async_client.knowledge_bases.list()
        assert_matches_type(KnowledgeBaseItemV2List, knowledge_base, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        knowledge_base = await async_client.knowledge_bases.list(
            account_id="string",
            limit=1,
            page=1,
            view=["Connections", "ArtifactCount"],
        )
        assert_matches_type(KnowledgeBaseItemV2List, knowledge_base, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = await response.parse()
        assert_matches_type(KnowledgeBaseItemV2List, knowledge_base, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = await response.parse()
            assert_matches_type(KnowledgeBaseItemV2List, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        knowledge_base = await async_client.knowledge_bases.delete(
            "string",
        )
        assert_matches_type(DeleteKnowledgeBaseResponseV2, knowledge_base, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = await response.parse()
        assert_matches_type(DeleteKnowledgeBaseResponseV2, knowledge_base, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = await response.parse()
            assert_matches_type(DeleteKnowledgeBaseResponseV2, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_query(self, async_client: AsyncSGP) -> None:
        knowledge_base = await async_client.knowledge_bases.query(
            "string",
            query="string",
            top_k=1,
        )
        assert_matches_type(object, knowledge_base, path=["response"])

    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncSGP) -> None:
        knowledge_base = await async_client.knowledge_bases.query(
            "string",
            query="string",
            top_k=1,
            include_embeddings=True,
            metadata_filters={},
            verbose=True,
        )
        assert_matches_type(object, knowledge_base, path=["response"])

    @parametrize
    async def test_raw_response_query(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.with_raw_response.query(
            "string",
            query="string",
            top_k=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = await response.parse()
        assert_matches_type(object, knowledge_base, path=["response"])

    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.with_streaming_response.query(
            "string",
            query="string",
            top_k=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = await response.parse()
            assert_matches_type(object, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_query(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.with_raw_response.query(
                "",
                query="string",
                top_k=1,
            )
