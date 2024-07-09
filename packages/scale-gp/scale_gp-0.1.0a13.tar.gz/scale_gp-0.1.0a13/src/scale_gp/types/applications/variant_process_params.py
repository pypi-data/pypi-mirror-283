# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Required, TypedDict

__all__ = ["VariantProcessParams", "History"]


class VariantProcessParams(TypedDict, total=False):
    inputs: Required[Dict[str, object]]
    """Input data for the application. You must provide inputs for each input node"""

    history: Iterable[History]
    """History of the application"""


class History(TypedDict, total=False):
    request: Required[str]
    """Request inputs"""

    response: Required[str]
    """Response outputs"""
