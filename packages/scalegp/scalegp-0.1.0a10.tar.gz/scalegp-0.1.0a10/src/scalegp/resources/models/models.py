# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ...types import model_list_params, model_create_params, model_update_params, model_retrieve_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    strip_not_given,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .deployments import (
    DeploymentsResource,
    AsyncDeploymentsResource,
    DeploymentsResourceWithRawResponse,
    AsyncDeploymentsResourceWithRawResponse,
    DeploymentsResourceWithStreamingResponse,
    AsyncDeploymentsResourceWithStreamingResponse,
)
from ..._base_client import (
    make_request_options,
)
from .usage_statistics import (
    UsageStatisticsResource,
    AsyncUsageStatisticsResource,
    UsageStatisticsResourceWithRawResponse,
    AsyncUsageStatisticsResourceWithRawResponse,
    UsageStatisticsResourceWithStreamingResponse,
    AsyncUsageStatisticsResourceWithStreamingResponse,
)
from ...types.shared.delete_response import DeleteResponse
from ...types.model_instance_response import ModelInstanceResponse
from ...types.model_instance_response_with_views import ModelInstanceResponseWithViews
from ...types.pagination_response_list_pydantic_main_model_instance_response_with_views import (
    PaginationResponseListPydanticMainModelInstanceResponseWithViews,
)

__all__ = ["ModelsResource", "AsyncModelsResource"]


class ModelsResource(SyncAPIResource):
    @cached_property
    def deployments(self) -> DeploymentsResource:
        return DeploymentsResource(self._client)

    @cached_property
    def usage_statistics(self) -> UsageStatisticsResource:
        return UsageStatisticsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ModelsResourceWithRawResponse:
        return ModelsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ModelsResourceWithStreamingResponse:
        return ModelsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        model_type: Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING"],
        name: str,
        base_model_id: str | NotGiven = NOT_GIVEN,
        base_model_metadata: model_create_params.BaseModelMetadata | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        model_card: str | NotGiven = NOT_GIVEN,
        model_creation_parameters: object | NotGiven = NOT_GIVEN,
        model_group_id: str | NotGiven = NOT_GIVEN,
        model_template_id: str | NotGiven = NOT_GIVEN,
        model_vendor: Literal["OPENAI", "COHERE", "GOOGLE", "ANTHROPIC", "LAUNCH", "LLMENGINE", "BEDROCK", "OTHER"]
        | NotGiven = NOT_GIVEN,
        training_data_card: str | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelInstanceResponse:
        """
        ### Description

        Creates and hosts a model based on a model template.

        Base embedding models, chunk ranking functions, and LLMs are often not
        sufficient for customer use cases. We have shown in various blogs that
        fine-tuning these models on customer data can lead to significant improvements
        in performance.

        1. [We Fine-Tuned GPT-4 to Beat the Industry Standard for Text2SQL](https://scale.com/blog/text2sql-fine-tuning)
        2. [OpenAI Names Scale as Preferred Partner to Fine-Tune GPT-3.5](https://scale.com/blog/open-ai-scale-partnership-gpt-3-5-fine-tuning)
        3. [How to Fine-Tune GPT-3.5 Turbo With OpenAI API](https://scale.com/blog/fine-tune-gpt-3.5)

        ### Details

        Before creating a model, you must first create a model template. A model
        template serves 2 purposes. First, it provides common scaffolding that is static
        across multiple models. Second, it exposes several variables that can be
        injected at model creation time to customize the model.

        For example, a model template can define a docker image that contains code to
        run a HuggingFace or SentenceTransformers model. This docker image code also
        accepts environment variables that can be set to swap out the model weights or
        model name. Refer to the Create Model Template API for more details.

        To create a new model, users must refer to an existing model template and
        provide the necessary parameters the the model template requires in its
        `model_creation_parameters_schema` field. The combination of the model template
        and the model creation parameters will be used to create and deploy a new model.

        Once a model has been created, it can be executed by calling the Execute Model
        API.

        ### Coming Soon

        Some of our EGP APIs depend on models, for example Knowledge Base APIs depend on
        embedding models, Chunk Ranking APIs depend on ranking models, and Completion
        APIs depend on LLMs.

        In the near future, if a model is created from a model template that is
        compatible with one of these APIs (based on the model template's
        `model_type field`), the model will automatically be registered with the API.
        This will allow users to immediately start using the model with those API
        without any additional setup.

        Args:
          account_id: The ID of the account that owns the given entity.

          model_type: An enum representing the different types of models supported.

              Attributes: COMPLETION: Denotes that the model type is completion.
              CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
              that the model type is agent. EMBEDDING: Denotes that the model type is
              embedding. RERANKING: Denotes that the model type is reranking.

          model_vendor: An enum representing the different types of model vendors supported.

              Attributes: OPENAI: Denotes that the model vendor is OpenAI. COHERE: Denotes
              that the model vendor is Cohere. GOOGLE: Denotes that the model vendor is
              Google. ANTHROPIC: Denotes that the model vendor is Anthropic. LLMENGINE:
              Denotes that the model vendor is LLM Engine. OTHER: Denotes that the model
              vendor is Other.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return self._post(
            "/v4/models",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "model_type": model_type,
                    "name": name,
                    "base_model_id": base_model_id,
                    "base_model_metadata": base_model_metadata,
                    "description": description,
                    "model_card": model_card,
                    "model_creation_parameters": model_creation_parameters,
                    "model_group_id": model_group_id,
                    "model_template_id": model_template_id,
                    "model_vendor": model_vendor,
                    "training_data_card": training_data_card,
                },
                model_create_params.ModelCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelInstanceResponse,
        )

    def retrieve(
        self,
        model_id: str,
        *,
        view: List[Literal["Deployments", "ModelGroup"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelInstanceResponseWithViews:
        """
        ### Description

        Gets the details of a model

        ### Details

        This API can be used to get information about a single model by ID. To use this
        API, pass in the `id` that was returned from your Create Model API call as a
        path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return self._get(
            f"/v4/models/{model_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"view": view}, model_retrieve_params.ModelRetrieveParams),
            ),
            cast_to=ModelInstanceResponseWithViews,
        )

    def update(
        self,
        model_id: str,
        *,
        base_model_id: str | NotGiven = NOT_GIVEN,
        base_model_metadata: model_update_params.BaseModelMetadata | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        model_card: str | NotGiven = NOT_GIVEN,
        model_creation_parameters: object | NotGiven = NOT_GIVEN,
        model_group_id: str | NotGiven = NOT_GIVEN,
        model_template_id: str | NotGiven = NOT_GIVEN,
        model_type: Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING"] | NotGiven = NOT_GIVEN,
        model_vendor: Literal["OPENAI", "COHERE", "GOOGLE", "ANTHROPIC", "LAUNCH", "LLMENGINE", "BEDROCK", "OTHER"]
        | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        training_data_card: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelInstanceResponse:
        """
        ### Description

        Updates a model

        ### Details

        This API can be used to update the model that matches the ID that was passed in
        as a path parameter. To use this API, pass in the `id` that was returned from
        your Create Model API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          model_type: An enum representing the different types of models supported.

              Attributes: COMPLETION: Denotes that the model type is completion.
              CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
              that the model type is agent. EMBEDDING: Denotes that the model type is
              embedding. RERANKING: Denotes that the model type is reranking.

          model_vendor: An enum representing the different types of model vendors supported.

              Attributes: OPENAI: Denotes that the model vendor is OpenAI. COHERE: Denotes
              that the model vendor is Cohere. GOOGLE: Denotes that the model vendor is
              Google. ANTHROPIC: Denotes that the model vendor is Anthropic. LLMENGINE:
              Denotes that the model vendor is LLM Engine. OTHER: Denotes that the model
              vendor is Other.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return self._patch(
            f"/v4/models/{model_id}",
            body=maybe_transform(
                {
                    "base_model_id": base_model_id,
                    "base_model_metadata": base_model_metadata,
                    "description": description,
                    "model_card": model_card,
                    "model_creation_parameters": model_creation_parameters,
                    "model_group_id": model_group_id,
                    "model_template_id": model_template_id,
                    "model_type": model_type,
                    "model_vendor": model_vendor,
                    "name": name,
                    "training_data_card": training_data_card,
                },
                model_update_params.ModelUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelInstanceResponse,
        )

    def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        model_group_id: str | NotGiven = NOT_GIVEN,
        model_type: str | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        sort_by: List[
            Literal[
                "model_vendor:asc",
                "model_vendor:desc",
                "base_model_id:asc",
                "base_model_id:desc",
                "base_model_metadata:asc",
                "base_model_metadata:desc",
                "model_creation_parameters:asc",
                "model_creation_parameters:desc",
                "model_card:asc",
                "model_card:desc",
                "training_data_card:asc",
                "training_data_card:desc",
                "description:asc",
                "description:desc",
                "model_template_id:asc",
                "model_template_id:desc",
                "model_group_id:asc",
                "model_group_id:desc",
                "model_group:asc",
                "model_group:desc",
                "request_schema:asc",
                "request_schema:desc",
                "response_schema:asc",
                "response_schema:desc",
                "deployment_count:asc",
                "deployment_count:desc",
                "supports_multi_turn:asc",
                "supports_multi_turn:desc",
                "deployments:asc",
                "deployments:desc",
                "id:asc",
                "id:desc",
                "created_at:asc",
                "created_at:desc",
                "account_id:asc",
                "account_id:desc",
                "created_by_user_id:asc",
                "created_by_user_id:desc",
                "created_by_user:asc",
                "created_by_user:desc",
                "name:asc",
                "name:desc",
                "model_type:asc",
                "model_type:desc",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        view: List[Literal["Deployments", "ModelGroup"]] | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaginationResponseListPydanticMainModelInstanceResponseWithViews:
        """
        ### Description

        Lists all models accessible to the user.

        ### Details

        This API can be used to list models. If a user has access to multiple accounts,
        all models from all accounts the user is associated with will be returned.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return self._get(
            "/v4/models",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "model_group_id": model_group_id,
                        "model_type": model_type,
                        "page": page,
                        "sort_by": sort_by,
                        "view": view,
                    },
                    model_list_params.ModelListParams,
                ),
            ),
            cast_to=PaginationResponseListPydanticMainModelInstanceResponseWithViews,
        )

    def delete(
        self,
        model_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteResponse:
        """
        ### Description

        Deletes a model

        ### Details

        This API can be used to delete a model by ID. To use this API, pass in the `id`
        that was returned from your Create Model API call as a path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return self._delete(
            f"/v4/models/{model_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )


class AsyncModelsResource(AsyncAPIResource):
    @cached_property
    def deployments(self) -> AsyncDeploymentsResource:
        return AsyncDeploymentsResource(self._client)

    @cached_property
    def usage_statistics(self) -> AsyncUsageStatisticsResource:
        return AsyncUsageStatisticsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncModelsResourceWithRawResponse:
        return AsyncModelsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncModelsResourceWithStreamingResponse:
        return AsyncModelsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        model_type: Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING"],
        name: str,
        base_model_id: str | NotGiven = NOT_GIVEN,
        base_model_metadata: model_create_params.BaseModelMetadata | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        model_card: str | NotGiven = NOT_GIVEN,
        model_creation_parameters: object | NotGiven = NOT_GIVEN,
        model_group_id: str | NotGiven = NOT_GIVEN,
        model_template_id: str | NotGiven = NOT_GIVEN,
        model_vendor: Literal["OPENAI", "COHERE", "GOOGLE", "ANTHROPIC", "LAUNCH", "LLMENGINE", "BEDROCK", "OTHER"]
        | NotGiven = NOT_GIVEN,
        training_data_card: str | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelInstanceResponse:
        """
        ### Description

        Creates and hosts a model based on a model template.

        Base embedding models, chunk ranking functions, and LLMs are often not
        sufficient for customer use cases. We have shown in various blogs that
        fine-tuning these models on customer data can lead to significant improvements
        in performance.

        1. [We Fine-Tuned GPT-4 to Beat the Industry Standard for Text2SQL](https://scale.com/blog/text2sql-fine-tuning)
        2. [OpenAI Names Scale as Preferred Partner to Fine-Tune GPT-3.5](https://scale.com/blog/open-ai-scale-partnership-gpt-3-5-fine-tuning)
        3. [How to Fine-Tune GPT-3.5 Turbo With OpenAI API](https://scale.com/blog/fine-tune-gpt-3.5)

        ### Details

        Before creating a model, you must first create a model template. A model
        template serves 2 purposes. First, it provides common scaffolding that is static
        across multiple models. Second, it exposes several variables that can be
        injected at model creation time to customize the model.

        For example, a model template can define a docker image that contains code to
        run a HuggingFace or SentenceTransformers model. This docker image code also
        accepts environment variables that can be set to swap out the model weights or
        model name. Refer to the Create Model Template API for more details.

        To create a new model, users must refer to an existing model template and
        provide the necessary parameters the the model template requires in its
        `model_creation_parameters_schema` field. The combination of the model template
        and the model creation parameters will be used to create and deploy a new model.

        Once a model has been created, it can be executed by calling the Execute Model
        API.

        ### Coming Soon

        Some of our EGP APIs depend on models, for example Knowledge Base APIs depend on
        embedding models, Chunk Ranking APIs depend on ranking models, and Completion
        APIs depend on LLMs.

        In the near future, if a model is created from a model template that is
        compatible with one of these APIs (based on the model template's
        `model_type field`), the model will automatically be registered with the API.
        This will allow users to immediately start using the model with those API
        without any additional setup.

        Args:
          account_id: The ID of the account that owns the given entity.

          model_type: An enum representing the different types of models supported.

              Attributes: COMPLETION: Denotes that the model type is completion.
              CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
              that the model type is agent. EMBEDDING: Denotes that the model type is
              embedding. RERANKING: Denotes that the model type is reranking.

          model_vendor: An enum representing the different types of model vendors supported.

              Attributes: OPENAI: Denotes that the model vendor is OpenAI. COHERE: Denotes
              that the model vendor is Cohere. GOOGLE: Denotes that the model vendor is
              Google. ANTHROPIC: Denotes that the model vendor is Anthropic. LLMENGINE:
              Denotes that the model vendor is LLM Engine. OTHER: Denotes that the model
              vendor is Other.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return await self._post(
            "/v4/models",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "model_type": model_type,
                    "name": name,
                    "base_model_id": base_model_id,
                    "base_model_metadata": base_model_metadata,
                    "description": description,
                    "model_card": model_card,
                    "model_creation_parameters": model_creation_parameters,
                    "model_group_id": model_group_id,
                    "model_template_id": model_template_id,
                    "model_vendor": model_vendor,
                    "training_data_card": training_data_card,
                },
                model_create_params.ModelCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelInstanceResponse,
        )

    async def retrieve(
        self,
        model_id: str,
        *,
        view: List[Literal["Deployments", "ModelGroup"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelInstanceResponseWithViews:
        """
        ### Description

        Gets the details of a model

        ### Details

        This API can be used to get information about a single model by ID. To use this
        API, pass in the `id` that was returned from your Create Model API call as a
        path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return await self._get(
            f"/v4/models/{model_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"view": view}, model_retrieve_params.ModelRetrieveParams),
            ),
            cast_to=ModelInstanceResponseWithViews,
        )

    async def update(
        self,
        model_id: str,
        *,
        base_model_id: str | NotGiven = NOT_GIVEN,
        base_model_metadata: model_update_params.BaseModelMetadata | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        model_card: str | NotGiven = NOT_GIVEN,
        model_creation_parameters: object | NotGiven = NOT_GIVEN,
        model_group_id: str | NotGiven = NOT_GIVEN,
        model_template_id: str | NotGiven = NOT_GIVEN,
        model_type: Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING"] | NotGiven = NOT_GIVEN,
        model_vendor: Literal["OPENAI", "COHERE", "GOOGLE", "ANTHROPIC", "LAUNCH", "LLMENGINE", "BEDROCK", "OTHER"]
        | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        training_data_card: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelInstanceResponse:
        """
        ### Description

        Updates a model

        ### Details

        This API can be used to update the model that matches the ID that was passed in
        as a path parameter. To use this API, pass in the `id` that was returned from
        your Create Model API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          model_type: An enum representing the different types of models supported.

              Attributes: COMPLETION: Denotes that the model type is completion.
              CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
              that the model type is agent. EMBEDDING: Denotes that the model type is
              embedding. RERANKING: Denotes that the model type is reranking.

          model_vendor: An enum representing the different types of model vendors supported.

              Attributes: OPENAI: Denotes that the model vendor is OpenAI. COHERE: Denotes
              that the model vendor is Cohere. GOOGLE: Denotes that the model vendor is
              Google. ANTHROPIC: Denotes that the model vendor is Anthropic. LLMENGINE:
              Denotes that the model vendor is LLM Engine. OTHER: Denotes that the model
              vendor is Other.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return await self._patch(
            f"/v4/models/{model_id}",
            body=await async_maybe_transform(
                {
                    "base_model_id": base_model_id,
                    "base_model_metadata": base_model_metadata,
                    "description": description,
                    "model_card": model_card,
                    "model_creation_parameters": model_creation_parameters,
                    "model_group_id": model_group_id,
                    "model_template_id": model_template_id,
                    "model_type": model_type,
                    "model_vendor": model_vendor,
                    "name": name,
                    "training_data_card": training_data_card,
                },
                model_update_params.ModelUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelInstanceResponse,
        )

    async def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        model_group_id: str | NotGiven = NOT_GIVEN,
        model_type: str | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        sort_by: List[
            Literal[
                "model_vendor:asc",
                "model_vendor:desc",
                "base_model_id:asc",
                "base_model_id:desc",
                "base_model_metadata:asc",
                "base_model_metadata:desc",
                "model_creation_parameters:asc",
                "model_creation_parameters:desc",
                "model_card:asc",
                "model_card:desc",
                "training_data_card:asc",
                "training_data_card:desc",
                "description:asc",
                "description:desc",
                "model_template_id:asc",
                "model_template_id:desc",
                "model_group_id:asc",
                "model_group_id:desc",
                "model_group:asc",
                "model_group:desc",
                "request_schema:asc",
                "request_schema:desc",
                "response_schema:asc",
                "response_schema:desc",
                "deployment_count:asc",
                "deployment_count:desc",
                "supports_multi_turn:asc",
                "supports_multi_turn:desc",
                "deployments:asc",
                "deployments:desc",
                "id:asc",
                "id:desc",
                "created_at:asc",
                "created_at:desc",
                "account_id:asc",
                "account_id:desc",
                "created_by_user_id:asc",
                "created_by_user_id:desc",
                "created_by_user:asc",
                "created_by_user:desc",
                "name:asc",
                "name:desc",
                "model_type:asc",
                "model_type:desc",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        view: List[Literal["Deployments", "ModelGroup"]] | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaginationResponseListPydanticMainModelInstanceResponseWithViews:
        """
        ### Description

        Lists all models accessible to the user.

        ### Details

        This API can be used to list models. If a user has access to multiple accounts,
        all models from all accounts the user is associated with will be returned.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return await self._get(
            "/v4/models",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "model_group_id": model_group_id,
                        "model_type": model_type,
                        "page": page,
                        "sort_by": sort_by,
                        "view": view,
                    },
                    model_list_params.ModelListParams,
                ),
            ),
            cast_to=PaginationResponseListPydanticMainModelInstanceResponseWithViews,
        )

    async def delete(
        self,
        model_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteResponse:
        """
        ### Description

        Deletes a model

        ### Details

        This API can be used to delete a model by ID. To use this API, pass in the `id`
        that was returned from your Create Model API call as a path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return await self._delete(
            f"/v4/models/{model_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )


class ModelsResourceWithRawResponse:
    def __init__(self, models: ModelsResource) -> None:
        self._models = models

        self.create = to_raw_response_wrapper(
            models.create,
        )
        self.retrieve = to_raw_response_wrapper(
            models.retrieve,
        )
        self.update = to_raw_response_wrapper(
            models.update,
        )
        self.list = to_raw_response_wrapper(
            models.list,
        )
        self.delete = to_raw_response_wrapper(
            models.delete,
        )

    @cached_property
    def deployments(self) -> DeploymentsResourceWithRawResponse:
        return DeploymentsResourceWithRawResponse(self._models.deployments)

    @cached_property
    def usage_statistics(self) -> UsageStatisticsResourceWithRawResponse:
        return UsageStatisticsResourceWithRawResponse(self._models.usage_statistics)


class AsyncModelsResourceWithRawResponse:
    def __init__(self, models: AsyncModelsResource) -> None:
        self._models = models

        self.create = async_to_raw_response_wrapper(
            models.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            models.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            models.update,
        )
        self.list = async_to_raw_response_wrapper(
            models.list,
        )
        self.delete = async_to_raw_response_wrapper(
            models.delete,
        )

    @cached_property
    def deployments(self) -> AsyncDeploymentsResourceWithRawResponse:
        return AsyncDeploymentsResourceWithRawResponse(self._models.deployments)

    @cached_property
    def usage_statistics(self) -> AsyncUsageStatisticsResourceWithRawResponse:
        return AsyncUsageStatisticsResourceWithRawResponse(self._models.usage_statistics)


class ModelsResourceWithStreamingResponse:
    def __init__(self, models: ModelsResource) -> None:
        self._models = models

        self.create = to_streamed_response_wrapper(
            models.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            models.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            models.update,
        )
        self.list = to_streamed_response_wrapper(
            models.list,
        )
        self.delete = to_streamed_response_wrapper(
            models.delete,
        )

    @cached_property
    def deployments(self) -> DeploymentsResourceWithStreamingResponse:
        return DeploymentsResourceWithStreamingResponse(self._models.deployments)

    @cached_property
    def usage_statistics(self) -> UsageStatisticsResourceWithStreamingResponse:
        return UsageStatisticsResourceWithStreamingResponse(self._models.usage_statistics)


class AsyncModelsResourceWithStreamingResponse:
    def __init__(self, models: AsyncModelsResource) -> None:
        self._models = models

        self.create = async_to_streamed_response_wrapper(
            models.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            models.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            models.update,
        )
        self.list = async_to_streamed_response_wrapper(
            models.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            models.delete,
        )

    @cached_property
    def deployments(self) -> AsyncDeploymentsResourceWithStreamingResponse:
        return AsyncDeploymentsResourceWithStreamingResponse(self._models.deployments)

    @cached_property
    def usage_statistics(self) -> AsyncUsageStatisticsResourceWithStreamingResponse:
        return AsyncUsageStatisticsResourceWithStreamingResponse(self._models.usage_statistics)
