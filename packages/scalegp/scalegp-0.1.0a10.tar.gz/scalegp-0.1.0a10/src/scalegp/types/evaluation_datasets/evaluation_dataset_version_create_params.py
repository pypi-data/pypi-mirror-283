# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["EvaluationDatasetVersionCreateParams"]


class EvaluationDatasetVersionCreateParams(TypedDict, total=False):
    account_id: str
    """The ID of the account that owns the given entity."""

    x_selected_account_id: Annotated[str, PropertyInfo(alias="x-selected-account-id")]
