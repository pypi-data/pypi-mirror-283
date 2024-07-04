# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import model_template_list_params, model_template_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    strip_not_given,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import (
    make_request_options,
)
from ..types.shared.delete_response import DeleteResponse
from ..types.model_template_response import ModelTemplateResponse
from ..types.pagination_response_list_egp_api_backend_server_api_models_model_api_models_model_template_response import (
    PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse,
)

__all__ = ["ModelTemplatesResource", "AsyncModelTemplatesResource"]


class ModelTemplatesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ModelTemplatesResourceWithRawResponse:
        return ModelTemplatesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ModelTemplatesResourceWithStreamingResponse:
        return ModelTemplatesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        endpoint_type: Literal["SYNC", "ASYNC", "STREAMING", "BATCH"],
        model_type: Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING"],
        name: str,
        vendor_configuration: model_template_create_params.VendorConfiguration,
        model_creation_parameters_schema: model_template_create_params.ModelCreationParametersSchema
        | NotGiven = NOT_GIVEN,
        model_request_parameters_schema: model_template_create_params.ModelRequestParametersSchema
        | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelTemplateResponse:
        """
        ### Description

        Creates a model template.

        ### Details

        Model templates serve 2 purposes. First, they provide common scaffolding that is
        static across multiple models. Second, they expose several variables that can be
        injected at model creation time to customize the model.

        For example, a model template can define a docker image that contains code to
        run a HuggingFace or SentenceTransformers model. This docker image code also
        accepts environment variables that can be set to swap out the model weights or
        model name.

        Two of the most important fields required to create a model template are the
        `model_creation_parameters_schema` and `model_request_parameters_schema` fields.

        The `model_creation_parameters_schema` field defines the schema for parameters
        that can be injected at model creation time. For example, if the schema contains
        a `model_weights_uri` field, which expects a string, when a model is created
        from this template, the user can provide a URI to a model weights file that can
        be used to swap out the model weights used by the model.

        The `model_request_parameters_schema` field defines the schema for parameters
        that can be injected by an end user at model execution time. For example, if the
        schema contains a `model_request_parameters` field, which expects a string, when
        a model is executed, the user can provide a string that will be passed to the
        model for inference.

        Args:
          account_id: The ID of the account that owns the given entity.

          endpoint_type: An enum representing the different types of model endpoint types supported.

              Attributes: SYNC: Denotes that the model endpoint type is sync. ASYNC: Denotes
              that the model endpoint type is async. STREAMING: Denotes that the model
              endpoint type is streaming. BATCH: Denotes that the model endpoint type is
              batch.

          model_type: An enum representing the different types of models supported.

              Attributes: COMPLETION: Denotes that the model type is completion.
              CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
              that the model type is agent. EMBEDDING: Denotes that the model type is
              embedding. RERANKING: Denotes that the model type is reranking.

          vendor_configuration: Configuration for launching a model using the Launch service which is an
              internal and self-hosted service developed by Scale that deploys models on
              Kubernetes.

              Attributes: vendor: The vendor of the model template bundle_config: The bundle
              configuration of the model template endpoint_config: The endpoint configuration
              of the model template

          model_creation_parameters_schema: The field names and types of available parameter fields which may be specified
              during model creation

          model_request_parameters_schema: The field names and types of available parameter fields which may be specified
              in a model execution API's `model_request_parameters` field.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return self._post(
            "/v4/model-templates",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "endpoint_type": endpoint_type,
                    "model_type": model_type,
                    "name": name,
                    "vendor_configuration": vendor_configuration,
                    "model_creation_parameters_schema": model_creation_parameters_schema,
                    "model_request_parameters_schema": model_request_parameters_schema,
                },
                model_template_create_params.ModelTemplateCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelTemplateResponse,
        )

    def retrieve(
        self,
        model_template_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelTemplateResponse:
        """
        ### Description

        Gets the details of a model template

        ### Details

        This API can be used to get information about a single model template by ID. To
        use this API, pass in the `id` that was returned from your Create Model Template
        API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_template_id:
            raise ValueError(f"Expected a non-empty value for `model_template_id` but received {model_template_id!r}")
        return self._get(
            f"/v4/model-templates/{model_template_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelTemplateResponse,
        )

    def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse:
        """
        ### Description

        Lists all model templates accessible to the user.

        ### Details

        This API can be used to list model templates. If a user has access to multiple
        accounts, all model templates from all accounts the user is associated with will
        be returned.

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
            "/v4/model-templates",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                    },
                    model_template_list_params.ModelTemplateListParams,
                ),
            ),
            cast_to=PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse,
        )

    def delete(
        self,
        model_template_id: str,
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

        Deletes a model template

        ### Details

        This API can be used to delete a model template by ID. To use this API, pass in
        the `id` that was returned from your Create Model Template API call as a path
        parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_template_id:
            raise ValueError(f"Expected a non-empty value for `model_template_id` but received {model_template_id!r}")
        return self._delete(
            f"/v4/model-templates/{model_template_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )


class AsyncModelTemplatesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncModelTemplatesResourceWithRawResponse:
        return AsyncModelTemplatesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncModelTemplatesResourceWithStreamingResponse:
        return AsyncModelTemplatesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        endpoint_type: Literal["SYNC", "ASYNC", "STREAMING", "BATCH"],
        model_type: Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING"],
        name: str,
        vendor_configuration: model_template_create_params.VendorConfiguration,
        model_creation_parameters_schema: model_template_create_params.ModelCreationParametersSchema
        | NotGiven = NOT_GIVEN,
        model_request_parameters_schema: model_template_create_params.ModelRequestParametersSchema
        | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelTemplateResponse:
        """
        ### Description

        Creates a model template.

        ### Details

        Model templates serve 2 purposes. First, they provide common scaffolding that is
        static across multiple models. Second, they expose several variables that can be
        injected at model creation time to customize the model.

        For example, a model template can define a docker image that contains code to
        run a HuggingFace or SentenceTransformers model. This docker image code also
        accepts environment variables that can be set to swap out the model weights or
        model name.

        Two of the most important fields required to create a model template are the
        `model_creation_parameters_schema` and `model_request_parameters_schema` fields.

        The `model_creation_parameters_schema` field defines the schema for parameters
        that can be injected at model creation time. For example, if the schema contains
        a `model_weights_uri` field, which expects a string, when a model is created
        from this template, the user can provide a URI to a model weights file that can
        be used to swap out the model weights used by the model.

        The `model_request_parameters_schema` field defines the schema for parameters
        that can be injected by an end user at model execution time. For example, if the
        schema contains a `model_request_parameters` field, which expects a string, when
        a model is executed, the user can provide a string that will be passed to the
        model for inference.

        Args:
          account_id: The ID of the account that owns the given entity.

          endpoint_type: An enum representing the different types of model endpoint types supported.

              Attributes: SYNC: Denotes that the model endpoint type is sync. ASYNC: Denotes
              that the model endpoint type is async. STREAMING: Denotes that the model
              endpoint type is streaming. BATCH: Denotes that the model endpoint type is
              batch.

          model_type: An enum representing the different types of models supported.

              Attributes: COMPLETION: Denotes that the model type is completion.
              CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
              that the model type is agent. EMBEDDING: Denotes that the model type is
              embedding. RERANKING: Denotes that the model type is reranking.

          vendor_configuration: Configuration for launching a model using the Launch service which is an
              internal and self-hosted service developed by Scale that deploys models on
              Kubernetes.

              Attributes: vendor: The vendor of the model template bundle_config: The bundle
              configuration of the model template endpoint_config: The endpoint configuration
              of the model template

          model_creation_parameters_schema: The field names and types of available parameter fields which may be specified
              during model creation

          model_request_parameters_schema: The field names and types of available parameter fields which may be specified
              in a model execution API's `model_request_parameters` field.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"x-selected-account-id": x_selected_account_id}), **(extra_headers or {})}
        return await self._post(
            "/v4/model-templates",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "endpoint_type": endpoint_type,
                    "model_type": model_type,
                    "name": name,
                    "vendor_configuration": vendor_configuration,
                    "model_creation_parameters_schema": model_creation_parameters_schema,
                    "model_request_parameters_schema": model_request_parameters_schema,
                },
                model_template_create_params.ModelTemplateCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelTemplateResponse,
        )

    async def retrieve(
        self,
        model_template_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelTemplateResponse:
        """
        ### Description

        Gets the details of a model template

        ### Details

        This API can be used to get information about a single model template by ID. To
        use this API, pass in the `id` that was returned from your Create Model Template
        API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_template_id:
            raise ValueError(f"Expected a non-empty value for `model_template_id` but received {model_template_id!r}")
        return await self._get(
            f"/v4/model-templates/{model_template_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelTemplateResponse,
        )

    async def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        x_selected_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse:
        """
        ### Description

        Lists all model templates accessible to the user.

        ### Details

        This API can be used to list model templates. If a user has access to multiple
        accounts, all model templates from all accounts the user is associated with will
        be returned.

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
            "/v4/model-templates",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                    },
                    model_template_list_params.ModelTemplateListParams,
                ),
            ),
            cast_to=PaginationResponseListEgpAPIBackendServerAPIModelsModelAPIModelsModelTemplateResponse,
        )

    async def delete(
        self,
        model_template_id: str,
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

        Deletes a model template

        ### Details

        This API can be used to delete a model template by ID. To use this API, pass in
        the `id` that was returned from your Create Model Template API call as a path
        parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_template_id:
            raise ValueError(f"Expected a non-empty value for `model_template_id` but received {model_template_id!r}")
        return await self._delete(
            f"/v4/model-templates/{model_template_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeleteResponse,
        )


class ModelTemplatesResourceWithRawResponse:
    def __init__(self, model_templates: ModelTemplatesResource) -> None:
        self._model_templates = model_templates

        self.create = to_raw_response_wrapper(
            model_templates.create,
        )
        self.retrieve = to_raw_response_wrapper(
            model_templates.retrieve,
        )
        self.list = to_raw_response_wrapper(
            model_templates.list,
        )
        self.delete = to_raw_response_wrapper(
            model_templates.delete,
        )


class AsyncModelTemplatesResourceWithRawResponse:
    def __init__(self, model_templates: AsyncModelTemplatesResource) -> None:
        self._model_templates = model_templates

        self.create = async_to_raw_response_wrapper(
            model_templates.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            model_templates.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            model_templates.list,
        )
        self.delete = async_to_raw_response_wrapper(
            model_templates.delete,
        )


class ModelTemplatesResourceWithStreamingResponse:
    def __init__(self, model_templates: ModelTemplatesResource) -> None:
        self._model_templates = model_templates

        self.create = to_streamed_response_wrapper(
            model_templates.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            model_templates.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            model_templates.list,
        )
        self.delete = to_streamed_response_wrapper(
            model_templates.delete,
        )


class AsyncModelTemplatesResourceWithStreamingResponse:
    def __init__(self, model_templates: AsyncModelTemplatesResource) -> None:
        self._model_templates = model_templates

        self.create = async_to_streamed_response_wrapper(
            model_templates.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            model_templates.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            model_templates.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            model_templates.delete,
        )
