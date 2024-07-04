# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ModelCreateParams", "BaseModelMetadata", "BaseModelMetadataModelDetails"]


class ModelCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    model_type: Required[Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING"]]
    """An enum representing the different types of models supported.

    Attributes: COMPLETION: Denotes that the model type is completion.
    CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
    that the model type is agent. EMBEDDING: Denotes that the model type is
    embedding. RERANKING: Denotes that the model type is reranking.
    """

    name: Required[str]

    base_model_id: str

    base_model_metadata: BaseModelMetadata

    description: str

    model_card: str

    model_creation_parameters: object

    model_group_id: str

    model_template_id: str

    model_vendor: Literal["OPENAI", "COHERE", "GOOGLE", "ANTHROPIC", "LAUNCH", "LLMENGINE", "BEDROCK", "OTHER"]
    """An enum representing the different types of model vendors supported.

    Attributes: OPENAI: Denotes that the model vendor is OpenAI. COHERE: Denotes
    that the model vendor is Cohere. GOOGLE: Denotes that the model vendor is
    Google. ANTHROPIC: Denotes that the model vendor is Anthropic. LLMENGINE:
    Denotes that the model vendor is LLM Engine. OTHER: Denotes that the model
    vendor is Other.
    """

    training_data_card: str

    x_selected_account_id: Annotated[str, PropertyInfo(alias="x-selected-account-id")]


class BaseModelMetadataModelDetails(TypedDict, total=False):
    alignments: int

    languages: int

    number_of_parameters: int

    token_context_window: int


class BaseModelMetadata(TypedDict, total=False):
    delivery_date: str

    model_developer: str

    model_license_url: str

    model_details: Annotated[BaseModelMetadataModelDetails, PropertyInfo(alias="modelDetails")]

    ui_model_section_type: Literal["PARTNER", "OPENSOURCE", "CUSTOM"]
    """An enumeration."""
