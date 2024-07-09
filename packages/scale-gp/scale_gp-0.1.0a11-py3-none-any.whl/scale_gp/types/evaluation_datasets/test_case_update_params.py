# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypedDict

__all__ = ["TestCaseUpdateParams", "PartialTestCaseVersionRequest", "RestoreRequest"]


class PartialTestCaseVersionRequest(TypedDict, total=False):
    evaluation_dataset_id: Required[str]

    chat_history: object
    """Used for tracking previous chat interactions for multi-chat test cases"""

    restore: Literal[False]
    """Set to true to restore the entity from the database."""

    schema_type: Literal["GENERATION"]
    """An enumeration."""

    test_case_data: object
    """The data for the test case in a format matching the provided schema_type"""

    test_case_metadata: object
    """Metadata for the test case"""


class RestoreRequest(TypedDict, total=False):
    evaluation_dataset_id: Required[str]

    restore: Required[Literal[True]]
    """Set to true to restore the entity from the database."""


TestCaseUpdateParams = Union[PartialTestCaseVersionRequest, RestoreRequest]
