# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import SGPError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "SGP",
    "AsyncSGP",
    "Client",
    "AsyncClient",
]


class SGP(SyncAPIClient):
    knowledge_bases: resources.KnowledgeBasesResource
    knowledge_base_data_sources: resources.KnowledgeBaseDataSourcesResource
    chunks: resources.ChunksResource
    agents: resources.AgentsResource
    completions: resources.CompletionsResource
    chat_completions: resources.ChatCompletionsResource
    models: resources.ModelsResource
    model_deployments: resources.ModelDeploymentsResource
    model_groups: resources.ModelGroupsResource
    users: resources.UsersResource
    accounts: resources.AccountsResource
    question_sets: resources.QuestionSetsResource
    evaluations: resources.EvaluationsResource
    evaluation_configs: resources.EvaluationConfigsResource
    evaluation_datasets: resources.EvaluationDatasetsResource
    studio_projects: resources.StudioProjectsResource
    application_specs: resources.ApplicationSpecsResource
    questions: resources.QuestionsResource
    model_templates: resources.ModelTemplatesResource
    fine_tuning_jobs: resources.FineTuningJobsResource
    training_datasets: resources.TrainingDatasetsResource
    application_variants: resources.ApplicationVariantsResource
    application_deployments: resources.ApplicationDeploymentsResource
    application_variant_reports: resources.ApplicationVariantReportsResource
    application_test_case_outputs: resources.ApplicationTestCaseOutputsResource
    application_schemas: resources.ApplicationSchemasResource
    applications: resources.ApplicationsResource
    threads: resources.ThreadsResource
    themes: resources.ThemesResource
    with_raw_response: SGPWithRawResponse
    with_streaming_response: SGPWithStreamedResponse

    # client options
    sgp_api_key: str

    def __init__(
        self,
        *,
        sgp_api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous sgp client instance.

        This automatically infers the `sgp_api_key` argument from the `SGP_API_KEY` environment variable if it is not provided.
        """
        if sgp_api_key is None:
            sgp_api_key = os.environ.get("SGP_API_KEY")
        if sgp_api_key is None:
            raise SGPError(
                "The sgp_api_key client option must be set either by passing sgp_api_key to the client or by setting the SGP_API_KEY environment variable"
            )
        self.sgp_api_key = sgp_api_key

        if base_url is None:
            base_url = os.environ.get("SGP_BASE_URL")
        if base_url is None:
            base_url = f"https://api.egp.scale.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.knowledge_bases = resources.KnowledgeBasesResource(self)
        self.knowledge_base_data_sources = resources.KnowledgeBaseDataSourcesResource(self)
        self.chunks = resources.ChunksResource(self)
        self.agents = resources.AgentsResource(self)
        self.completions = resources.CompletionsResource(self)
        self.chat_completions = resources.ChatCompletionsResource(self)
        self.models = resources.ModelsResource(self)
        self.model_deployments = resources.ModelDeploymentsResource(self)
        self.model_groups = resources.ModelGroupsResource(self)
        self.users = resources.UsersResource(self)
        self.accounts = resources.AccountsResource(self)
        self.question_sets = resources.QuestionSetsResource(self)
        self.evaluations = resources.EvaluationsResource(self)
        self.evaluation_configs = resources.EvaluationConfigsResource(self)
        self.evaluation_datasets = resources.EvaluationDatasetsResource(self)
        self.studio_projects = resources.StudioProjectsResource(self)
        self.application_specs = resources.ApplicationSpecsResource(self)
        self.questions = resources.QuestionsResource(self)
        self.model_templates = resources.ModelTemplatesResource(self)
        self.fine_tuning_jobs = resources.FineTuningJobsResource(self)
        self.training_datasets = resources.TrainingDatasetsResource(self)
        self.application_variants = resources.ApplicationVariantsResource(self)
        self.application_deployments = resources.ApplicationDeploymentsResource(self)
        self.application_variant_reports = resources.ApplicationVariantReportsResource(self)
        self.application_test_case_outputs = resources.ApplicationTestCaseOutputsResource(self)
        self.application_schemas = resources.ApplicationSchemasResource(self)
        self.applications = resources.ApplicationsResource(self)
        self.threads = resources.ThreadsResource(self)
        self.themes = resources.ThemesResource(self)
        self.with_raw_response = SGPWithRawResponse(self)
        self.with_streaming_response = SGPWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        sgp_api_key = self.sgp_api_key
        return {"x-api-key": sgp_api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        sgp_api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            sgp_api_key=sgp_api_key or self.sgp_api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncSGP(AsyncAPIClient):
    knowledge_bases: resources.AsyncKnowledgeBasesResource
    knowledge_base_data_sources: resources.AsyncKnowledgeBaseDataSourcesResource
    chunks: resources.AsyncChunksResource
    agents: resources.AsyncAgentsResource
    completions: resources.AsyncCompletionsResource
    chat_completions: resources.AsyncChatCompletionsResource
    models: resources.AsyncModelsResource
    model_deployments: resources.AsyncModelDeploymentsResource
    model_groups: resources.AsyncModelGroupsResource
    users: resources.AsyncUsersResource
    accounts: resources.AsyncAccountsResource
    question_sets: resources.AsyncQuestionSetsResource
    evaluations: resources.AsyncEvaluationsResource
    evaluation_configs: resources.AsyncEvaluationConfigsResource
    evaluation_datasets: resources.AsyncEvaluationDatasetsResource
    studio_projects: resources.AsyncStudioProjectsResource
    application_specs: resources.AsyncApplicationSpecsResource
    questions: resources.AsyncQuestionsResource
    model_templates: resources.AsyncModelTemplatesResource
    fine_tuning_jobs: resources.AsyncFineTuningJobsResource
    training_datasets: resources.AsyncTrainingDatasetsResource
    application_variants: resources.AsyncApplicationVariantsResource
    application_deployments: resources.AsyncApplicationDeploymentsResource
    application_variant_reports: resources.AsyncApplicationVariantReportsResource
    application_test_case_outputs: resources.AsyncApplicationTestCaseOutputsResource
    application_schemas: resources.AsyncApplicationSchemasResource
    applications: resources.AsyncApplicationsResource
    threads: resources.AsyncThreadsResource
    themes: resources.AsyncThemesResource
    with_raw_response: AsyncSGPWithRawResponse
    with_streaming_response: AsyncSGPWithStreamedResponse

    # client options
    sgp_api_key: str

    def __init__(
        self,
        *,
        sgp_api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async sgp client instance.

        This automatically infers the `sgp_api_key` argument from the `SGP_API_KEY` environment variable if it is not provided.
        """
        if sgp_api_key is None:
            sgp_api_key = os.environ.get("SGP_API_KEY")
        if sgp_api_key is None:
            raise SGPError(
                "The sgp_api_key client option must be set either by passing sgp_api_key to the client or by setting the SGP_API_KEY environment variable"
            )
        self.sgp_api_key = sgp_api_key

        if base_url is None:
            base_url = os.environ.get("SGP_BASE_URL")
        if base_url is None:
            base_url = f"https://api.egp.scale.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.knowledge_bases = resources.AsyncKnowledgeBasesResource(self)
        self.knowledge_base_data_sources = resources.AsyncKnowledgeBaseDataSourcesResource(self)
        self.chunks = resources.AsyncChunksResource(self)
        self.agents = resources.AsyncAgentsResource(self)
        self.completions = resources.AsyncCompletionsResource(self)
        self.chat_completions = resources.AsyncChatCompletionsResource(self)
        self.models = resources.AsyncModelsResource(self)
        self.model_deployments = resources.AsyncModelDeploymentsResource(self)
        self.model_groups = resources.AsyncModelGroupsResource(self)
        self.users = resources.AsyncUsersResource(self)
        self.accounts = resources.AsyncAccountsResource(self)
        self.question_sets = resources.AsyncQuestionSetsResource(self)
        self.evaluations = resources.AsyncEvaluationsResource(self)
        self.evaluation_configs = resources.AsyncEvaluationConfigsResource(self)
        self.evaluation_datasets = resources.AsyncEvaluationDatasetsResource(self)
        self.studio_projects = resources.AsyncStudioProjectsResource(self)
        self.application_specs = resources.AsyncApplicationSpecsResource(self)
        self.questions = resources.AsyncQuestionsResource(self)
        self.model_templates = resources.AsyncModelTemplatesResource(self)
        self.fine_tuning_jobs = resources.AsyncFineTuningJobsResource(self)
        self.training_datasets = resources.AsyncTrainingDatasetsResource(self)
        self.application_variants = resources.AsyncApplicationVariantsResource(self)
        self.application_deployments = resources.AsyncApplicationDeploymentsResource(self)
        self.application_variant_reports = resources.AsyncApplicationVariantReportsResource(self)
        self.application_test_case_outputs = resources.AsyncApplicationTestCaseOutputsResource(self)
        self.application_schemas = resources.AsyncApplicationSchemasResource(self)
        self.applications = resources.AsyncApplicationsResource(self)
        self.threads = resources.AsyncThreadsResource(self)
        self.themes = resources.AsyncThemesResource(self)
        self.with_raw_response = AsyncSGPWithRawResponse(self)
        self.with_streaming_response = AsyncSGPWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        sgp_api_key = self.sgp_api_key
        return {"x-api-key": sgp_api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        sgp_api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            sgp_api_key=sgp_api_key or self.sgp_api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class SGPWithRawResponse:
    def __init__(self, client: SGP) -> None:
        self.knowledge_bases = resources.KnowledgeBasesResourceWithRawResponse(client.knowledge_bases)
        self.knowledge_base_data_sources = resources.KnowledgeBaseDataSourcesResourceWithRawResponse(
            client.knowledge_base_data_sources
        )
        self.chunks = resources.ChunksResourceWithRawResponse(client.chunks)
        self.agents = resources.AgentsResourceWithRawResponse(client.agents)
        self.completions = resources.CompletionsResourceWithRawResponse(client.completions)
        self.chat_completions = resources.ChatCompletionsResourceWithRawResponse(client.chat_completions)
        self.models = resources.ModelsResourceWithRawResponse(client.models)
        self.model_deployments = resources.ModelDeploymentsResourceWithRawResponse(client.model_deployments)
        self.model_groups = resources.ModelGroupsResourceWithRawResponse(client.model_groups)
        self.users = resources.UsersResourceWithRawResponse(client.users)
        self.accounts = resources.AccountsResourceWithRawResponse(client.accounts)
        self.question_sets = resources.QuestionSetsResourceWithRawResponse(client.question_sets)
        self.evaluations = resources.EvaluationsResourceWithRawResponse(client.evaluations)
        self.evaluation_configs = resources.EvaluationConfigsResourceWithRawResponse(client.evaluation_configs)
        self.evaluation_datasets = resources.EvaluationDatasetsResourceWithRawResponse(client.evaluation_datasets)
        self.studio_projects = resources.StudioProjectsResourceWithRawResponse(client.studio_projects)
        self.application_specs = resources.ApplicationSpecsResourceWithRawResponse(client.application_specs)
        self.questions = resources.QuestionsResourceWithRawResponse(client.questions)
        self.model_templates = resources.ModelTemplatesResourceWithRawResponse(client.model_templates)
        self.fine_tuning_jobs = resources.FineTuningJobsResourceWithRawResponse(client.fine_tuning_jobs)
        self.training_datasets = resources.TrainingDatasetsResourceWithRawResponse(client.training_datasets)
        self.application_variants = resources.ApplicationVariantsResourceWithRawResponse(client.application_variants)
        self.application_deployments = resources.ApplicationDeploymentsResourceWithRawResponse(
            client.application_deployments
        )
        self.application_variant_reports = resources.ApplicationVariantReportsResourceWithRawResponse(
            client.application_variant_reports
        )
        self.application_test_case_outputs = resources.ApplicationTestCaseOutputsResourceWithRawResponse(
            client.application_test_case_outputs
        )
        self.application_schemas = resources.ApplicationSchemasResourceWithRawResponse(client.application_schemas)
        self.applications = resources.ApplicationsResourceWithRawResponse(client.applications)
        self.threads = resources.ThreadsResourceWithRawResponse(client.threads)
        self.themes = resources.ThemesResourceWithRawResponse(client.themes)


class AsyncSGPWithRawResponse:
    def __init__(self, client: AsyncSGP) -> None:
        self.knowledge_bases = resources.AsyncKnowledgeBasesResourceWithRawResponse(client.knowledge_bases)
        self.knowledge_base_data_sources = resources.AsyncKnowledgeBaseDataSourcesResourceWithRawResponse(
            client.knowledge_base_data_sources
        )
        self.chunks = resources.AsyncChunksResourceWithRawResponse(client.chunks)
        self.agents = resources.AsyncAgentsResourceWithRawResponse(client.agents)
        self.completions = resources.AsyncCompletionsResourceWithRawResponse(client.completions)
        self.chat_completions = resources.AsyncChatCompletionsResourceWithRawResponse(client.chat_completions)
        self.models = resources.AsyncModelsResourceWithRawResponse(client.models)
        self.model_deployments = resources.AsyncModelDeploymentsResourceWithRawResponse(client.model_deployments)
        self.model_groups = resources.AsyncModelGroupsResourceWithRawResponse(client.model_groups)
        self.users = resources.AsyncUsersResourceWithRawResponse(client.users)
        self.accounts = resources.AsyncAccountsResourceWithRawResponse(client.accounts)
        self.question_sets = resources.AsyncQuestionSetsResourceWithRawResponse(client.question_sets)
        self.evaluations = resources.AsyncEvaluationsResourceWithRawResponse(client.evaluations)
        self.evaluation_configs = resources.AsyncEvaluationConfigsResourceWithRawResponse(client.evaluation_configs)
        self.evaluation_datasets = resources.AsyncEvaluationDatasetsResourceWithRawResponse(client.evaluation_datasets)
        self.studio_projects = resources.AsyncStudioProjectsResourceWithRawResponse(client.studio_projects)
        self.application_specs = resources.AsyncApplicationSpecsResourceWithRawResponse(client.application_specs)
        self.questions = resources.AsyncQuestionsResourceWithRawResponse(client.questions)
        self.model_templates = resources.AsyncModelTemplatesResourceWithRawResponse(client.model_templates)
        self.fine_tuning_jobs = resources.AsyncFineTuningJobsResourceWithRawResponse(client.fine_tuning_jobs)
        self.training_datasets = resources.AsyncTrainingDatasetsResourceWithRawResponse(client.training_datasets)
        self.application_variants = resources.AsyncApplicationVariantsResourceWithRawResponse(
            client.application_variants
        )
        self.application_deployments = resources.AsyncApplicationDeploymentsResourceWithRawResponse(
            client.application_deployments
        )
        self.application_variant_reports = resources.AsyncApplicationVariantReportsResourceWithRawResponse(
            client.application_variant_reports
        )
        self.application_test_case_outputs = resources.AsyncApplicationTestCaseOutputsResourceWithRawResponse(
            client.application_test_case_outputs
        )
        self.application_schemas = resources.AsyncApplicationSchemasResourceWithRawResponse(client.application_schemas)
        self.applications = resources.AsyncApplicationsResourceWithRawResponse(client.applications)
        self.threads = resources.AsyncThreadsResourceWithRawResponse(client.threads)
        self.themes = resources.AsyncThemesResourceWithRawResponse(client.themes)


class SGPWithStreamedResponse:
    def __init__(self, client: SGP) -> None:
        self.knowledge_bases = resources.KnowledgeBasesResourceWithStreamingResponse(client.knowledge_bases)
        self.knowledge_base_data_sources = resources.KnowledgeBaseDataSourcesResourceWithStreamingResponse(
            client.knowledge_base_data_sources
        )
        self.chunks = resources.ChunksResourceWithStreamingResponse(client.chunks)
        self.agents = resources.AgentsResourceWithStreamingResponse(client.agents)
        self.completions = resources.CompletionsResourceWithStreamingResponse(client.completions)
        self.chat_completions = resources.ChatCompletionsResourceWithStreamingResponse(client.chat_completions)
        self.models = resources.ModelsResourceWithStreamingResponse(client.models)
        self.model_deployments = resources.ModelDeploymentsResourceWithStreamingResponse(client.model_deployments)
        self.model_groups = resources.ModelGroupsResourceWithStreamingResponse(client.model_groups)
        self.users = resources.UsersResourceWithStreamingResponse(client.users)
        self.accounts = resources.AccountsResourceWithStreamingResponse(client.accounts)
        self.question_sets = resources.QuestionSetsResourceWithStreamingResponse(client.question_sets)
        self.evaluations = resources.EvaluationsResourceWithStreamingResponse(client.evaluations)
        self.evaluation_configs = resources.EvaluationConfigsResourceWithStreamingResponse(client.evaluation_configs)
        self.evaluation_datasets = resources.EvaluationDatasetsResourceWithStreamingResponse(client.evaluation_datasets)
        self.studio_projects = resources.StudioProjectsResourceWithStreamingResponse(client.studio_projects)
        self.application_specs = resources.ApplicationSpecsResourceWithStreamingResponse(client.application_specs)
        self.questions = resources.QuestionsResourceWithStreamingResponse(client.questions)
        self.model_templates = resources.ModelTemplatesResourceWithStreamingResponse(client.model_templates)
        self.fine_tuning_jobs = resources.FineTuningJobsResourceWithStreamingResponse(client.fine_tuning_jobs)
        self.training_datasets = resources.TrainingDatasetsResourceWithStreamingResponse(client.training_datasets)
        self.application_variants = resources.ApplicationVariantsResourceWithStreamingResponse(
            client.application_variants
        )
        self.application_deployments = resources.ApplicationDeploymentsResourceWithStreamingResponse(
            client.application_deployments
        )
        self.application_variant_reports = resources.ApplicationVariantReportsResourceWithStreamingResponse(
            client.application_variant_reports
        )
        self.application_test_case_outputs = resources.ApplicationTestCaseOutputsResourceWithStreamingResponse(
            client.application_test_case_outputs
        )
        self.application_schemas = resources.ApplicationSchemasResourceWithStreamingResponse(client.application_schemas)
        self.applications = resources.ApplicationsResourceWithStreamingResponse(client.applications)
        self.threads = resources.ThreadsResourceWithStreamingResponse(client.threads)
        self.themes = resources.ThemesResourceWithStreamingResponse(client.themes)


class AsyncSGPWithStreamedResponse:
    def __init__(self, client: AsyncSGP) -> None:
        self.knowledge_bases = resources.AsyncKnowledgeBasesResourceWithStreamingResponse(client.knowledge_bases)
        self.knowledge_base_data_sources = resources.AsyncKnowledgeBaseDataSourcesResourceWithStreamingResponse(
            client.knowledge_base_data_sources
        )
        self.chunks = resources.AsyncChunksResourceWithStreamingResponse(client.chunks)
        self.agents = resources.AsyncAgentsResourceWithStreamingResponse(client.agents)
        self.completions = resources.AsyncCompletionsResourceWithStreamingResponse(client.completions)
        self.chat_completions = resources.AsyncChatCompletionsResourceWithStreamingResponse(client.chat_completions)
        self.models = resources.AsyncModelsResourceWithStreamingResponse(client.models)
        self.model_deployments = resources.AsyncModelDeploymentsResourceWithStreamingResponse(client.model_deployments)
        self.model_groups = resources.AsyncModelGroupsResourceWithStreamingResponse(client.model_groups)
        self.users = resources.AsyncUsersResourceWithStreamingResponse(client.users)
        self.accounts = resources.AsyncAccountsResourceWithStreamingResponse(client.accounts)
        self.question_sets = resources.AsyncQuestionSetsResourceWithStreamingResponse(client.question_sets)
        self.evaluations = resources.AsyncEvaluationsResourceWithStreamingResponse(client.evaluations)
        self.evaluation_configs = resources.AsyncEvaluationConfigsResourceWithStreamingResponse(
            client.evaluation_configs
        )
        self.evaluation_datasets = resources.AsyncEvaluationDatasetsResourceWithStreamingResponse(
            client.evaluation_datasets
        )
        self.studio_projects = resources.AsyncStudioProjectsResourceWithStreamingResponse(client.studio_projects)
        self.application_specs = resources.AsyncApplicationSpecsResourceWithStreamingResponse(client.application_specs)
        self.questions = resources.AsyncQuestionsResourceWithStreamingResponse(client.questions)
        self.model_templates = resources.AsyncModelTemplatesResourceWithStreamingResponse(client.model_templates)
        self.fine_tuning_jobs = resources.AsyncFineTuningJobsResourceWithStreamingResponse(client.fine_tuning_jobs)
        self.training_datasets = resources.AsyncTrainingDatasetsResourceWithStreamingResponse(client.training_datasets)
        self.application_variants = resources.AsyncApplicationVariantsResourceWithStreamingResponse(
            client.application_variants
        )
        self.application_deployments = resources.AsyncApplicationDeploymentsResourceWithStreamingResponse(
            client.application_deployments
        )
        self.application_variant_reports = resources.AsyncApplicationVariantReportsResourceWithStreamingResponse(
            client.application_variant_reports
        )
        self.application_test_case_outputs = resources.AsyncApplicationTestCaseOutputsResourceWithStreamingResponse(
            client.application_test_case_outputs
        )
        self.application_schemas = resources.AsyncApplicationSchemasResourceWithStreamingResponse(
            client.application_schemas
        )
        self.applications = resources.AsyncApplicationsResourceWithStreamingResponse(client.applications)
        self.threads = resources.AsyncThreadsResourceWithStreamingResponse(client.threads)
        self.themes = resources.AsyncThemesResourceWithStreamingResponse(client.themes)


Client = SGP

AsyncClient = AsyncSGP
