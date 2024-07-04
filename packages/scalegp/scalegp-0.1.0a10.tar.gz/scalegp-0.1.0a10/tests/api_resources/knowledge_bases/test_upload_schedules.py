# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp._utils import parse_datetime
from scalegp.types.shared import DeleteResponse
from scalegp.types.knowledge_bases import (
    UploadScheduleListResponse,
    KnowledgeBaseUploadScheduleResponse,
    KnowledgeBaseUploadScheduleResponseWithViews,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUploadSchedules:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.create(
            "string",
            chunking_strategy_config={"strategy": "character"},
            interval=0,
            knowledge_base_data_source_id="string",
        )
        assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.create(
            "string",
            chunking_strategy_config={
                "strategy": "character",
                "separator": "string",
                "chunk_size": 1,
                "chunk_overlap": 0,
            },
            interval=0,
            knowledge_base_data_source_id="string",
            account_id="string",
            next_run_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            x_selected_account_id="string",
        )
        assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.knowledge_bases.upload_schedules.with_raw_response.create(
            "string",
            chunking_strategy_config={"strategy": "character"},
            interval=0,
            knowledge_base_data_source_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = response.parse()
        assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.knowledge_bases.upload_schedules.with_streaming_response.create(
            "string",
            chunking_strategy_config={"strategy": "character"},
            interval=0,
            knowledge_base_data_source_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = response.parse()
            assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.create(
                "",
                chunking_strategy_config={"strategy": "character"},
                interval=0,
                knowledge_base_data_source_id="string",
            )

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.retrieve(
            "string",
            knowledge_base_id="string",
        )
        assert_matches_type(KnowledgeBaseUploadScheduleResponseWithViews, upload_schedule, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGP) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.retrieve(
            "string",
            knowledge_base_id="string",
            view=["DataSource"],
        )
        assert_matches_type(KnowledgeBaseUploadScheduleResponseWithViews, upload_schedule, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.knowledge_bases.upload_schedules.with_raw_response.retrieve(
            "string",
            knowledge_base_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = response.parse()
        assert_matches_type(KnowledgeBaseUploadScheduleResponseWithViews, upload_schedule, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.knowledge_bases.upload_schedules.with_streaming_response.retrieve(
            "string",
            knowledge_base_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = response.parse()
            assert_matches_type(KnowledgeBaseUploadScheduleResponseWithViews, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.retrieve(
                "string",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_schedule_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.retrieve(
                "",
                knowledge_base_id="string",
            )

    @parametrize
    def test_method_update(self, client: SGP) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.update(
            "string",
            knowledge_base_id="string",
        )
        assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGP) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.update(
            "string",
            knowledge_base_id="string",
            chunking_strategy_config={
                "strategy": "character",
                "separator": "string",
                "chunk_size": 1,
                "chunk_overlap": 0,
            },
            interval=0,
            next_run_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGP) -> None:
        response = client.knowledge_bases.upload_schedules.with_raw_response.update(
            "string",
            knowledge_base_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = response.parse()
        assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGP) -> None:
        with client.knowledge_bases.upload_schedules.with_streaming_response.update(
            "string",
            knowledge_base_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = response.parse()
            assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.update(
                "string",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_schedule_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.update(
                "",
                knowledge_base_id="string",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.list(
            "string",
        )
        assert_matches_type(UploadScheduleListResponse, upload_schedule, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.list(
            "string",
            account_id="string",
            limit=1,
            page=1,
            view=["DataSource"],
            x_selected_account_id="string",
        )
        assert_matches_type(UploadScheduleListResponse, upload_schedule, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.knowledge_bases.upload_schedules.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = response.parse()
        assert_matches_type(UploadScheduleListResponse, upload_schedule, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.knowledge_bases.upload_schedules.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = response.parse()
            assert_matches_type(UploadScheduleListResponse, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.delete(
            "string",
            knowledge_base_id="string",
        )
        assert_matches_type(DeleteResponse, upload_schedule, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.knowledge_bases.upload_schedules.with_raw_response.delete(
            "string",
            knowledge_base_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = response.parse()
        assert_matches_type(DeleteResponse, upload_schedule, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.knowledge_bases.upload_schedules.with_streaming_response.delete(
            "string",
            knowledge_base_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = response.parse()
            assert_matches_type(DeleteResponse, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.delete(
                "string",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_schedule_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.delete(
                "",
                knowledge_base_id="string",
            )


class TestAsyncUploadSchedules:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.create(
            "string",
            chunking_strategy_config={"strategy": "character"},
            interval=0,
            knowledge_base_data_source_id="string",
        )
        assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.create(
            "string",
            chunking_strategy_config={
                "strategy": "character",
                "separator": "string",
                "chunk_size": 1,
                "chunk_overlap": 0,
            },
            interval=0,
            knowledge_base_data_source_id="string",
            account_id="string",
            next_run_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            x_selected_account_id="string",
        )
        assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.upload_schedules.with_raw_response.create(
            "string",
            chunking_strategy_config={"strategy": "character"},
            interval=0,
            knowledge_base_data_source_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = await response.parse()
        assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.upload_schedules.with_streaming_response.create(
            "string",
            chunking_strategy_config={"strategy": "character"},
            interval=0,
            knowledge_base_data_source_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = await response.parse()
            assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.create(
                "",
                chunking_strategy_config={"strategy": "character"},
                interval=0,
                knowledge_base_data_source_id="string",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.retrieve(
            "string",
            knowledge_base_id="string",
        )
        assert_matches_type(KnowledgeBaseUploadScheduleResponseWithViews, upload_schedule, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGP) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.retrieve(
            "string",
            knowledge_base_id="string",
            view=["DataSource"],
        )
        assert_matches_type(KnowledgeBaseUploadScheduleResponseWithViews, upload_schedule, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.upload_schedules.with_raw_response.retrieve(
            "string",
            knowledge_base_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = await response.parse()
        assert_matches_type(KnowledgeBaseUploadScheduleResponseWithViews, upload_schedule, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.upload_schedules.with_streaming_response.retrieve(
            "string",
            knowledge_base_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = await response.parse()
            assert_matches_type(KnowledgeBaseUploadScheduleResponseWithViews, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.retrieve(
                "string",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_schedule_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.retrieve(
                "",
                knowledge_base_id="string",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGP) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.update(
            "string",
            knowledge_base_id="string",
        )
        assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGP) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.update(
            "string",
            knowledge_base_id="string",
            chunking_strategy_config={
                "strategy": "character",
                "separator": "string",
                "chunk_size": 1,
                "chunk_overlap": 0,
            },
            interval=0,
            next_run_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.upload_schedules.with_raw_response.update(
            "string",
            knowledge_base_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = await response.parse()
        assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.upload_schedules.with_streaming_response.update(
            "string",
            knowledge_base_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = await response.parse()
            assert_matches_type(KnowledgeBaseUploadScheduleResponse, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.update(
                "string",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_schedule_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.update(
                "",
                knowledge_base_id="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.list(
            "string",
        )
        assert_matches_type(UploadScheduleListResponse, upload_schedule, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.list(
            "string",
            account_id="string",
            limit=1,
            page=1,
            view=["DataSource"],
            x_selected_account_id="string",
        )
        assert_matches_type(UploadScheduleListResponse, upload_schedule, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.upload_schedules.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = await response.parse()
        assert_matches_type(UploadScheduleListResponse, upload_schedule, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.upload_schedules.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = await response.parse()
            assert_matches_type(UploadScheduleListResponse, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.delete(
            "string",
            knowledge_base_id="string",
        )
        assert_matches_type(DeleteResponse, upload_schedule, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.knowledge_bases.upload_schedules.with_raw_response.delete(
            "string",
            knowledge_base_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = await response.parse()
        assert_matches_type(DeleteResponse, upload_schedule, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.knowledge_bases.upload_schedules.with_streaming_response.delete(
            "string",
            knowledge_base_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = await response.parse()
            assert_matches_type(DeleteResponse, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.delete(
                "string",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_schedule_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.delete(
                "",
                knowledge_base_id="string",
            )
