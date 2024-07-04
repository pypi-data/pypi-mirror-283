# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import (
    ApplicationVariantResponse,
    PaginationResponseListEgpAPIBackendServerAPIModelsApplicationModelsApplicationVariantResponse,
)
from scalegp.types.shared import DeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplicationVariants:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        application_variant = client.application_variants.create(
            account_id="string",
            application_spec_id="string",
            configuration={
                "nodes": [
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                ],
                "edges": [
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                ],
            },
            name="string",
            version="V0",
        )
        assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        application_variant = client.application_variants.create(
            account_id="string",
            application_spec_id="string",
            configuration={
                "nodes": [
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                        "configuration": {"foo": {"value": {}}},
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                        "configuration": {"foo": {"value": {}}},
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                        "configuration": {"foo": {"value": {}}},
                    },
                ],
                "edges": [
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                ],
            },
            name="string",
            version="V0",
            description="string",
            x_selected_account_id="string",
        )
        assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.application_variants.with_raw_response.create(
            account_id="string",
            application_spec_id="string",
            configuration={
                "nodes": [
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                ],
                "edges": [
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                ],
            },
            name="string",
            version="V0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = response.parse()
        assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.application_variants.with_streaming_response.create(
            account_id="string",
            application_spec_id="string",
            configuration={
                "nodes": [
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                ],
                "edges": [
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                ],
            },
            name="string",
            version="V0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = response.parse()
            assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        application_variant = client.application_variants.retrieve(
            "string",
        )
        assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.application_variants.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = response.parse()
        assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.application_variants.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = response.parse()
            assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            client.application_variants.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        application_variant = client.application_variants.list()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsApplicationModelsApplicationVariantResponse,
            application_variant,
            path=["response"],
        )

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        application_variant = client.application_variants.list(
            account_id="string",
            application_spec_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsApplicationModelsApplicationVariantResponse,
            application_variant,
            path=["response"],
        )

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.application_variants.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = response.parse()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsApplicationModelsApplicationVariantResponse,
            application_variant,
            path=["response"],
        )

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.application_variants.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = response.parse()
            assert_matches_type(
                PaginationResponseListEgpAPIBackendServerAPIModelsApplicationModelsApplicationVariantResponse,
                application_variant,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        application_variant = client.application_variants.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, application_variant, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.application_variants.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = response.parse()
        assert_matches_type(DeleteResponse, application_variant, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.application_variants.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = response.parse()
            assert_matches_type(DeleteResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            client.application_variants.with_raw_response.delete(
                "",
            )


class TestAsyncApplicationVariants:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        application_variant = await async_client.application_variants.create(
            account_id="string",
            application_spec_id="string",
            configuration={
                "nodes": [
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                ],
                "edges": [
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                ],
            },
            name="string",
            version="V0",
        )
        assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        application_variant = await async_client.application_variants.create(
            account_id="string",
            application_spec_id="string",
            configuration={
                "nodes": [
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                        "configuration": {"foo": {"value": {}}},
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                        "configuration": {"foo": {"value": {}}},
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                        "configuration": {"foo": {"value": {}}},
                    },
                ],
                "edges": [
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                ],
            },
            name="string",
            version="V0",
            description="string",
            x_selected_account_id="string",
        )
        assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.application_variants.with_raw_response.create(
            account_id="string",
            application_spec_id="string",
            configuration={
                "nodes": [
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                ],
                "edges": [
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                ],
            },
            name="string",
            version="V0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = await response.parse()
        assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.application_variants.with_streaming_response.create(
            account_id="string",
            application_spec_id="string",
            configuration={
                "nodes": [
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                    {
                        "id": "string",
                        "application_node_schema_id": "text_input_schema",
                    },
                ],
                "edges": [
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                    {
                        "from_node": "string",
                        "to_node": "string",
                        "from_field": "string",
                        "to_field": "string",
                    },
                ],
            },
            name="string",
            version="V0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = await response.parse()
            assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        application_variant = await async_client.application_variants.retrieve(
            "string",
        )
        assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.application_variants.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = await response.parse()
        assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.application_variants.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = await response.parse()
            assert_matches_type(ApplicationVariantResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            await async_client.application_variants.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        application_variant = await async_client.application_variants.list()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsApplicationModelsApplicationVariantResponse,
            application_variant,
            path=["response"],
        )

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        application_variant = await async_client.application_variants.list(
            account_id="string",
            application_spec_id="string",
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsApplicationModelsApplicationVariantResponse,
            application_variant,
            path=["response"],
        )

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.application_variants.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = await response.parse()
        assert_matches_type(
            PaginationResponseListEgpAPIBackendServerAPIModelsApplicationModelsApplicationVariantResponse,
            application_variant,
            path=["response"],
        )

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.application_variants.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = await response.parse()
            assert_matches_type(
                PaginationResponseListEgpAPIBackendServerAPIModelsApplicationModelsApplicationVariantResponse,
                application_variant,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        application_variant = await async_client.application_variants.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, application_variant, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.application_variants.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = await response.parse()
        assert_matches_type(DeleteResponse, application_variant, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.application_variants.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = await response.parse()
            assert_matches_type(DeleteResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            await async_client.application_variants.with_raw_response.delete(
                "",
            )
