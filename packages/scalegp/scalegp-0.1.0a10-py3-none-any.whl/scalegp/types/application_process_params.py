# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ApplicationProcessParams", "Edge", "Node", "NodeConfiguration", "History"]


class ApplicationProcessParams(TypedDict, total=False):
    edges: Required[Iterable[Edge]]
    """List of edges in the application graph"""

    inputs: Required[Dict[str, object]]
    """Input data for the application. You must provide inputs for each input node"""

    nodes: Required[Iterable[Node]]
    """List of nodes in the application graph"""

    version: Required[Literal["V0"]]
    """
    An enum representing the version states of an application and its nodes'
    schemas. Attributes: V0: The initial version of an application schema.
    """

    history: Iterable[History]
    """History of the application"""


class Edge(TypedDict, total=False):
    from_field: Required[str]

    from_node: Required[str]

    to_field: Required[str]

    to_node: Required[str]


class NodeConfiguration(TypedDict, total=False):
    value: Required[object]


class Node(TypedDict, total=False):
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

    configuration: Dict[str, NodeConfiguration]


class History(TypedDict, total=False):
    request: Required[str]
    """Request inputs"""

    response: Required[str]
    """Response outputs"""
