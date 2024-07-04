# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import (
    ModelTemplateResponse,
    PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse,
)
from scalegp.types.shared import DeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestModelTemplates:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        model_template = client.model_templates.create(
            account_id="string",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="string",
            vendor_configuration={
                "bundle_config": {
                    "registry": "string",
                    "image": "string",
                    "tag": "string",
                }
            },
        )
        assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        model_template = client.model_templates.create(
            account_id="string",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="string",
            vendor_configuration={
                "vendor": "LAUNCH",
                "bundle_config": {
                    "registry": "string",
                    "image": "string",
                    "tag": "string",
                    "command": ["string", "string", "string"],
                    "env": {"foo": "string"},
                    "streaming_command": ["string", "string", "string"],
                    "readiness_initial_delay_seconds": 0,
                    "healthcheck_route": "string",
                    "predict_route": "string",
                    "streaming_predict_route": "string",
                },
                "endpoint_config": {
                    "cpus": 0,
                    "memory": "string",
                    "storage": "string",
                    "gpus": 0,
                    "gpu_type": "nvidia-tesla-t4",
                    "min_workers": 0,
                    "max_workers": 0,
                    "per_worker": 0,
                    "endpoint_type": "SYNC",
                    "high_priority": True,
                },
                "fine_tuning_job_bundle_config": {
                    "registry": "string",
                    "image": "string",
                    "tag": "string",
                    "command": ["string", "string", "string"],
                    "env": {"foo": "string"},
                    "mount_location": "string",
                    "training_dataset_schema_type": "GENERATION",
                    "resources": {
                        "cpus": 0,
                        "memory": "string",
                        "storage": "string",
                        "gpus": 0,
                        "gpu_type": "nvidia-tesla-t4",
                    },
                },
            },
            model_creation_parameters_schema={
                "parameters": [
                    {
                        "name": "string",
                        "type": "str",
                        "description": "string",
                        "required": True,
                    },
                    {
                        "name": "string",
                        "type": "str",
                        "description": "string",
                        "required": True,
                    },
                    {
                        "name": "string",
                        "type": "str",
                        "description": "string",
                        "required": True,
                    },
                ]
            },
            model_request_parameters_schema={
                "parameters": [
                    {
                        "name": "string",
                        "type": "str",
                        "description": "string",
                        "required": True,
                    },
                    {
                        "name": "string",
                        "type": "str",
                        "description": "string",
                        "required": True,
                    },
                    {
                        "name": "string",
                        "type": "str",
                        "description": "string",
                        "required": True,
                    },
                ]
            },
            x_selected_account_id="string",
        )
        assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.model_templates.with_raw_response.create(
            account_id="string",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="string",
            vendor_configuration={
                "bundle_config": {
                    "registry": "string",
                    "image": "string",
                    "tag": "string",
                }
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = response.parse()
        assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.model_templates.with_streaming_response.create(
            account_id="string",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="string",
            vendor_configuration={
                "bundle_config": {
                    "registry": "string",
                    "image": "string",
                    "tag": "string",
                }
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = response.parse()
            assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        model_template = client.model_templates.retrieve(
            "string",
        )
        assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.model_templates.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = response.parse()
        assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.model_templates.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = response.parse()
            assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_template_id` but received ''"):
            client.model_templates.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        model_template = client.model_templates.list()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse,
            model_template,
            path=["response"],
        )

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        model_template = client.model_templates.list(
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse,
            model_template,
            path=["response"],
        )

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.model_templates.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = response.parse()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse,
            model_template,
            path=["response"],
        )

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.model_templates.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = response.parse()
            assert_matches_type(
                PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse,
                model_template,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        model_template = client.model_templates.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, model_template, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.model_templates.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = response.parse()
        assert_matches_type(DeleteResponse, model_template, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.model_templates.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = response.parse()
            assert_matches_type(DeleteResponse, model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_template_id` but received ''"):
            client.model_templates.with_raw_response.delete(
                "",
            )


class TestAsyncModelTemplates:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        model_template = await async_client.model_templates.create(
            account_id="string",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="string",
            vendor_configuration={
                "bundle_config": {
                    "registry": "string",
                    "image": "string",
                    "tag": "string",
                }
            },
        )
        assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        model_template = await async_client.model_templates.create(
            account_id="string",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="string",
            vendor_configuration={
                "vendor": "LAUNCH",
                "bundle_config": {
                    "registry": "string",
                    "image": "string",
                    "tag": "string",
                    "command": ["string", "string", "string"],
                    "env": {"foo": "string"},
                    "streaming_command": ["string", "string", "string"],
                    "readiness_initial_delay_seconds": 0,
                    "healthcheck_route": "string",
                    "predict_route": "string",
                    "streaming_predict_route": "string",
                },
                "endpoint_config": {
                    "cpus": 0,
                    "memory": "string",
                    "storage": "string",
                    "gpus": 0,
                    "gpu_type": "nvidia-tesla-t4",
                    "min_workers": 0,
                    "max_workers": 0,
                    "per_worker": 0,
                    "endpoint_type": "SYNC",
                    "high_priority": True,
                },
                "fine_tuning_job_bundle_config": {
                    "registry": "string",
                    "image": "string",
                    "tag": "string",
                    "command": ["string", "string", "string"],
                    "env": {"foo": "string"},
                    "mount_location": "string",
                    "training_dataset_schema_type": "GENERATION",
                    "resources": {
                        "cpus": 0,
                        "memory": "string",
                        "storage": "string",
                        "gpus": 0,
                        "gpu_type": "nvidia-tesla-t4",
                    },
                },
            },
            model_creation_parameters_schema={
                "parameters": [
                    {
                        "name": "string",
                        "type": "str",
                        "description": "string",
                        "required": True,
                    },
                    {
                        "name": "string",
                        "type": "str",
                        "description": "string",
                        "required": True,
                    },
                    {
                        "name": "string",
                        "type": "str",
                        "description": "string",
                        "required": True,
                    },
                ]
            },
            model_request_parameters_schema={
                "parameters": [
                    {
                        "name": "string",
                        "type": "str",
                        "description": "string",
                        "required": True,
                    },
                    {
                        "name": "string",
                        "type": "str",
                        "description": "string",
                        "required": True,
                    },
                    {
                        "name": "string",
                        "type": "str",
                        "description": "string",
                        "required": True,
                    },
                ]
            },
            x_selected_account_id="string",
        )
        assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.model_templates.with_raw_response.create(
            account_id="string",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="string",
            vendor_configuration={
                "bundle_config": {
                    "registry": "string",
                    "image": "string",
                    "tag": "string",
                }
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = await response.parse()
        assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.model_templates.with_streaming_response.create(
            account_id="string",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="string",
            vendor_configuration={
                "bundle_config": {
                    "registry": "string",
                    "image": "string",
                    "tag": "string",
                }
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = await response.parse()
            assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        model_template = await async_client.model_templates.retrieve(
            "string",
        )
        assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.model_templates.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = await response.parse()
        assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.model_templates.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = await response.parse()
            assert_matches_type(ModelTemplateResponse, model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_template_id` but received ''"):
            await async_client.model_templates.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        model_template = await async_client.model_templates.list()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse,
            model_template,
            path=["response"],
        )

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        model_template = await async_client.model_templates.list(
            account_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse,
            model_template,
            path=["response"],
        )

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.model_templates.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = await response.parse()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse,
            model_template,
            path=["response"],
        )

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.model_templates.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = await response.parse()
            assert_matches_type(
                PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse,
                model_template,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        model_template = await async_client.model_templates.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, model_template, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.model_templates.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = await response.parse()
        assert_matches_type(DeleteResponse, model_template, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.model_templates.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = await response.parse()
            assert_matches_type(DeleteResponse, model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_template_id` but received ''"):
            await async_client.model_templates.with_raw_response.delete(
                "",
            )
