# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["TaskUpdateParams"]


class TaskUpdateParams(TypedDict, total=False):
    evaluation_id: Required[str]

    assigned_to: str
    """The ID of the user that the task is assigned to."""

    x_selected_account_id: Annotated[str, PropertyInfo(alias="x-selected-account-id")]
