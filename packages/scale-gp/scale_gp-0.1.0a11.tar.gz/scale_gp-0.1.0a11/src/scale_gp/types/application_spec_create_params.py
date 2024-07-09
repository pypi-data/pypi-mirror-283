# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ApplicationSpecCreateParams"]


class ApplicationSpecCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    description: Required[str]
    """The description of the Application Spec"""

    name: Required[str]
    """The name of the Application Spec"""

    run_online_evaluation: bool
    """Whether the application spec should run online evaluation, default is `false`"""

    theme_id: str

    x_selected_account_id: Annotated[str, PropertyInfo(alias="x-selected-account-id")]
