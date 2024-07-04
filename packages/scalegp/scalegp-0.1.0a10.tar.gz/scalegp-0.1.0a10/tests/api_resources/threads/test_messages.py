# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scalegp import SGP, AsyncSGP
from tests.utils import assert_matches_type
from scalegp.types.applications.variant import ChatThreadHistory, ChatThreadFeedback, ApplicationInteraction

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMessages:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update(self, client: SGP) -> None:
        message = client.threads.messages.update(
            "string",
            thread_id="string",
        )
        assert_matches_type(ApplicationInteraction, message, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGP) -> None:
        message = client.threads.messages.update(
            "string",
            thread_id="string",
            output_text="string",
        )
        assert_matches_type(ApplicationInteraction, message, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGP) -> None:
        response = client.threads.messages.with_raw_response.update(
            "string",
            thread_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(ApplicationInteraction, message, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGP) -> None:
        with client.threads.messages.with_streaming_response.update(
            "string",
            thread_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = response.parse()
            assert_matches_type(ApplicationInteraction, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.messages.with_raw_response.update(
                "string",
                thread_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_interaction_id` but received ''"
        ):
            client.threads.messages.with_raw_response.update(
                "",
                thread_id="string",
            )

    @parametrize
    def test_method_list(self, client: SGP) -> None:
        message = client.threads.messages.list(
            "string",
        )
        assert_matches_type(ChatThreadHistory, message, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGP) -> None:
        response = client.threads.messages.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(ChatThreadHistory, message, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGP) -> None:
        with client.threads.messages.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = response.parse()
            assert_matches_type(ChatThreadHistory, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.messages.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_feedback(self, client: SGP) -> None:
        message = client.threads.messages.feedback(
            thread_id="string",
            path_application_interaction_id="string",
            body_application_interaction_id="string",
            chat_thread_id="string",
            description="string",
            sentiment="positive",
        )
        assert_matches_type(ChatThreadFeedback, message, path=["response"])

    @parametrize
    def test_raw_response_feedback(self, client: SGP) -> None:
        response = client.threads.messages.with_raw_response.feedback(
            thread_id="string",
            path_application_interaction_id="string",
            body_application_interaction_id="string",
            chat_thread_id="string",
            description="string",
            sentiment="positive",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(ChatThreadFeedback, message, path=["response"])

    @parametrize
    def test_streaming_response_feedback(self, client: SGP) -> None:
        with client.threads.messages.with_streaming_response.feedback(
            thread_id="string",
            path_application_interaction_id="string",
            body_application_interaction_id="string",
            chat_thread_id="string",
            description="string",
            sentiment="positive",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = response.parse()
            assert_matches_type(ChatThreadFeedback, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_feedback(self, client: SGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.messages.with_raw_response.feedback(
                thread_id="",
                path_application_interaction_id="string",
                body_application_interaction_id="string",
                chat_thread_id="string",
                description="string",
                sentiment="positive",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_application_interaction_id` but received ''"
        ):
            client.threads.messages.with_raw_response.feedback(
                thread_id="string",
                path_application_interaction_id="",
                body_application_interaction_id="",
                chat_thread_id="string",
                description="string",
                sentiment="positive",
            )


class TestAsyncMessages:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_update(self, async_client: AsyncSGP) -> None:
        message = await async_client.threads.messages.update(
            "string",
            thread_id="string",
        )
        assert_matches_type(ApplicationInteraction, message, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGP) -> None:
        message = await async_client.threads.messages.update(
            "string",
            thread_id="string",
            output_text="string",
        )
        assert_matches_type(ApplicationInteraction, message, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGP) -> None:
        response = await async_client.threads.messages.with_raw_response.update(
            "string",
            thread_id="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = await response.parse()
        assert_matches_type(ApplicationInteraction, message, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGP) -> None:
        async with async_client.threads.messages.with_streaming_response.update(
            "string",
            thread_id="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = await response.parse()
            assert_matches_type(ApplicationInteraction, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.messages.with_raw_response.update(
                "string",
                thread_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_interaction_id` but received ''"
        ):
            await async_client.threads.messages.with_raw_response.update(
                "",
                thread_id="string",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGP) -> None:
        message = await async_client.threads.messages.list(
            "string",
        )
        assert_matches_type(ChatThreadHistory, message, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGP) -> None:
        response = await async_client.threads.messages.with_raw_response.list(
            "string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = await response.parse()
        assert_matches_type(ChatThreadHistory, message, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGP) -> None:
        async with async_client.threads.messages.with_streaming_response.list(
            "string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = await response.parse()
            assert_matches_type(ChatThreadHistory, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.messages.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_feedback(self, async_client: AsyncSGP) -> None:
        message = await async_client.threads.messages.feedback(
            thread_id="string",
            path_application_interaction_id="string",
            body_application_interaction_id="string",
            chat_thread_id="string",
            description="string",
            sentiment="positive",
        )
        assert_matches_type(ChatThreadFeedback, message, path=["response"])

    @parametrize
    async def test_raw_response_feedback(self, async_client: AsyncSGP) -> None:
        response = await async_client.threads.messages.with_raw_response.feedback(
            thread_id="string",
            path_application_interaction_id="string",
            body_application_interaction_id="string",
            chat_thread_id="string",
            description="string",
            sentiment="positive",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = await response.parse()
        assert_matches_type(ChatThreadFeedback, message, path=["response"])

    @parametrize
    async def test_streaming_response_feedback(self, async_client: AsyncSGP) -> None:
        async with async_client.threads.messages.with_streaming_response.feedback(
            thread_id="string",
            path_application_interaction_id="string",
            body_application_interaction_id="string",
            chat_thread_id="string",
            description="string",
            sentiment="positive",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = await response.parse()
            assert_matches_type(ChatThreadFeedback, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_feedback(self, async_client: AsyncSGP) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.messages.with_raw_response.feedback(
                thread_id="",
                path_application_interaction_id="string",
                body_application_interaction_id="string",
                chat_thread_id="string",
                description="string",
                sentiment="positive",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_application_interaction_id` but received ''"
        ):
            await async_client.threads.messages.with_raw_response.feedback(
                thread_id="string",
                path_application_interaction_id="",
                body_application_interaction_id="",
                chat_thread_id="string",
                description="string",
                sentiment="positive",
            )
