# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import (
    ModelInstanceResponse,
    ModelInstanceResponseWithViews,
    PaginationResponseListPydanticMainModelInstanceResponseWithViews,
)
from scalegp.types.shared import DeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestModels:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        model = client.models.create(
            account_id="string",
            model_type="COMPLETION",
            name="string",
        )
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        model = client.models.create(
            account_id="string",
            model_type="COMPLETION",
            name="string",
            base_model_id="string",
            base_model_metadata={
                "ui_model_section_type": "PARTNER",
                "model_developer": "string",
                "model_license_url": "string",
                "delivery_date": "string",
                "model_details": {
                    "number_of_parameters": 0,
                    "token_context_window": 0,
                    "languages": 0,
                    "alignments": 0,
                },
            },
            description="string",
            model_card="string",
            model_creation_parameters={},
            model_group_id="string",
            model_template_id="string",
            model_vendor="OPENAI",
            training_data_card="string",
            x_selected_account_id="string",
        )
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.models.with_raw_response.create(
            account_id="string",
            model_type="COMPLETION",
            name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.models.with_streaming_response.create(
            account_id="string",
            model_type="COMPLETION",
            name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(ModelInstanceResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        model = client.models.retrieve(
            "string",
        )
        assert_matches_type(ModelInstanceResponseWithViews, model, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGP) -> None:
        model = client.models.retrieve(
            "string",
            view=["Deployments", "ModelGroup"],
        )
        assert_matches_type(ModelInstanceResponseWithViews, model, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.models.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(ModelInstanceResponseWithViews, model, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.models.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(ModelInstanceResponseWithViews, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            client.models.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SGP) -> None:
        model = client.models.update(
            "string",
        )
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGP) -> None:
        model = client.models.update(
            "string",
            base_model_id="string",
            base_model_metadata={
                "ui_model_section_type": "PARTNER",
                "model_developer": "string",
                "model_license_url": "string",
                "delivery_date": "string",
                "model_details": {
                    "number_of_parameters": 0,
                    "token_context_window": 0,
                    "languages": 0,
                    "alignments": 0,
                },
            },
            description="string",
            model_card="string",
            model_creation_parameters={},
            model_group_id="string",
            model_template_id="string",
            model_type="COMPLETION",
            model_vendor="OPENAI",
            name="string",
            training_data_card="string",
        )
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGP) -> None:
        response = client.models.with_raw_response.update(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGP) -> None:
        with client.models.with_streaming_response.update(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(ModelInstanceResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            client.models.with_raw_response.update(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        model = client.models.list()
        assert_matches_type(PaginationResponseListPydanticMainModelInstanceResponseWithViews, model, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        model = client.models.list(
            account_id="string",
            limit=1,
            model_group_id="string",
            model_type="string",
            page=1,
            sort_by=["model_vendor:asc", "model_vendor:desc", "base_model_id:asc"],
            view=["Deployments", "ModelGroup"],
            x_selected_account_id="string",
        )
        assert_matches_type(PaginationResponseListPydanticMainModelInstanceResponseWithViews, model, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.models.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(PaginationResponseListPydanticMainModelInstanceResponseWithViews, model, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.models.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(
                PaginationResponseListPydanticMainModelInstanceResponseWithViews, model, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        model = client.models.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, model, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.models.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(DeleteResponse, model, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.models.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(DeleteResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            client.models.with_raw_response.delete(
                "",
            )


class TestAsyncModels:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        model = await async_client.models.create(
            account_id="string",
            model_type="COMPLETION",
            name="string",
        )
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        model = await async_client.models.create(
            account_id="string",
            model_type="COMPLETION",
            name="string",
            base_model_id="string",
            base_model_metadata={
                "ui_model_section_type": "PARTNER",
                "model_developer": "string",
                "model_license_url": "string",
                "delivery_date": "string",
                "model_details": {
                    "number_of_parameters": 0,
                    "token_context_window": 0,
                    "languages": 0,
                    "alignments": 0,
                },
            },
            description="string",
            model_card="string",
            model_creation_parameters={},
            model_group_id="string",
            model_template_id="string",
            model_vendor="OPENAI",
            training_data_card="string",
            x_selected_account_id="string",
        )
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.with_raw_response.create(
            account_id="string",
            model_type="COMPLETION",
            name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.models.with_streaming_response.create(
            account_id="string",
            model_type="COMPLETION",
            name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(ModelInstanceResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        model = await async_client.models.retrieve(
            "string",
        )
        assert_matches_type(ModelInstanceResponseWithViews, model, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGP) -> None:
        model = await async_client.models.retrieve(
            "string",
            view=["Deployments", "ModelGroup"],
        )
        assert_matches_type(ModelInstanceResponseWithViews, model, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(ModelInstanceResponseWithViews, model, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.models.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(ModelInstanceResponseWithViews, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            await async_client.models.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGP) -> None:
        model = await async_client.models.update(
            "string",
        )
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGP) -> None:
        model = await async_client.models.update(
            "string",
            base_model_id="string",
            base_model_metadata={
                "ui_model_section_type": "PARTNER",
                "model_developer": "string",
                "model_license_url": "string",
                "delivery_date": "string",
                "model_details": {
                    "number_of_parameters": 0,
                    "token_context_window": 0,
                    "languages": 0,
                    "alignments": 0,
                },
            },
            description="string",
            model_card="string",
            model_creation_parameters={},
            model_group_id="string",
            model_template_id="string",
            model_type="COMPLETION",
            model_vendor="OPENAI",
            name="string",
            training_data_card="string",
        )
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.with_raw_response.update(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(ModelInstanceResponse, model, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGP) -> None:
        async with async_client.models.with_streaming_response.update(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(ModelInstanceResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            await async_client.models.with_raw_response.update(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        model = await async_client.models.list()
        assert_matches_type(PaginationResponseListPydanticMainModelInstanceResponseWithViews, model, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        model = await async_client.models.list(
            account_id="string",
            limit=1,
            model_group_id="string",
            model_type="string",
            page=1,
            sort_by=["model_vendor:asc", "model_vendor:desc", "base_model_id:asc"],
            view=["Deployments", "ModelGroup"],
            x_selected_account_id="string",
        )
        assert_matches_type(PaginationResponseListPydanticMainModelInstanceResponseWithViews, model, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(PaginationResponseListPydanticMainModelInstanceResponseWithViews, model, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.models.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(
                PaginationResponseListPydanticMainModelInstanceResponseWithViews, model, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        model = await async_client.models.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, model, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.models.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(DeleteResponse, model, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.models.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(DeleteResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            await async_client.models.with_raw_response.delete(
                "",
            )
