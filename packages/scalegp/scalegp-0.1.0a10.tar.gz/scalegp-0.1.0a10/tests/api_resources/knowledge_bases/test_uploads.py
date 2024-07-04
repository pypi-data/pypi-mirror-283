# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.knowledge_bases import (
    KnowledgeBaseUploadList,
    GetKnowledgeBaseV2UploadResponse,
    CancelKnowledgeBaseV2UploadResponse,
    CreateKnowledgeBaseV2UploadResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUploads:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_overload_1(self, client: SGP) -> None:
        upload = client.knowledge_bases.uploads.create(
            "string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
        )
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: SGP) -> None:
        upload = client.knowledge_bases.uploads.create(
            "string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "s3_prefix": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
            chunking_strategy_config={
                "strategy": "character",
                "separator": "string",
                "chunk_size": 1,
                "chunk_overlap": 0,
            },
            data_source_auth_config={
                "encrypted": True,
                "source": "SharePoint",
                "client_secret": "string",
            },
            force_reupload=True,
        )
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_raw_response_create_overload_1(self, client: SGP) -> None:
        response = client.knowledge_bases.uploads.with_raw_response.create(
            "string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_1(self, client: SGP) -> None:
        with client.knowledge_bases.uploads.with_streaming_response.create(
            "string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_overload_1(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.create(
                "",
                data_source_config={
                    "source": "S3",
                    "s3_bucket": "string",
                    "aws_region": "string",
                    "aws_account_id": "string",
                },
            )

    @parametrize
    def test_method_create_overload_2(self, client: SGP) -> None:
        upload = client.knowledge_bases.uploads.create(
            "string",
            data_source_config={
                "source": "LocalChunks",
                "artifact_name": "string",
                "artifact_uri": "string",
            },
        )
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: SGP) -> None:
        upload = client.knowledge_bases.uploads.create(
            "string",
            data_source_config={
                "source": "LocalChunks",
                "artifact_name": "string",
                "artifact_uri": "string",
                "deduplication_strategy": "Overwrite",
            },
            chunks=[
                {
                    "text": "string",
                    "chunk_position": 0,
                    "metadata": {},
                },
                {
                    "text": "string",
                    "chunk_position": 0,
                    "metadata": {},
                },
                {
                    "text": "string",
                    "chunk_position": 0,
                    "metadata": {},
                },
            ],
            force_reupload=True,
        )
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_raw_response_create_overload_2(self, client: SGP) -> None:
        response = client.knowledge_bases.uploads.with_raw_response.create(
            "string",
            data_source_config={
                "source": "LocalChunks",
                "artifact_name": "string",
                "artifact_uri": "string",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_2(self, client: SGP) -> None:
        with client.knowledge_bases.uploads.with_streaming_response.create(
            "string",
            data_source_config={
                "source": "LocalChunks",
                "artifact_name": "string",
                "artifact_uri": "string",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_overload_2(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.create(
                "",
                data_source_config={
                    "source": "LocalChunks",
                    "artifact_name": "string",
                    "artifact_uri": "string",
                },
            )

    @parametrize
    def test_method_create_overload_3(self, client: SGP) -> None:
        upload = client.knowledge_bases.uploads.create(
            "string",
            chunking_strategy_config={"strategy": "character"},
            data_source_id="string",
        )
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_3(self, client: SGP) -> None:
        upload = client.knowledge_bases.uploads.create(
            "string",
            chunking_strategy_config={
                "strategy": "character",
                "separator": "string",
                "chunk_size": 1,
                "chunk_overlap": 0,
            },
            data_source_id="string",
            force_reupload=True,
        )
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_raw_response_create_overload_3(self, client: SGP) -> None:
        response = client.knowledge_bases.uploads.with_raw_response.create(
            "string",
            chunking_strategy_config={"strategy": "character"},
            data_source_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_3(self, client: SGP) -> None:
        with client.knowledge_bases.uploads.with_streaming_response.create(
            "string",
            chunking_strategy_config={"strategy": "character"},
            data_source_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_overload_3(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.create(
                "",
                chunking_strategy_config={"strategy": "character"},
                data_source_id="string",
            )

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        upload = client.knowledge_bases.uploads.retrieve(
            "string",
            knowledge_base_id="string",
        )
        assert_matches_type(GetKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGP) -> None:
        upload = client.knowledge_bases.uploads.retrieve(
            "string",
            knowledge_base_id="string",
            include_artifact_list=True,
        )
        assert_matches_type(GetKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.knowledge_bases.uploads.with_raw_response.retrieve(
            "string",
            knowledge_base_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(GetKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.knowledge_bases.uploads.with_streaming_response.retrieve(
            "string",
            knowledge_base_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(GetKnowledgeBaseV2UploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.retrieve(
                "string",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.retrieve(
                "",
                knowledge_base_id="string",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        upload = client.knowledge_bases.uploads.list(
            "string",
        )
        assert_matches_type(KnowledgeBaseUploadList, upload, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        upload = client.knowledge_bases.uploads.list(
            "string",
            limit=1,
            page=1,
            status="Running",
        )
        assert_matches_type(KnowledgeBaseUploadList, upload, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.knowledge_bases.uploads.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(KnowledgeBaseUploadList, upload, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.knowledge_bases.uploads.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(KnowledgeBaseUploadList, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_cancel(self, client: SGP) -> None:
        upload = client.knowledge_bases.uploads.cancel(
            "string",
            knowledge_base_id="string",
        )
        assert_matches_type(CancelKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_raw_response_cancel(self, client: SGP) -> None:
        response = client.knowledge_bases.uploads.with_raw_response.cancel(
            "string",
            knowledge_base_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(CancelKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    def test_streaming_response_cancel(self, client: SGP) -> None:
        with client.knowledge_bases.uploads.with_streaming_response.cancel(
            "string",
            knowledge_base_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(CancelKnowledgeBaseV2UploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_cancel(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.cancel(
                "string",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.cancel(
                "",
                knowledge_base_id="string",
            )


class TestAsyncUploads:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncSGP) -> None:
        upload = await async_client.knowledge_bases.uploads.create(
            "string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
        )
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncSGP) -> None:
        upload = await async_client.knowledge_bases.uploads.create(
            "string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "s3_prefix": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
            chunking_strategy_config={
                "strategy": "character",
                "separator": "string",
                "chunk_size": 1,
                "chunk_overlap": 0,
            },
            data_source_auth_config={
                "encrypted": True,
                "source": "SharePoint",
                "client_secret": "string",
            },
            force_reupload=True,
        )
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.uploads.with_raw_response.create(
            "string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.uploads.with_streaming_response.create(
            "string",
            data_source_config={
                "source": "S3",
                "s3_bucket": "string",
                "aws_region": "string",
                "aws_account_id": "string",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_overload_1(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.create(
                "",
                data_source_config={
                    "source": "S3",
                    "s3_bucket": "string",
                    "aws_region": "string",
                    "aws_account_id": "string",
                },
            )

    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncSGP) -> None:
        upload = await async_client.knowledge_bases.uploads.create(
            "string",
            data_source_config={
                "source": "LocalChunks",
                "artifact_name": "string",
                "artifact_uri": "string",
            },
        )
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncSGP) -> None:
        upload = await async_client.knowledge_bases.uploads.create(
            "string",
            data_source_config={
                "source": "LocalChunks",
                "artifact_name": "string",
                "artifact_uri": "string",
                "deduplication_strategy": "Overwrite",
            },
            chunks=[
                {
                    "text": "string",
                    "chunk_position": 0,
                    "metadata": {},
                },
                {
                    "text": "string",
                    "chunk_position": 0,
                    "metadata": {},
                },
                {
                    "text": "string",
                    "chunk_position": 0,
                    "metadata": {},
                },
            ],
            force_reupload=True,
        )
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.uploads.with_raw_response.create(
            "string",
            data_source_config={
                "source": "LocalChunks",
                "artifact_name": "string",
                "artifact_uri": "string",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.uploads.with_streaming_response.create(
            "string",
            data_source_config={
                "source": "LocalChunks",
                "artifact_name": "string",
                "artifact_uri": "string",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_overload_2(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.create(
                "",
                data_source_config={
                    "source": "LocalChunks",
                    "artifact_name": "string",
                    "artifact_uri": "string",
                },
            )

    @parametrize
    async def test_method_create_overload_3(self, async_client: AsyncSGP) -> None:
        upload = await async_client.knowledge_bases.uploads.create(
            "string",
            chunking_strategy_config={"strategy": "character"},
            data_source_id="string",
        )
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_3(self, async_client: AsyncSGP) -> None:
        upload = await async_client.knowledge_bases.uploads.create(
            "string",
            chunking_strategy_config={
                "strategy": "character",
                "separator": "string",
                "chunk_size": 1,
                "chunk_overlap": 0,
            },
            data_source_id="string",
            force_reupload=True,
        )
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_3(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.uploads.with_raw_response.create(
            "string",
            chunking_strategy_config={"strategy": "character"},
            data_source_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_3(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.uploads.with_streaming_response.create(
            "string",
            chunking_strategy_config={"strategy": "character"},
            data_source_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(CreateKnowledgeBaseV2UploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_overload_3(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.create(
                "",
                chunking_strategy_config={"strategy": "character"},
                data_source_id="string",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        upload = await async_client.knowledge_bases.uploads.retrieve(
            "string",
            knowledge_base_id="string",
        )
        assert_matches_type(GetKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGP) -> None:
        upload = await async_client.knowledge_bases.uploads.retrieve(
            "string",
            knowledge_base_id="string",
            include_artifact_list=True,
        )
        assert_matches_type(GetKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.uploads.with_raw_response.retrieve(
            "string",
            knowledge_base_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(GetKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.uploads.with_streaming_response.retrieve(
            "string",
            knowledge_base_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(GetKnowledgeBaseV2UploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.retrieve(
                "string",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.retrieve(
                "",
                knowledge_base_id="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        upload = await async_client.knowledge_bases.uploads.list(
            "string",
        )
        assert_matches_type(KnowledgeBaseUploadList, upload, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        upload = await async_client.knowledge_bases.uploads.list(
            "string",
            limit=1,
            page=1,
            status="Running",
        )
        assert_matches_type(KnowledgeBaseUploadList, upload, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.uploads.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(KnowledgeBaseUploadList, upload, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.uploads.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(KnowledgeBaseUploadList, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_cancel(self, async_client: AsyncSGP) -> None:
        upload = await async_client.knowledge_bases.uploads.cancel(
            "string",
            knowledge_base_id="string",
        )
        assert_matches_type(CancelKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.uploads.with_raw_response.cancel(
            "string",
            knowledge_base_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(CancelKnowledgeBaseV2UploadResponse, upload, path=["response"])

    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.uploads.with_streaming_response.cancel(
            "string",
            knowledge_base_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(CancelKnowledgeBaseV2UploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.cancel(
                "string",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.cancel(
                "",
                knowledge_base_id="string",
            )
