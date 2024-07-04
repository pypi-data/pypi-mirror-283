# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "ApplicationVariantCreateParams",
    "Configuration",
    "ConfigurationEdge",
    "ConfigurationNode",
    "ConfigurationNodeConfiguration",
]


class ApplicationVariantCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    configuration: Required[Configuration]

    name: Required[str]

    version: Required[Literal["V0"]]
    """
    An enum representing the version states of an application and its nodes'
    schemas. Attributes: V0: The initial version of an application schema.
    """

    description: str
    """Optional description of the application variant"""

    x_selected_account_id: Annotated[str, PropertyInfo(alias="x-selected-account-id")]


class ConfigurationEdge(TypedDict, total=False):
    from_field: Required[str]

    from_node: Required[str]

    to_field: Required[str]

    to_node: Required[str]


class ConfigurationNodeConfiguration(TypedDict, total=False):
    value: Required[object]


class ConfigurationNode(TypedDict, total=False):
    id: Required[str]

    application_node_schema_id: Required[
        Literal[
            "text_input_schema",
            "text_output_schema",
            "knowledge_base_schema",
            "reranker_schema",
            "prompt_engineering_schema",
            "completion_model_schema",
            "external_endpoint_schema",
        ]
    ]
    """An enumeration."""

    configuration: Dict[str, ConfigurationNodeConfiguration]


class Configuration(TypedDict, total=False):
    edges: Required[Iterable[ConfigurationEdge]]

    nodes: Required[Iterable[ConfigurationNode]]
