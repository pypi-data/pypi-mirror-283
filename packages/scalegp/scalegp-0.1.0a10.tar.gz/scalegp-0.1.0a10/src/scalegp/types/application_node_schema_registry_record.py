# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "ApplicationNodeSchemaRegistryRecord",
    "NodeSchema",
    "NodeSchemaConfiguration",
    "NodeSchemaConfigurationNumberConfigurationFieldSchema",
    "NodeSchemaConfigurationNumberConfigurationFieldSchemaValidationRules",
    "NodeSchemaConfigurationStringConfigurationFieldSchema",
    "NodeSchemaConfigurationStringConfigurationFieldSchemaValidationRules",
    "NodeSchemaConfigurationBoolConfigurationFieldSchema",
    "NodeSchemaConfigurationBoolConfigurationFieldSchemaValidationRules",
    "NodeSchemaInputs",
    "NodeSchemaOutputs",
]


class NodeSchemaConfigurationNumberConfigurationFieldSchemaValidationRules(BaseModel):
    max_value: int

    min_value: int

    required: bool


class NodeSchemaConfigurationNumberConfigurationFieldSchema(BaseModel):
    docs: str

    label: str

    validation_rules: NodeSchemaConfigurationNumberConfigurationFieldSchemaValidationRules

    default: Optional[int] = None

    type: Optional[Literal["TEXT", "STRING_ARRAY", "NUMBER", "BOOL", "CHUNK_ARRAY"]] = None
    """An enumeration."""


class NodeSchemaConfigurationStringConfigurationFieldSchemaValidationRules(BaseModel):
    required: bool

    regex_pattern: Optional[str] = None


class NodeSchemaConfigurationStringConfigurationFieldSchema(BaseModel):
    docs: str

    label: str

    validation_rules: NodeSchemaConfigurationStringConfigurationFieldSchemaValidationRules

    type: Optional[Literal["TEXT", "STRING_ARRAY", "NUMBER", "BOOL", "CHUNK_ARRAY"]] = None
    """An enumeration."""


class NodeSchemaConfigurationBoolConfigurationFieldSchemaValidationRules(BaseModel):
    required: bool


class NodeSchemaConfigurationBoolConfigurationFieldSchema(BaseModel):
    docs: str

    label: str

    validation_rules: NodeSchemaConfigurationBoolConfigurationFieldSchemaValidationRules

    type: Optional[Literal["TEXT", "STRING_ARRAY", "NUMBER", "BOOL", "CHUNK_ARRAY"]] = None
    """An enumeration."""


NodeSchemaConfiguration = Union[
    NodeSchemaConfigurationNumberConfigurationFieldSchema,
    NodeSchemaConfigurationStringConfigurationFieldSchema,
    NodeSchemaConfigurationBoolConfigurationFieldSchema,
]


class NodeSchemaInputs(BaseModel):
    docs: str

    label: str

    name: str

    required: bool

    type: Literal["TEXT", "STRING_ARRAY", "NUMBER", "BOOL", "CHUNK_ARRAY"]
    """An enumeration."""


class NodeSchemaOutputs(BaseModel):
    docs: str

    label: str

    name: str

    type: Literal["TEXT", "STRING_ARRAY", "NUMBER", "BOOL", "CHUNK_ARRAY"]
    """An enumeration."""


class NodeSchema(BaseModel):
    configuration: Dict[str, NodeSchemaConfiguration]

    inputs: Dict[str, NodeSchemaInputs]

    outputs: Dict[str, NodeSchemaOutputs]


class ApplicationNodeSchemaRegistryRecord(BaseModel):
    id: str

    name: str

    node_schema: NodeSchema = FieldInfo(alias="nodeSchema")

    tags: List[Literal["INPUT_NODE", "OUTPUT_NODE", "RAG_NODE"]]

    type: Literal[
        "TEXT_INPUT_NODE",
        "TEXT_OUTPUT_NODE",
        "KNOWLEDGE_BASE_NODE",
        "RERANKER_NODE",
        "PROMPT_ENGINEERING_NODE",
        "COMPLETION_MODEL_NODE",
        "EXTERNAL_ENDPOINT_NODE",
    ]
    """An enumeration."""

    version: Literal["V0"]
    """
    An enum representing the version states of an application and its nodes'
    schemas. Attributes: V0: The initial version of an application schema.
    """
