# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "ApplicationVariantResponse",
    "Configuration",
    "ConfigurationEdge",
    "ConfigurationNode",
    "ConfigurationNodeConfiguration",
]


class ConfigurationEdge(BaseModel):
    from_field: str

    from_node: str

    to_field: str

    to_node: str


class ConfigurationNodeConfiguration(BaseModel):
    value: object


class ConfigurationNode(BaseModel):
    id: str

    application_node_schema_id: Literal[
        "text_input_schema",
        "text_output_schema",
        "knowledge_base_schema",
        "reranker_schema",
        "prompt_engineering_schema",
        "completion_model_schema",
        "external_endpoint_schema",
    ]
    """An enumeration."""

    configuration: Optional[Dict[str, ConfigurationNodeConfiguration]] = None


class Configuration(BaseModel):
    edges: List[ConfigurationEdge]

    nodes: List[ConfigurationNode]


class ApplicationVariantResponse(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    configuration: Configuration

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    name: str

    version: Literal["V0"]
    """
    An enum representing the version states of an application and its nodes'
    schemas. Attributes: V0: The initial version of an application schema.
    """

    description: Optional[str] = None
    """Optional description of the application variant"""
