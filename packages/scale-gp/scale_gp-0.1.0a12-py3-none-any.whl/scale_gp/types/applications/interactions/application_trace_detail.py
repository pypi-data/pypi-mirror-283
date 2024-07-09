# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from ...application_variant_response import ApplicationVariantResponse
from ..variant.application_interaction import ApplicationInteraction

__all__ = ["ApplicationTraceDetail", "Span"]


class Span(BaseModel):
    id: str
    """Identifies the application step"""

    application_interaction_id: str
    """The id of the application insight this step belongs to"""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    node_id: str
    """The id of the node in the application_variant config that emitted this insight"""

    operation_status: Literal["SUCCESS", "ERROR"]
    """An enumeration."""

    operation_type: str
    """Type of the operation, e.g. RERANKING"""

    start_timestamp: datetime
    """The start time of the step"""

    operation_input: Optional[object] = None
    """The JSON representation of the input that this step received"""

    operation_metadata: Optional[object] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """

    operation_output: Optional[object] = None
    """The JSON representation of the output that this step emitted"""


class ApplicationTraceDetail(BaseModel):
    application_variant: ApplicationVariantResponse
    """Application variant"""

    interaction: ApplicationInteraction
    """Interaction details"""

    feedback: Optional[Literal["positive", "negative"]] = None
    """An enumeration."""

    feedback_comment: Optional[str] = None
    """Feedback comment"""

    metadata: Optional[object] = None
    """Trace metadata"""

    spans: Optional[List[Span]] = None
    """List of Span IDs belonging to this trace"""

    thread_interactions: Optional[List[ApplicationInteraction]] = None
    """List of interactions in the same thread"""
