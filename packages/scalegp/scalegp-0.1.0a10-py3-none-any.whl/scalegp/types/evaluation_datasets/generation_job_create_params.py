# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["GenerationJobCreateParams"]


class GenerationJobCreateParams(TypedDict, total=False):
    num_test_cases: int
    """Number of test cases to generate for the evaluation dataset"""

    x_selected_account_id: Annotated[str, PropertyInfo(alias="x-selected-account-id")]
