# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["TestCaseBatchParams", "Body"]


class TestCaseBatchParams(TypedDict, total=False):
    body: Required[Iterable[Body]]

    x_selected_account_id: Annotated[str, PropertyInfo(alias="x-selected-account-id")]


class Body(TypedDict, total=False):
    schema_type: Required[Literal["GENERATION"]]
    """An enumeration."""

    test_case_data: Required[object]
    """The data for the test case in a format matching the provided schema_type"""

    account_id: str
    """The ID of the account that owns the given entity."""

    chat_history: object
    """Used for tracking previous chat interactions for multi-chat test cases"""

    test_case_metadata: object
    """Metadata for the test case"""
