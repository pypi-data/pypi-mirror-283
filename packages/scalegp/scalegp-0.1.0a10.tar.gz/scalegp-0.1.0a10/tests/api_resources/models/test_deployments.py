# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.models import (
    EmbeddingResponse,
    RerankingResponse,
    CompletionResponse,
    ModelDeploymentResponse,
)
from scalegp.types.shared import DeleteResponse, PaginationResponseModelDeployment

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeployments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        deployment = client.models.deployments.create(
            "string",
            name="string",
        )
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        deployment = client.models.deployments.create(
            "string",
            name="string",
            account_id="string",
            deployment_metadata={},
            model_creation_parameters={},
            vendor_configuration={
                "min_workers": 0,
                "max_workers": 0,
                "per_worker": 0,
                "vendor": "LAUNCH",
            },
        )
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.models.deployments.with_raw_response.create(
            "string",
            name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.models.deployments.with_streaming_response.create(
            "string",
            name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            client.models.deployments.with_raw_response.create(
                "",
                name="string",
            )

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        deployment = client.models.deployments.retrieve(
            "string",
            model_instance_id="string",
        )
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.models.deployments.with_raw_response.retrieve(
            "string",
            model_instance_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.models.deployments.with_streaming_response.retrieve(
            "string",
            model_instance_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            client.models.deployments.with_raw_response.retrieve(
                "string",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.models.deployments.with_raw_response.retrieve(
                "",
                model_instance_id="string",
            )

    @parametrize
    def test_method_update(self, client: SGP) -> None:
        deployment = client.models.deployments.update(
            "string",
            model_instance_id="string",
        )
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGP) -> None:
        deployment = client.models.deployments.update(
            "string",
            model_instance_id="string",
            deployment_metadata={},
            model_creation_parameters={},
            name="string",
            vendor_configuration={
                "min_workers": 0,
                "max_workers": 0,
                "per_worker": 0,
                "vendor": "LAUNCH",
            },
        )
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGP) -> None:
        response = client.models.deployments.with_raw_response.update(
            "string",
            model_instance_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGP) -> None:
        with client.models.deployments.with_streaming_response.update(
            "string",
            model_instance_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            client.models.deployments.with_raw_response.update(
                "string",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.models.deployments.with_raw_response.update(
                "",
                model_instance_id="string",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        deployment = client.models.deployments.list(
            "string",
        )
        assert_matches_type(PaginationResponseModelDeployment, deployment, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        deployment = client.models.deployments.list(
            "string",
            account_id="string",
            limit=1,
            page=1,
            sort_by=["model_creation_parameters:asc", "model_creation_parameters:desc", "model_endpoint_id:asc"],
        )
        assert_matches_type(PaginationResponseModelDeployment, deployment, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.models.deployments.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(PaginationResponseModelDeployment, deployment, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.models.deployments.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(PaginationResponseModelDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            client.models.deployments.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        deployment = client.models.deployments.delete(
            "string",
            model_instance_id="string",
        )
        assert_matches_type(DeleteResponse, deployment, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.models.deployments.with_raw_response.delete(
            "string",
            model_instance_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(DeleteResponse, deployment, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.models.deployments.with_streaming_response.delete(
            "string",
            model_instance_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(DeleteResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            client.models.deployments.with_raw_response.delete(
                "string",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.models.deployments.with_raw_response.delete(
                "",
                model_instance_id="string",
            )

    @parametrize
    def test_method_chat_completions(self, client: SGP) -> None:
        deployment = client.models.deployments.chat_completions(
            "string",
            chat_history=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            prompt="string",
        )
        assert_matches_type(CompletionResponse, deployment, path=["response"])

    @parametrize
    def test_method_chat_completions_with_all_params(self, client: SGP) -> None:
        deployment = client.models.deployments.chat_completions(
            "string",
            chat_history=[
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
            prompt="string",
            frequency_penalty=0,
            max_tokens=0,
            model_request_parameters={"bindings": {"foo": "string"}},
            presence_penalty=0,
            stop_sequences=["string", "string", "string"],
            temperature=0,
            top_k=0,
            top_p=0,
        )
        assert_matches_type(CompletionResponse, deployment, path=["response"])

    @parametrize
    def test_raw_response_chat_completions(self, client: SGP) -> None:
        response = client.models.deployments.with_raw_response.chat_completions(
            "string",
            chat_history=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            prompt="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(CompletionResponse, deployment, path=["response"])

    @parametrize
    def test_streaming_response_chat_completions(self, client: SGP) -> None:
        with client.models.deployments.with_streaming_response.chat_completions(
            "string",
            chat_history=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            prompt="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(CompletionResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_chat_completions(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            client.models.deployments.with_raw_response.chat_completions(
                "",
                chat_history=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
                prompt="string",
            )

    @parametrize
    def test_method_completions(self, client: SGP) -> None:
        deployment = client.models.deployments.completions(
            "string",
            prompt="string",
        )
        assert_matches_type(CompletionResponse, deployment, path=["response"])

    @parametrize
    def test_method_completions_with_all_params(self, client: SGP) -> None:
        deployment = client.models.deployments.completions(
            "string",
            prompt="string",
            frequency_penalty=0,
            max_tokens=0,
            model_request_parameters={"bindings": {"foo": "string"}},
            presence_penalty=0,
            stop_sequences=["string", "string", "string"],
            temperature=0,
            top_k=0,
            top_p=0,
        )
        assert_matches_type(CompletionResponse, deployment, path=["response"])

    @parametrize
    def test_raw_response_completions(self, client: SGP) -> None:
        response = client.models.deployments.with_raw_response.completions(
            "string",
            prompt="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(CompletionResponse, deployment, path=["response"])

    @parametrize
    def test_streaming_response_completions(self, client: SGP) -> None:
        with client.models.deployments.with_streaming_response.completions(
            "string",
            prompt="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(CompletionResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_completions(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            client.models.deployments.with_raw_response.completions(
                "",
                prompt="string",
            )

    @parametrize
    def test_method_embeddings(self, client: SGP) -> None:
        deployment = client.models.deployments.embeddings(
            "string",
            texts=["string", "string", "string"],
        )
        assert_matches_type(EmbeddingResponse, deployment, path=["response"])

    @parametrize
    def test_method_embeddings_with_all_params(self, client: SGP) -> None:
        deployment = client.models.deployments.embeddings(
            "string",
            texts=["string", "string", "string"],
            model_request_parameters={"bindings": {"foo": "string"}},
        )
        assert_matches_type(EmbeddingResponse, deployment, path=["response"])

    @parametrize
    def test_raw_response_embeddings(self, client: SGP) -> None:
        response = client.models.deployments.with_raw_response.embeddings(
            "string",
            texts=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(EmbeddingResponse, deployment, path=["response"])

    @parametrize
    def test_streaming_response_embeddings(self, client: SGP) -> None:
        with client.models.deployments.with_streaming_response.embeddings(
            "string",
            texts=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(EmbeddingResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_embeddings(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            client.models.deployments.with_raw_response.embeddings(
                "",
                texts=["string", "string", "string"],
            )

    @parametrize
    def test_method_execute(self, client: SGP) -> None:
        deployment = client.models.deployments.execute(
            "string",
            model_instance_id="string",
        )
        assert_matches_type(object, deployment, path=["response"])

    @parametrize
    def test_raw_response_execute(self, client: SGP) -> None:
        response = client.models.deployments.with_raw_response.execute(
            "string",
            model_instance_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(object, deployment, path=["response"])

    @parametrize
    def test_streaming_response_execute(self, client: SGP) -> None:
        with client.models.deployments.with_streaming_response.execute(
            "string",
            model_instance_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(object, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_execute(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            client.models.deployments.with_raw_response.execute(
                "string",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            client.models.deployments.with_raw_response.execute(
                "",
                model_instance_id="string",
            )

    @parametrize
    def test_method_rerankings(self, client: SGP) -> None:
        deployment = client.models.deployments.rerankings(
            "string",
            chunks=["string", "string", "string"],
            query="string",
        )
        assert_matches_type(RerankingResponse, deployment, path=["response"])

    @parametrize
    def test_method_rerankings_with_all_params(self, client: SGP) -> None:
        deployment = client.models.deployments.rerankings(
            "string",
            chunks=["string", "string", "string"],
            query="string",
            model_request_parameters={"bindings": {"foo": "string"}},
        )
        assert_matches_type(RerankingResponse, deployment, path=["response"])

    @parametrize
    def test_raw_response_rerankings(self, client: SGP) -> None:
        response = client.models.deployments.with_raw_response.rerankings(
            "string",
            chunks=["string", "string", "string"],
            query="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(RerankingResponse, deployment, path=["response"])

    @parametrize
    def test_streaming_response_rerankings(self, client: SGP) -> None:
        with client.models.deployments.with_streaming_response.rerankings(
            "string",
            chunks=["string", "string", "string"],
            query="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(RerankingResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_rerankings(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            client.models.deployments.with_raw_response.rerankings(
                "",
                chunks=["string", "string", "string"],
                query="string",
            )


class TestAsyncDeployments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.create(
            "string",
            name="string",
        )
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.create(
            "string",
            name="string",
            account_id="string",
            deployment_metadata={},
            model_creation_parameters={},
            vendor_configuration={
                "min_workers": 0,
                "max_workers": 0,
                "per_worker": 0,
                "vendor": "LAUNCH",
            },
        )
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.deployments.with_raw_response.create(
            "string",
            name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.models.deployments.with_streaming_response.create(
            "string",
            name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            await async_client.models.deployments.with_raw_response.create(
                "",
                name="string",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.retrieve(
            "string",
            model_instance_id="string",
        )
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.deployments.with_raw_response.retrieve(
            "string",
            model_instance_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.models.deployments.with_streaming_response.retrieve(
            "string",
            model_instance_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            await async_client.models.deployments.with_raw_response.retrieve(
                "string",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.models.deployments.with_raw_response.retrieve(
                "",
                model_instance_id="string",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.update(
            "string",
            model_instance_id="string",
        )
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.update(
            "string",
            model_instance_id="string",
            deployment_metadata={},
            model_creation_parameters={},
            name="string",
            vendor_configuration={
                "min_workers": 0,
                "max_workers": 0,
                "per_worker": 0,
                "vendor": "LAUNCH",
            },
        )
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.deployments.with_raw_response.update(
            "string",
            model_instance_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGP) -> None:
        async with async_client.models.deployments.with_streaming_response.update(
            "string",
            model_instance_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(ModelDeploymentResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            await async_client.models.deployments.with_raw_response.update(
                "string",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.models.deployments.with_raw_response.update(
                "",
                model_instance_id="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.list(
            "string",
        )
        assert_matches_type(PaginationResponseModelDeployment, deployment, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.list(
            "string",
            account_id="string",
            limit=1,
            page=1,
            sort_by=["model_creation_parameters:asc", "model_creation_parameters:desc", "model_endpoint_id:asc"],
        )
        assert_matches_type(PaginationResponseModelDeployment, deployment, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.deployments.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(PaginationResponseModelDeployment, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.models.deployments.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(PaginationResponseModelDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            await async_client.models.deployments.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.delete(
            "string",
            model_instance_id="string",
        )
        assert_matches_type(DeleteResponse, deployment, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.deployments.with_raw_response.delete(
            "string",
            model_instance_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(DeleteResponse, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.models.deployments.with_streaming_response.delete(
            "string",
            model_instance_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(DeleteResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            await async_client.models.deployments.with_raw_response.delete(
                "string",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.models.deployments.with_raw_response.delete(
                "",
                model_instance_id="string",
            )

    @parametrize
    async def test_method_chat_completions(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.chat_completions(
            "string",
            chat_history=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            prompt="string",
        )
        assert_matches_type(CompletionResponse, deployment, path=["response"])

    @parametrize
    async def test_method_chat_completions_with_all_params(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.chat_completions(
            "string",
            chat_history=[
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
            prompt="string",
            frequency_penalty=0,
            max_tokens=0,
            model_request_parameters={"bindings": {"foo": "string"}},
            presence_penalty=0,
            stop_sequences=["string", "string", "string"],
            temperature=0,
            top_k=0,
            top_p=0,
        )
        assert_matches_type(CompletionResponse, deployment, path=["response"])

    @parametrize
    async def test_raw_response_chat_completions(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.deployments.with_raw_response.chat_completions(
            "string",
            chat_history=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            prompt="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(CompletionResponse, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_chat_completions(self, async_client: AsyncSGP) -> None:
        async with async_client.models.deployments.with_streaming_response.chat_completions(
            "string",
            chat_history=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
            prompt="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(CompletionResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_chat_completions(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            await async_client.models.deployments.with_raw_response.chat_completions(
                "",
                chat_history=[{"content": "string"}, {"content": "string"}, {"content": "string"}],
                prompt="string",
            )

    @parametrize
    async def test_method_completions(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.completions(
            "string",
            prompt="string",
        )
        assert_matches_type(CompletionResponse, deployment, path=["response"])

    @parametrize
    async def test_method_completions_with_all_params(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.completions(
            "string",
            prompt="string",
            frequency_penalty=0,
            max_tokens=0,
            model_request_parameters={"bindings": {"foo": "string"}},
            presence_penalty=0,
            stop_sequences=["string", "string", "string"],
            temperature=0,
            top_k=0,
            top_p=0,
        )
        assert_matches_type(CompletionResponse, deployment, path=["response"])

    @parametrize
    async def test_raw_response_completions(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.deployments.with_raw_response.completions(
            "string",
            prompt="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(CompletionResponse, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_completions(self, async_client: AsyncSGP) -> None:
        async with async_client.models.deployments.with_streaming_response.completions(
            "string",
            prompt="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(CompletionResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_completions(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            await async_client.models.deployments.with_raw_response.completions(
                "",
                prompt="string",
            )

    @parametrize
    async def test_method_embeddings(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.embeddings(
            "string",
            texts=["string", "string", "string"],
        )
        assert_matches_type(EmbeddingResponse, deployment, path=["response"])

    @parametrize
    async def test_method_embeddings_with_all_params(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.embeddings(
            "string",
            texts=["string", "string", "string"],
            model_request_parameters={"bindings": {"foo": "string"}},
        )
        assert_matches_type(EmbeddingResponse, deployment, path=["response"])

    @parametrize
    async def test_raw_response_embeddings(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.deployments.with_raw_response.embeddings(
            "string",
            texts=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(EmbeddingResponse, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_embeddings(self, async_client: AsyncSGP) -> None:
        async with async_client.models.deployments.with_streaming_response.embeddings(
            "string",
            texts=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(EmbeddingResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_embeddings(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            await async_client.models.deployments.with_raw_response.embeddings(
                "",
                texts=["string", "string", "string"],
            )

    @parametrize
    async def test_method_execute(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.execute(
            "string",
            model_instance_id="string",
        )
        assert_matches_type(object, deployment, path=["response"])

    @parametrize
    async def test_raw_response_execute(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.deployments.with_raw_response.execute(
            "string",
            model_instance_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(object, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_execute(self, async_client: AsyncSGP) -> None:
        async with async_client.models.deployments.with_streaming_response.execute(
            "string",
            model_instance_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(object, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_execute(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            await async_client.models.deployments.with_raw_response.execute(
                "string",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            await async_client.models.deployments.with_raw_response.execute(
                "",
                model_instance_id="string",
            )

    @parametrize
    async def test_method_rerankings(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.rerankings(
            "string",
            chunks=["string", "string", "string"],
            query="string",
        )
        assert_matches_type(RerankingResponse, deployment, path=["response"])

    @parametrize
    async def test_method_rerankings_with_all_params(self, async_client: AsyncSGP) -> None:
        deployment = await async_client.models.deployments.rerankings(
            "string",
            chunks=["string", "string", "string"],
            query="string",
            model_request_parameters={"bindings": {"foo": "string"}},
        )
        assert_matches_type(RerankingResponse, deployment, path=["response"])

    @parametrize
    async def test_raw_response_rerankings(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.deployments.with_raw_response.rerankings(
            "string",
            chunks=["string", "string", "string"],
            query="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(RerankingResponse, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_rerankings(self, async_client: AsyncSGP) -> None:
        async with async_client.models.deployments.with_streaming_response.rerankings(
            "string",
            chunks=["string", "string", "string"],
            query="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(RerankingResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_rerankings(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            await async_client.models.deployments.with_raw_response.rerankings(
                "",
                chunks=["string", "string", "string"],
                query="string",
            )
