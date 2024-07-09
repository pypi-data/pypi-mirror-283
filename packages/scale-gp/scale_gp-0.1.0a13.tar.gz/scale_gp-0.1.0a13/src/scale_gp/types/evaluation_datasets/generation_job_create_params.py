# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["GenerationJobCreateParams"]


class GenerationJobCreateParams(TypedDict, total=False):
    num_test_cases: int
    """Number of test cases to generate for the evaluation dataset"""
