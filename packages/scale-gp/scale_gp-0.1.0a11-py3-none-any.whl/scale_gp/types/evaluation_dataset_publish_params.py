# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["EvaluationDatasetPublishParams"]


class EvaluationDatasetPublishParams(TypedDict, total=False):
    force: bool
    """Force approve an evaluation dataset"""

    x_selected_account_id: Annotated[str, PropertyInfo(alias="x-selected-account-id")]
