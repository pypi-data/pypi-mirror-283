# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import (
    KnowledgeBaseDataSourceResponse,
    KnowledgeBaseDataSourceListResponse,
)
from scalegp.types.shared import DeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestKnowledgeBaseDataSources:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.create(
            account_id="string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
            name="string",
        )
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.create(
            account_id="string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "s3_prefix": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
            name="string",
            data_source_auth_config={
                "encrypted": True,
                "source": "SharePoint",
                "client_secret": "string",
            },
            description="string",
            x_selected_account_id="string",
        )
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.knowledge_base_data_sources.with_raw_response.create(
            account_id="string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
            name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = response.parse()
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.knowledge_base_data_sources.with_streaming_response.create(
            account_id="string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
            name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = response.parse()
            assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.retrieve(
            "string",
        )
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.knowledge_base_data_sources.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = response.parse()
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.knowledge_base_data_sources.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = response.parse()
            assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            client.knowledge_base_data_sources.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SGP) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.update(
            "string",
        )
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGP) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.update(
            "string",
            data_source_auth_config={
                "encrypted": True,
                "source": "SharePoint",
                "client_secret": "string",
            },
            description="string",
            name="string",
        )
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGP) -> None:
        response = client.knowledge_base_data_sources.with_raw_response.update(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = response.parse()
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGP) -> None:
        with client.knowledge_base_data_sources.with_streaming_response.update(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = response.parse()
            assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            client.knowledge_base_data_sources.with_raw_response.update(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.list()
        assert_matches_type(KnowledgeBaseDataSourceListResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.list(
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(KnowledgeBaseDataSourceListResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.knowledge_base_data_sources.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = response.parse()
        assert_matches_type(KnowledgeBaseDataSourceListResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.knowledge_base_data_sources.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = response.parse()
            assert_matches_type(KnowledgeBaseDataSourceListResponse, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.knowledge_base_data_sources.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = response.parse()
        assert_matches_type(DeleteResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.knowledge_base_data_sources.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = response.parse()
            assert_matches_type(DeleteResponse, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            client.knowledge_base_data_sources.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_verify(self, client: SGP) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.verify(
            "string",
        )
        assert_matches_type(object, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_raw_response_verify(self, client: SGP) -> None:
        response = client.knowledge_base_data_sources.with_raw_response.verify(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = response.parse()
        assert_matches_type(object, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_streaming_response_verify(self, client: SGP) -> None:
        with client.knowledge_base_data_sources.with_streaming_response.verify(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = response.parse()
            assert_matches_type(object, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_verify(self, client: SGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            client.knowledge_base_data_sources.with_raw_response.verify(
                "",
            )


class TestAsyncKnowledgeBaseDataSources:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.create(
            account_id="string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
            name="string",
        )
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.create(
            account_id="string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "s3_prefix": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
            name="string",
            data_source_auth_config={
                "encrypted": True,
                "source": "SharePoint",
                "client_secret": "string",
            },
            description="string",
            x_selected_account_id="string",
        )
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_base_data_sources.with_raw_response.create(
            account_id="string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
            name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = await response.parse()
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_base_data_sources.with_streaming_response.create(
            account_id="string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
            name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = await response.parse()
            assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.retrieve(
            "string",
        )
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_base_data_sources.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = await response.parse()
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_base_data_sources.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = await response.parse()
            assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            await async_client.knowledge_base_data_sources.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGP) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.update(
            "string",
        )
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGP) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.update(
            "string",
            data_source_auth_config={
                "encrypted": True,
                "source": "SharePoint",
                "client_secret": "string",
            },
            description="string",
            name="string",
        )
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_base_data_sources.with_raw_response.update(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = await response.parse()
        assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_base_data_sources.with_streaming_response.update(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = await response.parse()
            assert_matches_type(KnowledgeBaseDataSourceResponse, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            await async_client.knowledge_base_data_sources.with_raw_response.update(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.list()
        assert_matches_type(KnowledgeBaseDataSourceListResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.list(
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(KnowledgeBaseDataSourceListResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_base_data_sources.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = await response.parse()
        assert_matches_type(KnowledgeBaseDataSourceListResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_base_data_sources.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = await response.parse()
            assert_matches_type(KnowledgeBaseDataSourceListResponse, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_base_data_sources.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = await response.parse()
        assert_matches_type(DeleteResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_base_data_sources.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = await response.parse()
            assert_matches_type(DeleteResponse, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            await async_client.knowledge_base_data_sources.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_verify(self, async_client: AsyncSGP) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.verify(
            "string",
        )
        assert_matches_type(object, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_raw_response_verify(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_base_data_sources.with_raw_response.verify(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = await response.parse()
        assert_matches_type(object, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_streaming_response_verify(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_base_data_sources.with_streaming_response.verify(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = await response.parse()
            assert_matches_type(object, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_verify(self, async_client: AsyncSGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            await async_client.knowledge_base_data_sources.with_raw_response.verify(
                "",
            )
