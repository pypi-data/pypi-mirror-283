# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types import (
    ApplicationSpecResponse,
    ApplicationSpecListResponse,
)
from scalegp.types.shared import DeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplicationSpecs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGP) -> None:
        application_spec = client.application_specs.create(
            account_id="string",
            description="string",
            name="string",
        )
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGP) -> None:
        application_spec = client.application_specs.create(
            account_id="string",
            description="string",
            name="string",
            run_online_evaluation=True,
            theme_id="string",
            x_selected_account_id="string",
        )
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGP) -> None:
        response = client.application_specs.with_raw_response.create(
            account_id="string",
            description="string",
            name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = response.parse()
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGP) -> None:
        with client.application_specs.with_streaming_response.create(
            account_id="string",
            description="string",
            name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = response.parse()
            assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGP) -> None:
        application_spec = client.application_specs.retrieve(
            "string",
        )
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGP) -> None:
        response = client.application_specs.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = response.parse()
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGP) -> None:
        with client.application_specs.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = response.parse()
            assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            client.application_specs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update_overload_1(self, client: SGP) -> None:
        application_spec = client.application_specs.update(
            "string",
        )
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    def test_method_update_with_all_params_overload_1(self, client: SGP) -> None:
        application_spec = client.application_specs.update(
            "string",
            description="string",
            name="string",
            restore=True,
            run_online_evaluation=True,
            theme_id="string",
        )
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    def test_raw_response_update_overload_1(self, client: SGP) -> None:
        response = client.application_specs.with_raw_response.update(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = response.parse()
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    def test_streaming_response_update_overload_1(self, client: SGP) -> None:
        with client.application_specs.with_streaming_response.update(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = response.parse()
            assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_overload_1(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            client.application_specs.with_raw_response.update(
                "",
            )

    @parametrize
    def test_method_update_overload_2(self, client: SGP) -> None:
        application_spec = client.application_specs.update(
            "string",
            restore=True,
        )
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    def test_raw_response_update_overload_2(self, client: SGP) -> None:
        response = client.application_specs.with_raw_response.update(
            "string",
            restore=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = response.parse()
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    def test_streaming_response_update_overload_2(self, client: SGP) -> None:
        with client.application_specs.with_streaming_response.update(
            "string",
            restore=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = response.parse()
            assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_overload_2(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            client.application_specs.with_raw_response.update(
                "",
                restore=True,
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        application_spec = client.application_specs.list()
        assert_matches_type(ApplicationSpecListResponse, application_spec, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGP) -> None:
        application_spec = client.application_specs.list(
            account_id="string",
            include_archived=True,
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(ApplicationSpecListResponse, application_spec, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.application_specs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = response.parse()
        assert_matches_type(ApplicationSpecListResponse, application_spec, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.application_specs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = response.parse()
            assert_matches_type(ApplicationSpecListResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGP) -> None:
        application_spec = client.application_specs.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, application_spec, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGP) -> None:
        response = client.application_specs.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = response.parse()
        assert_matches_type(DeleteResponse, application_spec, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGP) -> None:
        with client.application_specs.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = response.parse()
            assert_matches_type(DeleteResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            client.application_specs.with_raw_response.delete(
                "",
            )


class TestAsyncApplicationSpecs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGP) -> None:
        application_spec = await async_client.application_specs.create(
            account_id="string",
            description="string",
            name="string",
        )
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGP) -> None:
        application_spec = await async_client.application_specs.create(
            account_id="string",
            description="string",
            name="string",
            run_online_evaluation=True,
            theme_id="string",
            x_selected_account_id="string",
        )
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGP) -> None:
        response = await async_client.application_specs.with_raw_response.create(
            account_id="string",
            description="string",
            name="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = await response.parse()
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGP) -> None:
        async with async_client.application_specs.with_streaming_response.create(
            account_id="string",
            description="string",
            name="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = await response.parse()
            assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGP) -> None:
        application_spec = await async_client.application_specs.retrieve(
            "string",
        )
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGP) -> None:
        response = await async_client.application_specs.with_raw_response.retrieve(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = await response.parse()
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGP) -> None:
        async with async_client.application_specs.with_streaming_response.retrieve(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = await response.parse()
            assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            await async_client.application_specs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update_overload_1(self, async_client: AsyncSGP) -> None:
        application_spec = await async_client.application_specs.update(
            "string",
        )
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    async def test_method_update_with_all_params_overload_1(self, async_client: AsyncSGP) -> None:
        application_spec = await async_client.application_specs.update(
            "string",
            description="string",
            name="string",
            restore=True,
            run_online_evaluation=True,
            theme_id="string",
        )
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    async def test_raw_response_update_overload_1(self, async_client: AsyncSGP) -> None:
        response = await async_client.application_specs.with_raw_response.update(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = await response.parse()
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    async def test_streaming_response_update_overload_1(self, async_client: AsyncSGP) -> None:
        async with async_client.application_specs.with_streaming_response.update(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = await response.parse()
            assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_overload_1(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            await async_client.application_specs.with_raw_response.update(
                "",
            )

    @parametrize
    async def test_method_update_overload_2(self, async_client: AsyncSGP) -> None:
        application_spec = await async_client.application_specs.update(
            "string",
            restore=True,
        )
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    async def test_raw_response_update_overload_2(self, async_client: AsyncSGP) -> None:
        response = await async_client.application_specs.with_raw_response.update(
            "string",
            restore=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = await response.parse()
        assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

    @parametrize
    async def test_streaming_response_update_overload_2(self, async_client: AsyncSGP) -> None:
        async with async_client.application_specs.with_streaming_response.update(
            "string",
            restore=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = await response.parse()
            assert_matches_type(ApplicationSpecResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_overload_2(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            await async_client.application_specs.with_raw_response.update(
                "",
                restore=True,
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        application_spec = await async_client.application_specs.list()
        assert_matches_type(ApplicationSpecListResponse, application_spec, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGP) -> None:
        application_spec = await async_client.application_specs.list(
            account_id="string",
            include_archived=True,
            limit=1,
            page=1,
            x_selected_account_id="string",
        )
        assert_matches_type(ApplicationSpecListResponse, application_spec, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.application_specs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = await response.parse()
        assert_matches_type(ApplicationSpecListResponse, application_spec, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.application_specs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = await response.parse()
            assert_matches_type(ApplicationSpecListResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGP) -> None:
        application_spec = await async_client.application_specs.delete(
            "string",
        )
        assert_matches_type(DeleteResponse, application_spec, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGP) -> None:
        response = await async_client.application_specs.with_raw_response.delete(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = await response.parse()
        assert_matches_type(DeleteResponse, application_spec, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGP) -> None:
        async with async_client.application_specs.with_streaming_response.delete(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = await response.parse()
            assert_matches_type(DeleteResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            await async_client.application_specs.with_raw_response.delete(
                "",
            )
