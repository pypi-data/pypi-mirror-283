# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["EvaluationDatasetApproveBatchParams"]


class EvaluationDatasetApproveBatchParams(TypedDict, total=False):
    autogenerated_draft_test_cases: Required[List[str]]
    """Ids of auto generated draft test cases to be approved."""

    force: bool
    """Force approve a batch of autogenerated test case IDs for the evaluation dataset"""

    x_selected_account_id: Annotated[str, PropertyInfo(alias="x-selected-account-id")]
