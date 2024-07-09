# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["ThreadProcessParams", "History"]


class ThreadProcessParams(TypedDict, total=False):
    application_variant_id: Required[str]

    inputs: Required[Dict[str, object]]
    """Input data for the application. You must provide inputs for each input node"""

    history: Iterable[History]
    """History of the application"""

    x_selected_account_id: Annotated[str, PropertyInfo(alias="x-selected-account-id")]


class History(TypedDict, total=False):
    request: Required[str]
    """Request inputs"""

    response: Required[str]
    """Response outputs"""
